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
from app.models.schemas import CVUploadResponse, AnalysisRequest, CompileRequest, AIAnalysisResponse, SaveSettingsRequest, FetchModelsRequest
from app.services.cv_parser import extract_text_from_pdf
from app.services.ai_engine import analyze_cv
from app.services.latex_builder import generate_latex, compile_pdf
import uuid
from tinydb import TinyDB, Query

router = APIRouter()
db = TinyDB('cv_database.json')
settings_db = TinyDB('settings.json')

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

@router.post("/cv/upload", response_model=CVUploadResponse)
async def upload_cv(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Stream-read with size limit to prevent memory exhaustion
    chunks = []
    total = 0
    async for chunk in file:
        total += len(chunk)
        if total > MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=413, detail="File too large. Maximum size is 10 MB.")
        chunks.append(chunk)
    contents = b"".join(chunks)

    # Validate PDF magic bytes
    if not contents[:5] == b"%PDF-":
        raise HTTPException(status_code=400, detail="File is not a valid PDF.")

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
        fallback_queue = asyncio.Queue()
        
        async def on_fallback(event):
            await fallback_queue.put(event)
        
        try:
            yield f"data: {json.dumps({'progress': 10, 'status': 'Parsing CV...'})}\n\n"
            await asyncio.sleep(0.5)
            
            yield f"data: {json.dumps({'progress': 30, 'status': 'Booting AI Model...'})}\n\n"
            await asyncio.sleep(0.5)
            
            yield f"data: {json.dumps({'progress': 50, 'status': 'AI Faking Skills & Tailoring Projects...'})}\n\n"
            
            # Run analyze_cv in a task so we can stream fallback events in real-time
            analysis_task = asyncio.create_task(
                analyze_cv(cv_text, request.job_description, on_fallback=on_fallback)
            )
            
            # Poll for fallback events while analysis is running
            while not analysis_task.done():
                try:
                    event = await asyncio.wait_for(fallback_queue.get(), timeout=0.3)
                    # Map fallback events to user-friendly SSE messages
                    if event["type"] == "trying":
                        model_short = event["model"].split("/")[-1]  # e.g. "nemotron-nano-9b-v2:free"
                        attempt = event.get("attempt", "?")
                        total = event.get("total", "?")
                        progress = min(50 + (int(attempt) * 4), 75)  # 54, 58, 62, 66, 70...
                        yield f"data: {json.dumps({'progress': progress, 'status': f'⚡ Trying model: {model_short} ({attempt}/{total})...', 'fallback': event})}\n\n"
                    elif event["type"] == "failed":
                        model_short = event["model"].split("/")[-1]
                        reason = event.get("reason", "Unknown")
                        yield f"data: {json.dumps({'progress': -2, 'status': f'⚠ {model_short} unavailable — {reason}', 'fallback': event})}\n\n"
                    elif event["type"] == "success":
                        model_short = event["model"].split("/")[-1]
                        yield f"data: {json.dumps({'progress': 76, 'status': f'✓ Connected to {model_short}', 'fallback': event})}\n\n"
                except asyncio.TimeoutError:
                    continue  # No event yet, keep polling
            
            # Drain any remaining events in the queue
            while not fallback_queue.empty():
                try:
                    event = fallback_queue.get_nowait()
                    if event["type"] == "success":
                        model_short = event["model"].split("/")[-1]
                        yield f"data: {json.dumps({'progress': 76, 'status': f'✓ Connected to {model_short}', 'fallback': event})}\n\n"
                except asyncio.QueueEmpty:
                    break
            
            # Get the result (may raise if all models failed)
            analysis_result = await analysis_task
            
            yield f"data: {json.dumps({'progress': 80, 'status': 'Fetching SearXNG Links...'})}\n\n"
            from app.services.roadmap_builder import build_enriched_roadmap
            from app.models.schemas import Roadmap
            enriched_dict = await build_enriched_roadmap(analysis_result.roadmap)
            analysis_result.roadmap = Roadmap(**enriched_dict)
            
            yield f"data: {json.dumps({'progress': 100, 'status': 'Complete!', 'result': analysis_result.model_dump()})}\n\n"
        except Exception as e:
            error_msg = str(e)
            print(f"ERROR in analyze_cv_stream: {error_msg}")
            
            # Check if it's a PROVIDER_DOWN error with structured failed_models data
            if error_msg.startswith("PROVIDER_DOWN:"):
                try:
                    failed_models = json.loads(error_msg.replace("PROVIDER_DOWN:", "", 1))
                except Exception:
                    failed_models = []
                yield f"data: {json.dumps({'progress': -1, 'status': 'All AI models are currently unavailable', 'provider_issue': True, 'failed_models': failed_models})}\n\n"
            else:
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
async def save_settings(request: SaveSettingsRequest):
    import os
    settings_db.truncate()
    settings_db.insert({
        "api_key": request.api_key,
        "model_provider": request.model_provider,
        "model_name": request.model_name,
        "searxng_url": request.searxng_url,
    })
    # Set the correct env var based on provider
    if request.api_key:
        if request.model_provider == "opencode-zen":
            os.environ["OPENCODE_API_KEY"] = request.api_key
        elif request.model_provider == "openai":
            os.environ["OPENAI_API_KEY"] = request.api_key
        elif request.model_provider == "anthropic":
            os.environ["ANTHROPIC_API_KEY"] = request.api_key
        elif request.model_provider == "gemini":
            os.environ["GEMINI_API_KEY"] = request.api_key
        else:
            os.environ["OPENROUTER_API_KEY"] = request.api_key
    return {"status": "saved"}


@router.post("/models")
async def fetch_models(request: FetchModelsRequest):
    """Fetch available models from a provider's API."""
    import httpx

    provider = request.provider
    api_key = request.api_key

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
