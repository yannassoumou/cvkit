# cvkit — AI-Powered CV Toolkit

> **One-step setup.** Tell your AI agent: "Read cvkit.md and set up my CV project."

---

## What is cvkit?

cvkit is a self-contained CV generation toolkit. Clone it, give your agent your CV, and it generates tailored ATS-friendly LaTeX CVs for every job offer. No coding, no templates to configure — the agent handles everything.

**What's included:**
- LaTeX template (ATS-friendly, navy blue, compact, 10pt)
- Agent instructions (AGENTS.md — read automatically by Claude Code, Cursor, etc.)
- Skills for Hermes agent (interactive workflow, auto-review, web scraping)
- Scripts for bulk generation and web dashboard
- Placeholder files ready for your data

---

## One-Command Setup

```bash
# Clone the toolkit
git clone https://github.com/yannassoumou/cvkit.git ~/cv
cd ~/cv

# Install LaTeX (required for PDF generation)
# Linux (Ubuntu/Debian):
sudo apt install -y texlive-latex-recommended texlive-lang-french poppler-utils
# macOS:
brew install --cask mactex && brew install poppler
# Fedora:
sudo dnf install -y texlive-scheme-medium texlive-babel-french poppler-utils

# Install Hermes skills (optional — for Hermes agent users only)
mkdir -p ~/.hermes/skills/
cp -r .agents/skills/* ~/.hermes/skills/

# Done. Tell your agent to read AGENTS.md and set up your CV.
```

**No GitHub repo?** The agent will `git init` locally. You can push to GitHub/GitLab later.

---

## What Your Agent Does

When you tell your agent "Set up my CV project":

0. **Sets up Git** — asks if you have a GitHub/GitLab repo; if not, `git init` locally
1. **Reads AGENTS.md** — understands the project structure and rules
2. **Asks for your CV** — paste as text or attach a PDF (agent extracts it)
3. **Writes CV_Master_texte.txt** — structured plain-text CV, the source of truth
4. **Updates the LaTeX template** — fills in your name, contact, links
5. **Creates Offers/ directory** — ready for job applications
6. **Confirms** — shows you what it extracted, lets you correct anything

Then you're ready:

> "I found this offer: [paste job description]"

The agent walks you through **interactive CV generation**:
- Header format review
- Profile tailored to the role (you approve or modify)
- Project selection (agent suggests, you pick)
- Cover letter (optional, same review process)
- Auto-review (checks for truncation, formatting issues)
- Commit locally (pushes to GitHub if remote is configured)

---

## Project Structure

```
~/cv/
├── AGENTS.md                    # Agent instructions (read this first)
├── cvkit.md                     # This file — setup guide
├── CV_Master_template.txt       # Reference format for your CV
├── CV_Master_texte.txt          # Your CV (created by the agent)
├── .gitignore
├── .agents/skills/              # Agent skill documentation
│   ├── cv-job-application-workflow/  # Full interactive workflow
│   ├── cv-review/                    # Automatic quality checks
│   └── camofox-browser/              # Web scraping (optional)
├── templates/
│   └── cv_template.tex          # LaTeX template (placeholders — agent fills in)
├── scripts/
│   ├── generate_all_latex_cvs.py     # Bulk CV generator
│   └── cv_web_server.py             # Web dashboard for browsing CVs
└── Offers/                      # Your adapted CVs (created by agent)
    └── README.md                # Application journal
```

---

## Agent-Agnostic

Works with any AI agent:

| Agent | How to start |
|---|---|
| **Hermes** | `cd ~/cv && hermes` |
| **Claude Code** | Open `~/cv` — reads AGENTS.md |
| **Cursor** | Open `~/cv` folder |
| **OpenCode** | Point to `~/cv` |
| **GitHub Copilot** | Open `~/cv` in VS Code |

---

## Requirements

- Python 3.10+
- LaTeX (pdflatex) — for PDF compilation
- poppler-utils (pdftotext, pdfinfo) — for CV review
- Git — for version control

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `pdflatex: command not found` | Run the LaTeX install command above |
| CV exceeds 2 pages | Cut less relevant projects, shorten bullet points |
| Section cut across pages | Agent adds `\needspace{15\baselineskip}` before PROJETS |
| Skills not loading (Hermes) | Run `cp -r .agents/skills/* ~/.hermes/skills/` and restart |

---

**Last Updated**: May 2026
