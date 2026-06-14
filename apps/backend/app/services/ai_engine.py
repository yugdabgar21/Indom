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

import os
import yaml
import json
from litellm import acompletion
from app.models.schemas import AIAnalysisResponse
from dotenv import load_dotenv
from tinydb import TinyDB

load_dotenv(override=True)

def load_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, "../../../../"))
    config_path = os.path.join(root_dir, "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_settings():
    """Load settings from TinyDB (set via UI), falling back to config.yaml and .env."""
    try:
        settings_db = TinyDB('settings.json')
        all_settings = settings_db.all()
        if all_settings:
            s = all_settings[0]
            # Set env var for litellm based on provider
            provider = s.get("model_provider", "openrouter")
            if s.get("api_key"):
                if provider == "opencode-zen":
                    os.environ["OPENCODE_API_KEY"] = s["api_key"]
                else:
                    os.environ["OPENROUTER_API_KEY"] = s["api_key"]
            return provider, s.get("model_name", "google/gemma-4-31b-it:free")
    except Exception:
        pass
    # Fallback to config.yaml
    config = load_config()
    return config["model"]["type"], config["model"]["model_name"]

async def analyze_cv(cv_text: str, job_description: str) -> AIAnalysisResponse:
    model_type, model_name = load_settings()
    
    system_prompt = """
    You are an expert ATS CV tailor. Your mandate: "SMART FAKING".
    
    STRICT RULES — READ CAREFULLY:
    1. PROJECTS: Extract ONLY the projects that EXIST in the original CV. Do NOT invent or add new projects. You MAY rewrite the "description" and "stack" fields of existing projects to better match the JD. Keep the original project "name" and "link" exactly as-is. IF the link is not a valid URL (e.g., just the word 'GitHub'), set the link to an empty string "". IMPORTANT: Keep each project description SHORT — maximum 2-3 lines. Be concise and impactful.
    2. EDUCATION: Extract EXACTLY as written in the CV. Do NOT modify, add, or remove any education entries. Copy degree, school, date_range, gpa verbatim.
    3. CERTIFICATIONS: Extract EXACTLY as written in the CV. Do NOT add fake certifications. If none exist, return an empty array [].
    4. LANGUAGES: Extract EXACTLY as written in the CV. If none are listed, default to ["English"].
    5. SKILLS: You CAN and SHOULD fake/inject skills into skills_tools, skills_automation, skills_ai_dev, skills_other to match the JD.
    6. FAKED_SKILLS: List every skill you added that was NOT in the original CV.
    
    You MUST output valid JSON matching this schema EXACTLY:
    {
      "full_name": "Extract from CV exactly",
      "email": "Extract from CV exactly",
      "phone": "Extract from CV exactly",
      "location": "Extract from CV exactly",
      "github_username": "Extract from CV or blank",
      "job_title": "Tailored job title matching the JD",
      "professional_summary": "A compelling professional summary (2-3 sentences). Mention role, core skills, and what value you bring. Tailored to the JD.",
      "skills_tools": "comma separated — CAN BE FAKED to match JD",
      "skills_automation": "comma separated — CAN BE FAKED to match JD",
      "skills_ai_dev": "comma separated — CAN BE FAKED to match JD",
      "skills_other": "comma separated — CAN BE FAKED to match JD",
      "faked_skills": ["every skill you injected that was NOT in original CV"],
      "projects": [
        {
          "name": "ORIGINAL project name from CV — DO NOT INVENT",
          "link": "ORIGINAL project URL from CV — or empty string '' if not a valid url",
          "description": "SHORT 2-3 line description. Rewritten to emphasize JD-matching skills — CAN BE FAKED",
          "stack": "Rewritten tech stack to match JD — CAN BE FAKED"
        }
      ],
      "education": [
        {
          "degree": "EXACT from CV — DO NOT CHANGE",
          "school": "EXACT from CV — DO NOT CHANGE",
          "date_range": "EXACT from CV — DO NOT CHANGE",
          "gpa": "EXACT from CV — DO NOT CHANGE"
        }
      ],
      "certifications": ["EXACT from CV only — DO NOT ADD FAKE ONES"],
      "languages": ["EXACT from CV — default to English if none found"],
      "match_score_before": 45,
      "match_score_after": 95,
      "roadmap": {
         "days": [
             {"day": 1, "topic": "topic name", "description": "short desc", "search_query": "youtube search query"},
             {"day": 2, "topic": "topic name", "description": "short desc", "search_query": "youtube search query"},
             {"day": 3, "topic": "topic name", "description": "short desc", "search_query": "youtube search query"},
             {"day": 4, "topic": "topic name", "description": "short desc", "search_query": "youtube search query"},
             {"day": 5, "topic": "topic name", "description": "short desc", "search_query": "youtube search query"}
         ]
      }
    }
    CRITICAL: The roadmap MUST have EXACTLY 5 days. NO MORE, NO LESS.
    CRITICAL: Return ONLY the JSON object. No markdown, no explanation, no extra text.
    """
    
    import asyncio as _asyncio
    last_error = None
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"CV:\n{cv_text}\n\nJob Description:\n{job_description}"}
    ]
    
    # --- OpenCode Zen: direct HTTP call (no litellm) ---
    if model_type == "opencode-zen":
        import httpx
        zen_api_key = os.environ.get("OPENCODE_API_KEY", "")
        if not zen_api_key:
            raise ValueError("NO_API_KEY:OpenCode Zen API key is not set. Please add your API key in Settings.")
        print(f"DEBUG: Attempting AI analysis with model: zen/{model_name}")
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                resp = await client.post(
                    "https://opencode.ai/zen/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {zen_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={"model": model_name, "messages": messages},
                )
                if resp.status_code != 200:
                    error_body = resp.text
                    print(f"WARNING: Zen API returned {resp.status_code}: {error_body}")
                    raise httpx.HTTPStatusError(
                        f"Zen API error {resp.status_code}: {error_body}",
                        request=resp.request, response=resp
                    )
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                print(f"DEBUG: Successfully used model: zen/{model_name}")
        except Exception as e:
            error_detail = str(e)
            # Try to extract response body for httpx errors
            if hasattr(e, 'response') and e.response is not None:
                error_detail = f"HTTP {e.response.status_code}: {e.response.text}"
            print(f"WARNING: Zen model zen/{model_name} failed: {error_detail}")
            content = None
            last_error = e
        
        # If Zen failed, try litellm fallbacks ONLY if OpenRouter key exists
        if content is None:
            openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")
            if not openrouter_key:
                zen_error = str(last_error) if last_error else "Unknown error"
                raise ValueError(f"NO_FALLBACK:Zen model failed: {zen_error}. No OpenRouter API key configured for fallback. Please check your Zen API key or add an OpenRouter key.")
            
            fallback_models = [
                "openrouter/nvidia/nemotron-nano-9b-v2:free",
                "openrouter/openai/gpt-oss-20b:free",
                "openrouter/z-ai/glm-4.5-air:free",
                "openrouter/google/gemma-4-31b-it:free",
                "openrouter/nvidia/nemotron-3-super-120b-a12b:free",
            ]
            for model_id in fallback_models:
                try:
                    print(f"DEBUG: Fallback — attempting model: {model_id}")
                    response = await acompletion(model=model_id, messages=messages)
                    content = response.choices[0].message.content
                    print(f"DEBUG: Successfully used fallback: {model_id}")
                    break
                except Exception as e:
                    print(f"WARNING: Fallback {model_id} failed: {str(e)}")
                    last_error = e
                    await _asyncio.sleep(1)
            else:
                raise ValueError(f"All AI models failed. Last error: {last_error}")
    
    # --- All other providers: use litellm ---
    else:
        model_string = model_name if model_name.startswith(f"{model_type}/") else f"{model_type}/{model_name}"
        fallback_models = [
            model_string,
            "openrouter/nvidia/nemotron-nano-9b-v2:free",
            "openrouter/openai/gpt-oss-20b:free",
            "openrouter/z-ai/glm-4.5-air:free",
            "openrouter/google/gemma-4-31b-it:free",
            "openrouter/nvidia/nemotron-3-super-120b-a12b:free",
        ]
        for model_id in fallback_models:
            try:
                print(f"DEBUG: Attempting AI analysis with model: {model_id}")
                response = await acompletion(model=model_id, messages=messages)
                content = response.choices[0].message.content
                print(f"DEBUG: Successfully used model: {model_id}")
                break
            except Exception as e:
                print(f"WARNING: Model {model_id} failed: {str(e)}")
                last_error = e
                await _asyncio.sleep(1)
        else:
            raise ValueError(f"All AI models failed. Last error: {last_error}")
    
    if content is None:
        raise ValueError("AI returned an empty response.")
        
    # Strip markdown formatting and extract JSON
    from json_repair import repair_json
    
    content = content.strip()
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()
    
    # Extract just the JSON object
    first_brace = content.find('{')
    last_brace = content.rfind('}')
    if first_brace != -1 and last_brace != -1:
        content = content[first_brace:last_brace + 1]
    
    # Repair and parse — handles control chars, trailing commas, comments, etc.
    repaired = repair_json(content)
    data = json.loads(repaired)
    
    return AIAnalysisResponse(**data)
