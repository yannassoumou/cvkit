# cvkit — Bootstrap Guide for AI Agents

> **Read this file first.** This is the single source of truth for setting up cvkit.
> AI agents should execute every step automatically.

> **⚠️ Note for Agents**: This file uses `<ROOT_PROJECT>` as a placeholder for the project root directory. Replace it with the actual path when executing commands.

---

## 🎯 What is cvkit?

cvkit is an AI-powered toolkit for generating tailored, ATS-compatible CVs and cover letters using LaTeX templates and agent workflows. No coding required — just tell the agent what you want.

**Project Location**: `<ROOT_PROJECT>`

---

## 📋 Setup Steps (Execute All)

### 1. Clone the Repository

```bash
cd <ROOT_PROJECT>
git clone https://github.com/YOUR_USERNAME/cvkit.git
cd cvkit
```

### 2. Install System Dependencies

#### Python 3.10+
```bash
python3 --version
# Expected: Python 3.10 or higher
```

#### LaTeX Compiler (Required for PDF generation)

**macOS:**
```bash
brew install --cask mactex
# Or use MacTeX: https://www.tug.org/mactex/
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install -y texlive-latex-recommended texlive-fonts-recommended texlive-xetex texlive-lang-french
```

**Windows:**
```bash
# Install MiKTeX: https://miktex.org/download
```

**Verify LaTeX installation:**
```bash
pdflatex --version
```

#### Camofox Browser (Optional but recommended for web scraping)

Camofox is a Firefox fork with fingerprint spoofing for anti-detection browsing.

**macOS:**
```bash
brew install --cask camofox
```

**Linux:**
```bash
# Download from: https://github.com/brave/camofox
```

### 3. Pull Skills from skills-cv Repository

> **⚠️ Requirement**: `skills-cv` must be accessible for this step to work.

```bash
# Pull skills into .agents/skills/
git subtree pull --prefix=.agents/skills https://github.com/yannassoumou/skills-cv.git main --allow-unrelated-histories
```

**If the repository is private**, use SSH:
```bash
git subtree pull --prefix=.agents/skills git@github.com:yannassoumou/skills-cv.git main --allow-unrelated-histories
```

**Verify skills are installed:**
```bash
ls -la .agents/skills/
# Expected: camofox-browser/ cv-job-application-workflow/
```

### 4. Recreate Folder Structure

Ensure this structure exists:

```
cvkit/
├── CV_Master_texte.txt          # 🔲 USER PROVIDES (your CV in markdown format)
├── CV_Master_template.txt       # ✅ PROVIDED (template with placeholders)
├── config.yaml                  # 🔲 USER PROVIDES (create from template below)
├── config.template.yaml         # ✅ PROVIDED (configuration template)
├── scripts/                     # ✅ PROVIDED (generation scripts)
│   ├── generate_cv_page_budget.py
│   ├── generate_all_latex_cvs.py
│   └── ...
├── templates/                   # ✅ PROVIDED (LaTeX templates)
│   ├── latex_cv_template.tex
│   └── delescen/
├── Offers/                      # 🔲 CREATED ON FIRST JOB APPLICATION
│   └── offer1_company_role/
│       ├── CV_Company_Role.pdf
│       ├── Lettre_Motivation.pdf
│       ├── offre_data.md
│       └── README.md
├── archive/                     # 🔲 CREATED ON CV UPDATE
├── .agents/skills/              # 🔲 PULLED FROM skills-cv (Step 3)
├── .private/                    # ✅ PROVIDED (private features)
├── cvkit.md                     # ✅ PROVIDED (this file)
├── README.md                    # ✅ PROVIDED (public documentation)
└── QWEN.md                      # 🔲 CREATED BY AGENT (private configuration)
```

**Create missing directories:**
```bash
mkdir -p Offers/ archive/
```

### 5. Create config.yaml

```bash
cp config.template.yaml config.yaml
```

**Agent prompts the user to fill in:**
- Full name
- Email
- Phone
- LinkedIn URL
- GitHub URL
- Address

**config.yaml content:**
```yaml
# cvkit Configuration
# Copy this file from config.template.yaml and fill in your details

defaults:
  template: "delescin"        # standard | delescin
  mode: "compact"             # full | compact | ultra
  output_dir: "Offers/"
  max_pages: 1

contact:
  name: "[YOUR_FULL_NAME]"
  email: "[your.email@example.com]"
  phone: "[+XX XXX XXX XXXX]"
  linkedin: "[linkedin.com/in/yourprofile]"
  github: "[github.com/yourusername]"
  address: "[Your Address, Postal Code City, Country]"

latex:
  compiler: "pdflatex"
  extra_packages:
    - "hyperref"
    - "xcolor"
    - "geometry"

git:
  remote_public: "cvkit"
  remote_private: "origin"
  branch: "main"

agent:
  preferred_model: "qwen"
  auto_commit: true
  auto_push: true
```

### 6. User Provides Their CV

**Agent tells the user:**
> "Please place your CV in the root directory as `CV_Master_texte.txt`.
> You can use `CV_Master_template.txt` as a reference for the format."

**Required CV Format:**
```
[YOUR_NAME]
[Job Title]
----------------------------------------

COORDONNÉES
-----------
📍 [Your Address]
📞 [Your Phone]
📧 [Your Email]
💼 [LinkedIn URL]
🔗 [GitHub URL]

PROFIL
------
[2-3 line professional summary]

EXPÉRIENCES PROFESSIONNELLES
-----------------------------
[Job Title] | [Company]
[Date] - [Present/End Date]
• [Achievement 1]
• [Achievement 2]
• [Achievement 3]

[Job Title] | [Company]
[Date] - [Present/End Date]
• [Achievement 1]
• [Achievement 2]

PROJET PERSONNEL
----------------
[Project Name]
[Role] | [Date] - [Present/End Date]
• [Project description]
• [Technologies used]

CERTIFICATIONS
--------------
[Certification Name]
[Issuer] | [Date]
• [Relevant details]

COMPÉTENCES TECHNIQUES
----------------------
[Category]:
• [Skill 1]
• [Skill 2]

[Category]:
• [Skill 1]
• [Skill 2]

COMPÉTENCES TRANSVERSALES
-------------------------
• [Skill 1]
• [Skill 2]
```

**Agent validates the CV:**
- ✅ Checks that all required sections are present
- ✅ Verifies contact information is filled in
- ✅ Confirms formatting uses correct section headers

### 7. Create QWEN.md (Private Configuration)

**Agent creates `QWEN.md`** based on the user's config.yaml and CV. This file:
- Contains the user's personal information (private)
- Documents the full workflow for the agent
- Includes Golden Rules for the project
- Lists available agent skills with triggers

**QWEN.md should include:**
- Project overview
- Golden Rules (workflow standards)
- Agent skills documentation
- Common commands
- Theme & design system
- ATS compliance rules

### 8. Ready to Use!

**Agent tells the user:**
> "cvkit is ready! You can now use natural language to generate CVs and cover letters.
>
> Try these prompts:
> - 'Generate a CV for [Company] [Position] using the delescin template'
> - 'Create a cover letter for [Company] [Position]'
> - 'Update my CV with new experience at [Company]'
> - 'Extract details from this job offer: [paste offer or URL]'"

---

## 📚 Agent Skills Documentation

The `.agents/skills/` directory contains comprehensive documentation for AI agents:

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| **camofox-browser** | Anti-detection browser server for web scraping | Extracting job offers from LinkedIn, bypassing bot detection |
| **cv-job-application-workflow** | Full pipeline: extract → adapt → generate | When you receive a job offer |
| **cv-source-update** | Update master CV with new info | When you get a new job/certification |
| **cv-improvement-workflow** | Design & ATS optimization | When you want to improve CV quality |
| **cv-creation-from-scratch** | Build CV without existing source | When starting from zero |
| **cv-job-matching** | Match CV to job requirements | When evaluating job fit |
| **cv-adaptation** | Role-specific customization | When adapting for specific role |

Each skill includes:
- Trigger conditions (when to use)
- Step-by-step workflow
- Code examples
- Common pitfalls to avoid

---

## 🎨 Theme & Design System

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| **Primary Blue** | `#003366` | Standard template headers, name |
| **Modern Green** | `#228B22` | Delescin template name |
| **Secondary Gray** | `#808080` | Contact info, subtle elements |
| **Text Black** | `#000000` | Body text |

### Typography

- **Font Family**: Calibri (primary), Montserrat Alternates (headers)
- **Font Sizes**: 11pt (full), 10pt (compact), 9pt (ultra)
- **Line Height**: 1.15 (compact), 1.25 (full)

### Template Styles

| Template | Style | Best For |
|----------|-------|----------|
| **Standard** | Blue header, centered name, traditional layout | Traditional companies, Google-compliant |
| **Delescin** | Green name, right-aligned contacts, modern spacing | Tech companies, modern startups |

### ATS Compliance Rules

All generated CVs follow these rules:

- ✅ Single-column layout only
- ✅ Standard section headings (PROFIL, EXPÉRIENCES, etc.)
- ✅ No tables, columns, or graphics
- ✅ Text-based content only (no images)
- ✅ Standard fonts (Calibri)
- ✅ High contrast text (black on white)
- ✅ Clear, professional filenames

---

## 🚀 Common Commands

### Agent-First (Natural Language)

```
Agent prompts you can use:
- "Adapt my CV for [job title] at [company]"
- "Generate a cover letter for [company] [position]"
- "Update my CV with: [new experience details]"
- "Extract job details from: [URL or pasted text]"
- "Create a compact version of my CV"
- "Show me my application history"
```

### CLI (For Developers)

```bash
# Generate a CV with page budget control
python3 scripts/generate_cv_page_budget.py \
  --master CV_Master_texte.txt \
  --template delescin \
  --mode compact \
  --output-dir Offers/offer1_company/

# Batch generate all CVs
python3 scripts/generate_all_latex_cvs.py

# Manual LaTeX compilation
pdflatex -output-directory=Offers/offer1_company/ \
  Offers/offer1_company/CV_Company_Role.tex

# Check PDF page count
pdfinfo Offers/offer1_company/CV_Company_Role.pdf | grep Pages
```

---

## 📖 Git Workflow

### Sync Both Repos

```bash
# Push to both public (cvkit) and private (cv)
git push cvkit main && git push origin main
```

### Push Private Only

```bash
# For job applications (contains personal data)
git add Offers/ && git commit -m "add new offer"
git push origin main
```

### Push Public Only

```bash
# For skill updates (sanitized changes)
git add .agents/ && git commit -m "update skill docs"
git push cvkit main
git push origin main
```

---

## 🆘 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| LaTeX compilation fails | Install TeX Live: `brew install --cask mactex` (macOS) or `sudo apt install texlive-latex-recommended` (Linux) |
| `pdflatex` command not found | Add TeX Live to PATH (adjust year/arch): `export PATH=$PATH:/usr/local/texlive/YYYY/bin/ARCH` |
| CV exceeds 1 page | Use `mode="compact"` or `mode="ultra"` |
| Agent doesn't recognize CV | Ensure `CV_Master_texte.txt` is in root directory |
| Template not found | Check `templates/` directory exists |
| Offers/ folder not created | Agent should create it automatically on first use |
| Skills pull fails | Ensure skills-cv repo is accessible: `git subtree pull --prefix=.agents/skills https://github.com/yannassoumou/skills-cv.git main` |
| Git subtree error | Try: `git subtree add --prefix=.agents/skills https://github.com/yannassoumou/skills-cv.git main --squash` |

### Verification Checklist

Run these commands to verify setup:

```bash
# Python version
python3 --version

# LaTeX installation
pdflatex --version

# Skills directory exists
ls -la .agents/skills/

# Template files exist
ls -la templates/

# Directories created
ls -la Offers/ archive/
```

---

## 📋 Agent Setup Checklist

When an agent reads this file, it should:

- [ ] Clone repo and cd into directory
- [ ] Verify Python 3.10+ is installed (`python3 --version`)
- [ ] Verify LaTeX is installed (`pdflatex --version`)
- [ ] Pull skills from skills-cv repository
- [ ] Create `Offers/` and `archive/` directories if missing
- [ ] Copy `config.template.yaml` to `config.yaml`
- [ ] Prompt user to fill in `config.yaml`
- [ ] Prompt user to provide `CV_Master_texte.txt`
- [ ] Validate CV format and sections
- [ ] Create `QWEN.md` with user's configuration
- [ ] Confirm setup is complete and suggest first prompts

---

## 📝 Notes for AI Agents

1. **Never expose personal data** in public repos (cvkit)
2. **Always ask the user** for template preference (standard or delescin)
3. **Use compact mode by default** to keep CVs to 1 page
4. **Archive old CV versions** before overwriting `CV_Master_texte.txt`
5. **Use production-ready language**: "RAG system" not "POC RAG"
6. **Commit after every major change** to both repos
7. **Validate CV format** before generating PDFs
8. **Prompt user for job offer details** if not provided
9. **Create QWEN.md** with user's configuration after setup
10. **Use absolute paths** (e.g., `<ROOT_PROJECT>/`) for reliability

---

## 🎯 First-Use Prompts

After setup is complete, suggest these prompts to the user:

```
"Generate a CV for Google Data Scientist using the delescin template"
"Create a cover letter for Microsoft AI Engineer position"
"Extract job details from: [paste job offer URL]"
"Update my CV with new experience at [Company]"
"Create a compact version of my CV for [Company]"
"Show me my application history in Offers/"
```

---

## 📄 End of cvkit.md

This file is the single source of truth. If something is unclear, update this file first.

**Last Updated**: April 2026
**Project Location**: `<ROOT_PROJECT>`
