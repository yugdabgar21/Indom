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
    
    # Map projects — generate raw LaTeX (no custom commands)
    project_latex = ""
    for p in analysis.projects:
        name_str = escape_latex(p.name)
        if p.link and p.link.startswith("http"):
            link_str = f"\\hfill \\href{{{p.link}}}{{Link}}"
        else:
            link_str = ""
        desc_str = escape_latex(p.description)
        stack_str = escape_latex(p.stack)
        project_latex += (
            f"\\textbf{{{name_str}}} {link_str} \\\\\n"
            f"{desc_str} \\\\\n"
            f"\\textit{{Used:}} {stack_str} \\\\\n"
            f"\n\\vspace{{6pt}}\n\n"
        )
        
    # Map education — generate raw LaTeX
    edu_latex = ""
    for e in analysis.education:
        degree_str = escape_latex(e.degree)
        school_str = escape_latex(e.school)
        date_str = escape_latex(e.date_range)
        gpa_str = escape_latex(e.gpa)
        edu_latex += (
            f"\\textbf{{{degree_str}}} \\hfill {date_str} \\\\\n"
            f"{school_str} \\\\\n"
        )
        if gpa_str:
            edu_latex += f"GPA: {gpa_str} \\\\\n"
        edu_latex += "\n\\vspace{6pt}\n\n"
        
    # Map certifications
    if analysis.certifications and len(analysis.certifications) > 0:
        cert_latex = "\\begin{itemize}[leftmargin=*]\n"
        for c in analysis.certifications:
            cert_latex += f"  \\item {escape_latex(c)}\n"
        cert_latex += "\\end{itemize}\n"
    else:
        cert_latex = "None listed.\n"
        
    # Map languages
    lang_latex = ", ".join([escape_latex(l) for l in analysis.languages]) if analysis.languages else "English"

    # Build professional summary text
    professional_summary_text = escape_latex(analysis.professional_summary) if analysis.professional_summary else "Dedicated professional seeking to leverage skills and experience."

    replacements = {
        "{{PROJECTS_LIST}}": project_latex,
        "{{EDUCATION_LIST}}": edu_latex,
        "{{CERTIFICATIONS_LIST}}": cert_latex,
        "{{LANGUAGES_LIST}}": lang_latex,
        "{{PROFESSIONAL SUMMARY}}": professional_summary_text,
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
    
    print(f"DEBUG generate_latex: full_name='{analysis.full_name}', job_title='{analysis.job_title}', projects={len(analysis.projects)}")
    
    for key, val in replacements.items():
        tex = tex.replace(key, val)
    
    # Sanity check — warn if any tokens were NOT replaced
    import re as _re
    leftover = _re.findall(r'\{\{[A-Z_]+\}\}', tex)
    if leftover:
        print(f"WARNING: Unreplaced tokens in LaTeX output: {leftover}")
        
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

async def compile_pdf(latex_code: str) -> dict | bytes:
    """
    Compile LaTeX code to PDF. Returns PDF bytes on success.
    Raises Exception with full logs on failure.
    """
    import shutil
    import logging

    logger = logging.getLogger("latex_builder")

    pdflatex_cmd = find_pdflatex()

    # Verify pdflatex exists and is executable
    if not shutil.which(pdflatex_cmd) and not os.path.exists(pdflatex_cmd):
        raise RuntimeError(
            f"pdflatex not found at '{pdflatex_cmd}'. "
            "Please install MiKTeX (Windows) or TeX Live (Linux/macOS) and ensure it is in your PATH."
        )

    with tempfile.TemporaryDirectory() as temp_dir:
        tex_path = os.path.join(temp_dir, "cv.tex")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(latex_code)

        # Build the command with all non-interactive flags
        cmd = [
            pdflatex_cmd,
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            "cv.tex",
        ]

        # Prevent MiKTeX from trying to auto-install packages (this causes the hang)
        env = os.environ.copy()
        env["MIKTEX_ENABLEINSTALLER"] = "no"

        logger.info(f"Running: {' '.join(cmd)} in {temp_dir}")

        process = None
        stdout_str = ""
        stderr_str = ""

        try:
            process = subprocess.run(
                cmd,
                cwd=temp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=20,
                env=env,
            )
            stdout_str = process.stdout or ""
            stderr_str = process.stderr or ""
        except subprocess.TimeoutExpired as e:
            # Kill the process tree on timeout
            logger.error("pdflatex timed out after 20s — killed.")
            # e.stdout / e.stderr may be str (text=True) or bytes or None
            _tout = e.stdout if isinstance(e.stdout, str) else (e.stdout or b"").decode("utf-8", errors="ignore")
            _terr = e.stderr if isinstance(e.stderr, str) else (e.stderr or b"").decode("utf-8", errors="ignore")
            raise Exception(
                "PDF compilation timed out (20s). "
                "This usually means MiKTeX is trying to install a missing package. "
                "Pre-install required packages: geometry, enumitem, hyperref, titlesec.\n"
                f"stdout: {_tout[:500]}\n"
                f"stderr: {_terr[:500]}"
            )
        except FileNotFoundError:
            raise Exception(
                f"pdflatex executable not found at '{pdflatex_cmd}'. "
                "Ensure MiKTeX or TeX Live is installed and in your PATH."
            )
        except Exception as e:
            raise Exception(f"Failed to start LaTeX compiler: {str(e)}")

        # Fail fast: check return code immediately
        if process.returncode != 0:
            logger.error(f"pdflatex exited with code {process.returncode}")
            logger.error(f"STDOUT:\n{stdout_str[:1000]}")
            logger.error(f"STDERR:\n{stderr_str[:1000]}")

            # Extract common error patterns for user-friendly hints
            error_hint = ""
            if "article.cls" in stdout_str:
                error_hint = (
                    "\nHint: 'article.cls' not found. Run: "
                    "miktex-console --admin -> Packages -> Install 'base'"
                )
            elif "Undefined control sequence" in stdout_str:
                error_hint = "\nHint: LaTeX syntax error. Check your CV data for special characters."
            elif "File" in stdout_str and "not found" in stdout_str:
                error_hint = (
                    "\nHint: A required package/file is missing. "
                    "Pre-install packages: geometry, enumitem, hyperref, titlesec."
                )

            raise Exception(
                f"pdflatex failed (exit code {process.returncode}):\n"
                f"--- STDOUT (truncated) ---\n{stdout_str[:800]}\n"
                f"--- STDERR ---\n{stderr_str[:400]}\n"
                f"{error_hint}"
            )

        # Verify PDF was actually created
        pdf_path = os.path.join(temp_dir, "cv.pdf")
        if not os.path.exists(pdf_path):
            raise Exception(
                f"pdflatex exited with code 0 but no PDF was produced.\n"
                f"STDOUT: {stdout_str[:500]}\nSTDERR: {stderr_str[:500]}"
            )

        logger.info("PDF compiled successfully.")

        with open(pdf_path, "rb") as f:
            return f.read()