#!/usr/bin/env python3
"""
Bulk CV Generator — reads all offre_data.md files and generates tailored LaTeX CVs.
Reads the canonical template (filled in during setup), modifies only the role title
and profile paragraph per offer. All personal data comes from the template.
ROBUST: simple parsing, no external deps, works with any model.
Usage: python3 scripts/generate_all_latex_cvs.py [--compile] [--offer offer_dir_name]
"""
import os, re, subprocess, sys
from datetime import datetime

CV_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Project root
OFFERS_DIR = os.path.join(CV_DIR, "Offers")
TEMPLATE_PATH = os.path.join(CV_DIR, "templates", "cv_template.tex")


# ── Template reader ───────────────────────────────────────
def get_preamble():
    """Read the canonical template preamble (everything before \\begin{document})"""
    with open(TEMPLATE_PATH) as f:
        content = f.read()
    # Use rfind to get the LAST \\begin{document} (avoids matching the one in the comment)
    end = content.rfind("\\begin{document}")
    if end == -1:
        raise ValueError("Template missing \\begin{document}")
    return content[:end] + "\\begin{document}\n"


def get_template_body():
    """Extract the body from \\begin{document} to \\end{document} (exclusive)"""
    with open(TEMPLATE_PATH) as f:
        content = f.read()
    start = content.rfind("\\begin{document}")  # rfind to skip the one in the comment
    end = content.rfind("\\end{document}")
    if start == -1 or end == -1:
        raise ValueError("Template missing \\begin{document} or \\end{document}")
    return content[start + len("\\begin{document}"):end]


# ── Offer Data Parser ──────────────────────────────────────
def parse_offre_data(filepath):
    """Parse offre_data.md and extract structured fields.
    Returns dict with: company, role, date, focus, location, contract, url
    """
    if not os.path.exists(filepath):
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    data = {
        "company": "",
        "role": "",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "focus": "",
        "location": "",
        "contract": "",
        "url": "",
    }

    # Simple regex extraction — no heavy parsing
    patterns = {
        "company": [r'\*\*Entreprise\s*:?\*\*\s*(.+)', r'\*\*Company\*\*:?\s*(.+)', r'\|\s*\*\*Company\*\*\s*\|\s*(.+?)\s*\|'],
        "role": [r'\*\*Poste\s*:?\*\*\s*(.+)', r'\*\*Position\*\*:?\s*(.+)', r'\|\s*\*\*Position\*\*\s*\|\s*(.+?)\s*\|'],
        "location": [r'\*\*Lieu\s*:?\*\*\s*(.+)', r'\*\*Location\*\*:?\s*(.+)', r'\|\s*\*\*Location\*\*\s*\|\s*(.+?)\s*\|'],
        "contract": [r'\*\*Contrat\s*:?\*\*\s*(.+)', r'\*\*Contract\*\*:?\s*(.+)'],
        "url": [r'\((https?://[^\s\)]+)\)', r'https?://[^\s\)]+jobs[^\s\)]+'],
    }

    for field, pats in patterns.items():
        for pat in pats:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                data[field] = m.group(1).strip() if m.lastindex else m.group(0).strip()
                break

    # Strip markdown table formatting, parentheticals, and whitespace
    for field in ["company", "role", "location"]:
        val = data[field]
        val = re.sub(r'\s*\([^)]*\)', '', val)
        val = val.strip().strip("|").strip()
        if val.startswith("|"):
            val = val[1:]
        if val.endswith("|"):
            val = val[:-1]
        val = val.strip()
        data[field] = val

    # Detect focus keywords from the offer text
    if not data["focus"]:
        keywords = text.lower()
        if "agent" in keywords and "rag" in keywords:
            data["focus"] = "agentic AI RAG LLM"
        elif "rag" in keywords:
            data["focus"] = "RAG LLM Python"
        elif "voice" in keywords or "tts" in keywords:
            data["focus"] = "voice AI TTS"
        elif "ml" in keywords or "machine learning" in keywords:
            data["focus"] = "ML infrastructure"
        elif "data" in keywords:
            data["focus"] = "data AI engineering"
        elif "genai" in keywords or "gen ai" in keywords:
            data["focus"] = "GenAI Python LLM"
        else:
            data["focus"] = "AI engineering Python"

    return data


# ── LaTeX Generator ────────────────────────────────────────
def esc(text):
    """Escape LaTeX special characters"""
    for old, new in [("&", "\\&"), ("%", "\\%"), ("$", "\\$"), ("#", "\\#"),
                      ("_", "\\_"), ("{", "\\{"), ("}", "\\}"),
                      ("~", "\\textasciitilde"), ("^", "\\textasciicircum")]:
        text = text.replace(old, new)
    return text


def build_cv(offer):
    """Generate a complete LaTeX CV string from offer data.
    
    Reads the canonical template (filled in during setup) and only modifies:
    1. The role title in the header
    2. The profile paragraph (tailored to the offer's focus)
    
    All other content (name, contact, skills, experiences, projects, etc.)
    comes directly from the user's template — no hardcoded personal data.
    """
    role = esc(offer.get("role", "AI Engineer"))
    focus = offer.get("focus", "AI engineering")

    # ── Smart profile based on offer focus keywords ──────────
    # These are generic sentence templates — no personal data.
    # Keep them SHORT (1-2 lines) to avoid page overflow.
    profiles = {
        "agentic": (
            "Expert en agents IA autonomes (LangGraph, CrewAI, AutoGen), "
            "RAG avanc\\'e et Model Context Protocol. J\\'ai con\\c{c}u et d\\'eploy\\'e "
            "des pipelines agentiques de l\\'exp\\'erimentation \\`a la production."
        ),
        "voice": (
            "Expert en synth\\`ese vocale temps r\\'eel, agents IA autonomes "
            "et RAG avanc\\'e. J\\'ai con\\c{c}u des pipelines TTS optimis\\'es pour la production."
        ),
        "ml": (
            "Sp\\'ecialis\\'e en infrastructure ML et d\\'eploiement de LLMs \\`a grande \\'echelle. "
            "J\\'ai con\\c{c}u et maintenu des syst\\`emes de serving haute performance en production."
        ),
        "data": (
            "Expert en RAG avanc\\'e, agents IA autonomes et pipelines de donn\\'ees. "
            "J\\'ai d\\'eploy\\'e des syst\\`emes complets d\\^'analyse en production."
        ),
        "genai": (
            "Sp\\'ecialis\\'e en IA g\\'en\\'erative, LLMs et RAG avanc\\'e. "
            "J\\'ai con\\c{c}u et d\\'eploy\\'e des syst\\`emes IA de bout en bout."
        ),
    }

    # Pick the profile that matches the focus
    profile = profiles.get("ml", profiles["data"])  # Default: data
    for key, text in profiles.items():
        if key in focus.lower():
            profile = text
            break

    # ── Read template body ──────────────────────────────────
    preamble = get_preamble()
    body = get_template_body()

    # ── 1. Replace role title in header ─────────────────────
    # Pattern: {\large\color{secondary} ...}
    body = re.sub(
        r'(\{\\large\\color\{secondary\}\s*)(.*?)(\s*\})',
        r'\1' + role + r'\3',
        body,
        count=1
    )

    # ── 2. Replace profile paragraph ────────────────────────
    # Index-based: find \cvsection{PROFIL}, skip to profile text,
    # find next \cvsection{, replace content between them.
    prof_marker = '\\cvsection{PROFIL}'
    prof_idx = body.index(prof_marker)
    # Skip past \cvsection{PROFIL}\n and the blank line to reach the profile text
    content_start = body.index('\n\n', prof_idx) + 2
    # Find the next \cvsection{ after the profile text
    next_section_idx = body.index('\\cvsection{', content_start)
    # Find the \n\n that precedes the next section (before the comment line)
    before_next = body.rfind('\n\n', content_start, next_section_idx)
    if before_next == -1:
        before_next = next_section_idx

    body = body[:content_start] + profile + body[before_next:]

    return preamble + body + "\n\\end{document}\n"


# ── Main ────────────────────────────────────────────────────
def compile_tex(tex_path):
    """Compile LaTeX to PDF and return True if successful"""
    offer_dir = os.path.dirname(tex_path)
    tex_name = os.path.basename(tex_path)
    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_name],
            cwd=offer_dir, capture_output=True, timeout=60
        )
        pdf_name = tex_name.replace(".tex", ".pdf")
        pdf_path = os.path.join(offer_dir, pdf_name)
        success = os.path.exists(pdf_path)
        # Clean aux files
        for ext in [".aux", ".log", ".out"]:
            aux = os.path.join(offer_dir, tex_name.replace(".tex", ext))
            if os.path.exists(aux):
                os.remove(aux)
        return success
    except Exception as e:
        print(f"  Compile error: {e}")
        return False


def main():
    compile_flag = "--compile" in sys.argv

    # Allow targeting a single offer
    target = None
    for i, arg in enumerate(sys.argv):
        if arg.startswith("--offer="):
            target = arg.split("=", 1)[1]
        elif arg == "--offer" and i + 1 < len(sys.argv):
            target = sys.argv[i + 1]

    if not os.path.exists(TEMPLATE_PATH):
        print(f"ERROR: Template not found: {TEMPLATE_PATH}")
        print("Did you complete setup? Run the agent first to fill in the template.")
        sys.exit(1)

    # Verify template has been filled in (no placeholders)
    with open(TEMPLATE_PATH) as f:
        template_content = f.read()
    if "[YOUR" in template_content:
        print("ERROR: Template still has [YOUR ...] placeholders.")
        print("Did you complete setup? Run the agent first to fill in the template.")
        sys.exit(1)

    if not os.path.exists(OFFERS_DIR):
        print(f"Offers directory not found: {OFFERS_DIR}")
        print("Creating Offsers/ directory...")
        os.makedirs(OFFERS_DIR, exist_ok=True)
        with open(os.path.join(OFFERS_DIR, "README.md"), "w") as f:
            f.write("# Offers Directory\n")

    # Scan all offer directories
    offers = []
    for entry in sorted(os.listdir(OFFERS_DIR)):
        offer_dir = os.path.join(OFFERS_DIR, entry)
        if not os.path.isdir(offer_dir):
            continue
        data_path = os.path.join(offer_dir, "offre_data.md")
        if not os.path.exists(data_path):
            continue
        if target and entry != target:
            continue
        data = parse_offre_data(data_path)
        if data and data["company"]:
            data["key"] = entry
            offers.append(data)

    if not offers:
        print("No offers found with offre_data.md")
        sys.exit(1)

    print(f"Found {len(offers)} offer(s) with data")
    print()

    generated = 0
    for offer in offers:
        key = offer["key"]
        company_slug = re.sub(r"[^a-zA-Z0-9]", "_", offer["company"])[:30]
        role_slug = re.sub(r"[^a-zA-Z0-9]", "_", offer["role"])[:30]
        # Clean up: remove double underscores, trailing underscores
        company_slug = re.sub(r"_+", "_", company_slug).strip("_")
        role_slug = re.sub(r"_+", "_", role_slug).strip("_")
        if not company_slug:
            company_slug = "Company"
        if not role_slug:
            role_slug = "Role"
        tex_name = f"CV_{company_slug}_{role_slug}_{offer['date']}.tex"
        tex_path = os.path.join(OFFERS_DIR, key, tex_name)

        # Generate
        print(f"Generating: {key} ({offer['company']} — {offer['role']})")
        print(f"  Focus: {offer['focus']}")
        try:
            latex = build_cv(offer)
            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(latex)
            print(f"  -> {tex_name}")

            if compile_flag:
                ok = compile_tex(tex_path)
                print(f"  PDF: {'OK' if ok else 'FAIL'}")
                if ok:
                    # Clean old PDFs
                    pdf_name = tex_name.replace(".tex", ".pdf")
                    for old in os.listdir(os.path.join(OFFERS_DIR, key)):
                        if old.endswith(".pdf") and old != pdf_name:
                            os.remove(os.path.join(OFFERS_DIR, key, old))
                            print(f"  Removed old: {old}")
                    generated += 1
            else:
                generated += 1
        except Exception as e:
            print(f"  ERROR: {e}")
        print()

    print(f"Done. {generated}/{len(offers)} generated.")


if __name__ == "__main__":
    main()
