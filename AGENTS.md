# AGENTS.md — CV Project Instructions

> This file is read automatically by AI agents (Claude Code, Cursor, OpenCode, Copilot, Hermes).
> It tells the agent what this project is, how it works, and what to do.

---

## ⚠️ FIRST THING YOU MUST DO — MANDATORY SETUP

**If `CV_Master_texte.txt` does not exist or `templates/cv_template.tex` contains `[YOUR` placeholders, you MUST complete setup before ANY other action.**

### Step 0: Git repository

> "Do you have a GitHub or GitLab repository for your CV project?
> - Yes → give me the URL and I'll clone it
> - No → I'll set up a local Git repo for you (you can push it online later)"

**If the user provides a repo URL:**
```bash
git clone <url> .
# Check if setup is already done — if CV_Master_texte.txt exists and template has no [YOUR] placeholders, skip to Step 5
```

**If the user has NO repo:**
```bash
git init
# Create .gitignore if it doesn't exist:
cat > .gitignore << 'EOF'
*.aux
*.log
*.out
*.pdf
__pycache__/
EOF
git add -A && git commit -m "Initial cvkit setup"
```
Then tell the user: "Your CV project is tracked locally with Git. When you're ready to push online, create a repo on GitHub/GitLab and run `git remote add origin <url>` — I'll handle the rest."

**IMPORTANT:** Only proceed to Step 1 if setup is NOT already done (template still has `[YOUR` placeholders).

### Step 1: Ask for the user's CV

> "To set up your CV project, I need your CV. You can:
> - Paste it as text (from LinkedIn, existing PDF, Word doc...)
> - Attach a PDF and I'll extract the text"

### Step 2: Extract and structure

If PDF: run `pdftotext -layout thefile.pdf -` and parse the output.

Structure the extracted text into `CV_Master_texte.txt` using this EXACT format:

```
FULL NAME
Job Title
----

COORDONNÉES
-----------
Address
Phone
Email
LinkedIn URL
GitHub URL

PROFIL
------
2-3 line professional summary (will be rewritten per offer in first person)

EXPÉRIENCES PROFESSIONNELLES
-----------------------------
Title | Company
Dates
• Achievement
• Achievement

PROJETS PERSONNELS
------------------
Project Name — Description
Role | Date
• Detail
• Stack: technologies

CERTIFICATIONS
--------------
Name | Issuer | Date
• Details

COMPÉTENCES TECHNIQUES
----------------------
Category:
Skills

COMPÉTENCES TRANSVERSALES
-------------------------
• Skill

FORMATION
---------
Degree
Institution | Dates

LANGUES
-------
• Language : Level
```

### Step 3: Replace placeholders in the LaTeX template

Open `templates/cv_template.tex`. Find ALL `[YOUR ...]` placeholders and replace them:

| Placeholder | Replace with |
|---|---|
| `[YOUR FULL NAME]` | User's full name |
| `[YOUR JOB TITLE]` | Current job title |
| `[YOUR ADDRESS]` | Full address |
| `[YOUR PHONE]` | Phone number |
| `[YOUR EMAIL]` | Email address |
| `[YOUR LINKEDIN URL]` | Full LinkedIn URL (https://...) |
| `[YOUR LINKEDIN DISPLAY]` | Short LinkedIn handle (linkedin.com/in/...) |
| `[YOUR GITHUB URL]` | Full GitHub URL (https://...) |
| `[YOUR GITHUB DISPLAY]` | Short GitHub handle (github.com/...) |

Also replace the placeholder sections (profile, skills, experiences, projects, etc.) with the user's ACTUAL content from CV_Master_texte.txt. Keep the LaTeX structure but fill in real data.

### Step 4: Create the Offers directory

```bash
mkdir -p Offers/
echo "# Offers Directory" > Offers/README.md
```

### Step 5: Confirm with the user

Show the user:
- The extracted CV_Master_texte.txt content
- The updated template header
- Ask: "Does this look correct? I can fix anything before we proceed."

**DO NOT skip setup. DO NOT generate a CV before setup is complete.**

---

## After Setup: When the User Shares a Job Offer

**Interactive workflow** — do NOT auto-generate. Follow these steps:

### Step 1: Extract offer details
Parse: company name, job title, location, contract type, key requirements, tech stack.

### Step 2: Header review
Show the header format (name, title, address, phone, email, links — each on its own line, never compressed with `$|$`):
```
MARC DUBOIS
Senior Data Engineer
14 rue de la République, 75011 Paris, France
+33 6 12 34 56 78
marc.dubois@email.com
linkedin...  |  github...
```
Ask user to approve.

### Step 3: Profile review
Draft a 3-5 line profile in FIRST PERSON "je" (NOT "A conçu" — use "J'ai conçu").
Tailor to the offer's keywords and industry. Ask user to approve or modify.

### Step 4: Project selection
List ALL projects from `CV_Master_texte.txt` (excluding prototypes: llama-tracker, experimental).
Sort by relevance to this offer. Add a 1-line rationale for each.
Ask user to select 2-4. Confirm final list.

### Step 5: Cover letter (optional)
Ask if they want a cover letter. If yes: 4 paragraphs (motivation, experience, achievements, call to action). Same review process.

### Step 6: Generate LaTeX
Copy the preamble from `templates/cv_template.tex` (everything before `\begin{document}`).
Fill in with tailored content from steps 2-5.
**Add `\needspace{15\baselineskip}` before `\cvsection{PROJETS PERSONNELS}`**.
Save to `Offers/offerN_[company]_[role]/CV_[Company]_[Role]_[Date].tex`.

### Step 7: Compile
```bash
cd Offers/offerN_[company]_[role]/
pdflatex -interaction=nonstopmode CV_*.tex
rm -f *.aux *.log *.out
```

### Step 8: Review (mandatory)
- `pdftotext -layout CV_*.pdf - | grep -B1 $'\f' | grep "PROJETS\|COMPÉTENCES\|EXPÉRIENCES"` — if match, section truncated → fix with larger needspace
- `pdfinfo CV_*.pdf | grep Pages` — must be 1-2 pages
- `grep -c "A conçu\|A développé" CV_*.tex` — if >0, third person → fix
- Fix and recompile if needed

### Step 9: Save offer data
Create `offre_data.md` in the offer directory.

### Step 10: Commit and push
```bash
git add -A && git commit -m "Add CV for [Company] — [Role]"
```
Then try to push:
```bash
git push 2>/dev/null || echo "No remote configured — commit saved locally."
```
If push fails, remind the user: "Commit saved locally. To push online: create a repo on GitHub and run `git remote add origin <url> && git push -u origin main`."

---

## Golden Rules

1. **FIRST: complete setup** — do not skip the mandatory setup above
2. **Profile in first person "je"** — always
3. **No frontend skills** (React, Material-UI, Tailwind) for AI/Data roles
4. **No prototypes** — exclude llama-tracker and experimental projects
5. **Section order**: Profil → Compétences → Expériences → Projets → Certifications → Formation → Langues
6. **`\needspace{15\baselineskip}`** before PROJETS PERSONNELS
7. **`\needspace{3\baselineskip}`** in all `\cvsection`, `\cvsubsection`, `\cvsubsubsection`
8. **1-2 pages max** — cut content if needed
9. **Header format**: each element on its own line, never `$|$` compressed
10. **Commit after every generation** — always commit even without a remote
11. **Push gracefully**: try `git push`, if no remote configured → remind user they can add one later (never fail silently, never block on push)

---

## File Naming

```
Offers/offerN_[company_slug]_[role_slug]/
├── offre_data.md
├── CV_[Company]_[Role]_[Date].tex
├── CV_[Company]_[Role]_[Date].pdf
└── Lettre_Motivation_[Company]_[Date].tex/pdf (optional)
```

Clean slugs: no special chars, max 80 chars, no double underscores.

---

## Tools

- `pdflatex` — compile LaTeX to PDF
- `pdftotext` — extract text from PDF
- `pdfinfo` — check page count
- `scripts/generate_all_latex_cvs.py` — bulk regenerate all CVs
- `scripts/cv_web_server.py` — web dashboard

---

## Quick Fixes

| Issue | Fix |
|-------|-----|
| Setup not done | Complete the mandatory setup at top of this file |
| Section orphaned at page bottom | `\needspace{15\baselineskip}` before the `\cvsection` |
| CV 3+ pages | Remove 1-2 projects, shorten bullets |
| Third person | Replace "A conçu" → "J'ai conçu" |
| Frontend skills visible | Delete Material-UI/Tailwind/React lines |
| PDF won't compile | Check unescaped `&`, `%`, `$`, `#` in LaTeX |
