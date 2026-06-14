# Copyright 2026 Yug Dabgar
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import Response, JSONResponse, StreamingResponse
import json
import asyncio
from app.models.schemas import CVUploadResponse, AnalysisRequest, CompileRequest, AIAnalysisResponse
from app.services.cv_parser import extract_text_from_pdf
from app.services.ai_engine import analyze_cv
from app.services.latex_builder import generate_latex, compile_pdf
import uuid
from tinydb import TinyDB, Query

router = APIRouter()
db = TinyDB('cv_database.json')
settings_db = TinyDB('settings.json')

@router.post("/cv/upload", response_model=CVUploadResponse)
async def upload_cv(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    contents = await file.read()
    try:
        text = await extract_text_from_pdf(contents)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    cv_id = str(uuid.uuid4())
    db.insert({'id': cv_id, 'text': text})
    
    return CVUploadResponse(message="CV uploaded and parsed successfully", cv_id=cv_id, extracted_text=text)

@router.post("/analyze/stream")
async def analyze_cv_stream(request: AnalysisRequest):
    CV = Query()
    result = db.search(CV.id == request.cv_id)
    if not result:
        raise HTTPException(status_code=404, detail="CV not found.")
        
    cv_text = result[0]['text']
    
    async def event_generator():
        try:
            yield f"data: {json.dumps({'progress': 10, 'status': 'Parsing CV...'})}\n\n"
            await asyncio.sleep(0.5)
            
            yield f"data: {json.dumps({'progress': 30, 'status': 'Booting AI Model...'})}\n\n"
            await asyncio.sleep(0.5)
            
            yield f"data: {json.dumps({'progress': 50, 'status': 'AI Faking Skills & Tailoring Projects...'})}\n\n"
            analysis_result = await analyze_cv(cv_text, request.job_description)
            
            yield f"data: {json.dumps({'progress': 80, 'status': 'Fetching SearXNG Links...'})}\n\n"
            from app.services.roadmap_builder import build_enriched_roadmap
            from app.models.schemas import Roadmap
            enriched_dict = await build_enriched_roadmap(analysis_result.roadmap)
            analysis_result.roadmap = Roadmap(**enriched_dict)
            
            yield f"data: {json.dumps({'progress': 100, 'status': 'Complete!', 'result': analysis_result.model_dump()})}\n\n"
        except Exception as e:
            error_msg = str(e)
            print(f"ERROR in analyze_cv_stream: {error_msg}")
            yield f"data: {json.dumps({'progress': -1, 'status': error_msg})}\n\n"
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.post("/generate/latex")
async def generate_latex_endpoint(request: CompileRequest):
    try:
        tex = await generate_latex(request)
        return {"latex_code": tex}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"ERROR in generate_latex: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compile/pdf")
async def compile_pdf_endpoint(request: CompileRequest):
    try:
        tex = await generate_latex(request)
        pdf_bytes = await compile_pdf(tex)
        return Response(content=pdf_bytes, media_type="application/pdf")
    except Exception as e:
        print(f"ERROR in compile_pdf: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compile/pdf/stream")
async def compile_pdf_stream(request: CompileRequest):
    import base64
    
    async def event_generator():
        try:
            yield "data: " + json.dumps({"progress": 15, "status": "Generating LaTeX code..."}) + "\n\n"
            await asyncio.sleep(0.3)
            
            tex = await generate_latex(request)
            
            yield "data: " + json.dumps({"progress": 40, "status": "LaTeX generated. Writing .tex file..."}) + "\n\n"
            await asyncio.sleep(0.3)
            
            yield "data: " + json.dumps({"progress": 60, "status": "Running pdflatex compiler..."}) + "\n\n"
            await asyncio.sleep(0.2)
            
            pdf_bytes = await compile_pdf(tex)
            
            yield "data: " + json.dumps({"progress": 90, "status": "PDF compiled! Encoding..."}) + "\n\n"
            await asyncio.sleep(0.2)
            
            pdf_b64 = base64.b64encode(pdf_bytes).decode('utf-8')
            
            yield "data: " + json.dumps({"progress": 100, "status": "Complete!", "pdf_base64": pdf_b64}) + "\n\n"
        except Exception as e:
            error_msg = str(e)
            print(f"ERROR in compile_pdf_stream: {error_msg}")
            yield "data: " + json.dumps({"progress": -1, "status": f"Error: {error_msg}"}) + "\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/settings")
async def get_settings():
    all_settings = settings_db.all()
    if not all_settings:
        # Return defaults
        return {
            "api_key": "",
            "model_provider": "openrouter",
            "model_name": "google/gemma-4-31b-it:free",
            "searxng_url": "http://localhost:8888"
        }
    return all_settings[0]

@router.post("/settings")
async def save_settings(request: dict):
    import os
    settings_db.truncate()
    settings_db.insert({
        "api_key": request.get("api_key", ""),
        "model_provider": request.get("model_provider", "openrouter"),
        "model_name": request.get("model_name", "google/gemma-4-31b-it:free"),
        "searxng_url": request.get("searxng_url", "http://localhost:8888"),
    })
    # Set the correct env var based on provider
    provider = request.get("model_provider", "openrouter")
    if request.get("api_key"):
        if provider == "opencode-zen":
            os.environ["OPENCODE_API_KEY"] = request["api_key"]
        elif provider == "openai":
            os.environ["OPENAI_API_KEY"] = request["api_key"]
        elif provider == "anthropic":
            os.environ["ANTHROPIC_API_KEY"] = request["api_key"]
        elif provider == "gemini":
            os.environ["GEMINI_API_KEY"] = request["api_key"]
        else:
            os.environ["OPENROUTER_API_KEY"] = request["api_key"]
    return {"status": "saved"}


@router.post("/models")
async def fetch_models(request: dict):
    """Fetch available models from a provider's API."""
    import httpx

    provider = request.get("provider", "")
    api_key = request.get("api_key", "")

    if not provider or not api_key:
        return {"models": [], "count": 0, "error": "Provider and API key required"}

    models = []

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            if provider == "openrouter":
                resp = await client.get(
                    "https://openrouter.ai/api/v1/models",
                    headers={"Authorization": f"Bearer {api_key}"},
                )
                resp.raise_for_status()
                data = resp.json()
                for m in data.get("data", []):
                    model_id = m.get("id", "")
                    pricing = m.get("pricing", {})
                    prompt_price = float(pricing.get("prompt", "1") or "1")
                    is_free = ":free" in model_id or prompt_price == 0
                    models.append({
                        "id": model_id,
                        "name": m.get("name", model_id),
                        "free": is_free,
                    })

            elif provider == "opencode-zen":
                resp = await client.get(
                    "https://opencode.ai/zen/v1/models",
                    headers={"Authorization": f"Bearer {api_key}"},
                )
                resp.raise_for_status()
                data = resp.json()
                for m in data.get("data", []):
                    model_id = m.get("id", "")
                    is_free = "free" in model_id.lower()
                    models.append({
                        "id": model_id,
                        "name": m.get("id", model_id),
                        "free": is_free,
                    })

            elif provider == "openai":
                resp = await client.get(
                    "https://api.openai.com/v1/models",
                    headers={"Authorization": f"Bearer {api_key}"},
                )
                resp.raise_for_status()
                data = resp.json()
                for m in data.get("data", []):
                    model_id = m.get("id", "")
                    # Filter to chat models only
                    if any(k in model_id for k in ["gpt", "o1", "o3", "o4", "chatgpt"]):
                        models.append({
                            "id": model_id,
                            "name": model_id,
                            "free": False,
                        })

            elif provider == "anthropic":
                resp = await client.get(
                    "https://api.anthropic.com/v1/models",
                    headers={
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01",
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                for m in data.get("data", []):
                    model_id = m.get("id", "")
                    models.append({
                        "id": model_id,
                        "name": m.get("display_name", model_id),
                        "free": False,
                    })

            elif provider == "gemini":
                resp = await client.get(
                    f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}",
                )
                resp.raise_for_status()
                data = resp.json()
                for m in data.get("models", []):
                    model_id = m.get("name", "").replace("models/", "")
                    if "generateContent" in str(m.get("supportedGenerationMethods", [])):
                        models.append({
                            "id": f"gemini/{model_id}",
                            "name": m.get("displayName", model_id),
                            "free": False,
                        })

            else:
                return {"models": [], "count": 0, "error": f"Unknown provider: {provider}"}

    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        if status == 401 or status == 403:
            return {"models": [], "count": 0, "error": "Invalid API key"}
        return {"models": [], "count": 0, "error": f"API error: {status}"}
    except Exception as e:
        return {"models": [], "count": 0, "error": str(e)}

    # Sort: free models first, then alphabetical
    models.sort(key=lambda x: (not x["free"], x["id"]))

    return {"models": models, "count": len(models)}
