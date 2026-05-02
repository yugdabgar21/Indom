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
import re
import subprocess
import tempfile
import yaml
from app.models.schemas import CompileRequest

def load_template_path(template_name: str):
    """
    Safely resolves the template path with strict validation to prevent path traversal (CWE-22).
    """
    if not template_name:
        raise ValueError("Template name is required.")

    # 1. Strip extension if provided
    clean_name = template_name.replace(".tex", "")
    
    # 2. Strict Regex Validation: Only allow alphanumeric, underscores, and hyphens
    if not re.fullmatch(r"[A-Za-z0-9_\-]+", clean_name):
        raise ValueError(f"Invalid template name: '{template_name}'")
        
    # 3. Whitelist Check
    ALLOWED_TEMPLATES = {"classic", "modern", "template"}
    if clean_name not in ALLOWED_TEMPLATES:
        raise ValueError(f"Template '{clean_name}' is not in the allowed list")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up to the project root
    root_dir = os.path.abspath(os.path.join(current_dir, "../../../../"))
    
    # 4. Use realpath to resolve all symlinks and '..' segments
    templates_dir = os.path.realpath(os.path.join(root_dir, "templates"))
    filename = f"{clean_name}.tex"
    template_path = os.path.realpath(os.path.join(templates_dir, filename))

    # 5. Boundary Check: Ensure the resolved path is still inside the templates directory
    if not template_path.startswith(templates_dir):
        raise ValueError("Security Violation: Path traversal detected")
        
    # 6. Final Existence Check
    if not os.path.exists(template_path):
        raise ValueError(f"Template file '{filename}' not found on disk")
        
    return template_path

def escape_latex(text: str) -> str:
    # Basic LaTeX escape sequence handling
    escape_chars = {
        '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}', '\\': r'\textbackslash{}'
    }
    return ''.join(escape_chars.get(c, c) for c in text)

async def generate_latex(request: CompileRequest) -> str:
    template_path = load_template_path(request.template_name)
    with open(template_path, "r", encoding="utf-8") as f:
        tex = f.read()
    
    # Inject user cv data based on analysis
    analysis = request.analysis
    
    # Map projects
    project_latex = ""
    for p in analysis.projects:
        if p.link and p.link.startswith("http"):
            link_str = f"\\href{{{escape_latex(p.link)}}}{{Link}}"
        elif p.link:
            link_str = f"\\textcolor{{subtext}}{{{escape_latex(p.link)}}}"
        else:
            link_str = ""
        project_latex += f"\\projectentry\n  {{{escape_latex(p.name)}}}\n  {{{link_str}}}\n  {{{escape_latex(p.description)}}}\n  {{{escape_latex(p.stack)}}}\n\n"
        
    # Map education
    edu_latex = ""
    for e in analysis.education:
        edu_latex += f"\\eduentry\n  {{{escape_latex(e.degree)}}}\n  {{{escape_latex(e.school)}}}\n  {{{escape_latex(e.date_range)}}}\n  {{{escape_latex(e.gpa)}}}\n\n"
        
    # Map certifications
    if analysis.certifications and len(analysis.certifications) > 0:
        cert_latex = "\\begin{itemize}\n"
        for c in analysis.certifications:
            cert_latex += f"  \\item {escape_latex(c)}\n"
        cert_latex += "\\end{itemize}\n"
    else:
        cert_latex = ""
        
    # Map languages
    lang_latex = " \\quad\\textbullet\\quad ".join([escape_latex(l) for l in analysis.languages])

    replacements = {
        "{{PROJECTS_LIST}}": project_latex,
        "{{EDUCATION_LIST}}": edu_latex,
        "{{CERTIFICATIONS_LIST}}": cert_latex,
        "{{LANGUAGES_LIST}}": lang_latex,
        "{{FULL_NAME}}": escape_latex(analysis.full_name) if analysis.full_name else "User Name",
        "{{JOB_TITLE}}": escape_latex(analysis.job_title),
        "{{EMAIL}}": escape_latex(analysis.email) if analysis.email else "user@example.com",
        "{{PHONE}}": escape_latex(analysis.phone) if analysis.phone else "+1 234 567 890",
        "{{LOCATION}}": escape_latex(analysis.location) if analysis.location else "Remote",
        "{{GITHUB_USERNAME}}": escape_latex(analysis.github_username) if analysis.github_username else "githubuser",
        "{{SKILLS_TOOLS}}": escape_latex(analysis.skills_tools),
        "{{SKILLS_AUTOMATION}}": escape_latex(analysis.skills_automation),
        "{{SKILLS_AI_DEV}}": escape_latex(analysis.skills_ai_dev),
        "{{SKILLS_OTHER}}": escape_latex(analysis.skills_other),
    }
    
    for key, val in replacements.items():
        tex = tex.replace(key, val)
        
    return tex

def find_pdflatex():
    """Try to find pdflatex in system PATH or common MiKTeX install locations."""
    import shutil
    # 1. Try system PATH first (best for C: installs)
    path = shutil.which("pdflatex")
    if path:
        return path
        
    # 2. Try common Windows installation paths
    common_paths = [
        r"C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"),
    ]
    
    # 3. Add the project-local path as fallback
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, "../../../../"))
    common_paths.append(os.path.join(root_dir, "miktex", "miktex", "bin", "x64", "pdflatex.exe"))
    
    for p in common_paths:
        if os.path.exists(p):
            return p
            
    # Final fallback
    return "pdflatex"

async def compile_pdf(latex_code: str) -> bytes:
    pdflatex_cmd = find_pdflatex()
    with tempfile.TemporaryDirectory() as temp_dir:
        tex_path = os.path.join(temp_dir, "cv.tex")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(latex_code)
            
        process = subprocess.run(
            [pdflatex_cmd, "-interaction=nonstopmode", "cv.tex"],
            cwd=temp_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        pdf_path = os.path.join(temp_dir, "cv.pdf")
        if not os.path.exists(pdf_path):
            stdout_str = process.stdout.decode('utf-8', errors='ignore')
            stderr_str = process.stderr.decode('utf-8', errors='ignore')
            raise Exception(f"Failed to compile LaTeX using '{pdflatex_cmd}':\n{stdout_str}\n{stderr_str}")
            
        with open(pdf_path, "rb") as f:
            return f.read()