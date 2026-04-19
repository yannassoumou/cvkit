# cvkit — One-Line Setup for AI Agents

> **Read this file first.** This is the single source of truth for setting up cvkit.

---

## 🚀 One-Line Installation

### For AI Agents (via curl)

```bash
curl -fsSL https://raw.githubusercontent.com/yannassoumou/cvkit/refs/heads/main/cvkit.md
```

This command fetches and displays the complete setup documentation.

### For Humans (Interactive Setup)

Open this file in your browser: [cvkit.md on GitHub](https://github.com/yannassoumou/cvkit/blob/main/cvkit.md)

---

## 🎯 What is cvkit?

cvkit is an AI-powered toolkit for generating tailored, ATS-compatible CVs and cover letters using LaTeX templates and agent workflows. No coding required — just tell the agent what you want.

**Project Location**: `<ROOT_PROJECT>`

---

## 📋 Setup Steps (Execute All)

### 0. Choose Project Directory

**LLM asks the user:**
> "Where would you like to install cvkit? Please provide the full path to your project directory (e.g., `/Users/username/projects/cv` or `/home/username/cv`)."

**User responds with their preferred directory path.**

**LLM validates and uses:**
- Path must be absolute (starts with `/`)
- Path must be writable
- Directory will be created if it doesn't exist

**Set `<ROOT_PROJECT>` to user's response for all subsequent commands.**

### 1. Create Project Structure

```bash
cd <ROOT_PROJECT>

# Create required directories
mkdir -p .agents/skills/ Offers/ archive/ scripts/ templates/ .private/

# Create config from template
cp config.template.yaml config.yaml
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

### 3. Install Skills from skills-cv Repository

> **⚠️ Requirement**: `skills-cv` must be accessible for this step to work.

The `skills-cv` repository contains multiple skills. Install the ones you need:

```bash
# Install all CV-related skills
npx skills add https://github.com/yannassoumou/skills-cv --skill cv-job-application-workflow
npx skills add https://github.com/yannassoumou/skills-cv --skill cv-job-matching
npx skills add https://github.com/yannassoumou/skills-cv --skill job-offer-cv-adaptation-workflow
npx skills add https://github.com/yannassoumou/skills-cv --skill cv-adaptation
npx skills add https://github.com/yannassoumou/skills-cv --skill cv-improvement-workflow
npx skills add https://github.com/yannassoumou/skills-cv --skill cv-creation-from-scratch
npx skills add https://github.com/yannassoumou/skills-cv --skill camofox-browser
npx skills add https://github.com/yannassoumou/skills-cv --skill csv-to-cv-generation

# Verify skills are installed
npx skills list
```

### 4. Create config.yaml

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
| **csv-to-cv-generation** | Generate CVs and cover letters from CSV/Excel data | When you have structured job application data |
| **cv-job-application-workflow** | Full pipeline: extract → adapt → generate → organize | When you receive a job offer |
| **cv-source-update** | Update master CV with new info | When you get a new job/certification |
| **cv-adaptation** | Role-specific customization | When adapting CV for specific position |
| **cv-creation-from-scratch** | Build CV without existing source | When starting from zero |
| **cv-improvement-workflow** | Design & ATS optimization | When you want to improve CV quality |
| **cv-job-matching** | Match CV to job requirements | When evaluating job fit |

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
