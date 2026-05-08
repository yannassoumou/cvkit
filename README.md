# cvkit — AI-Powered CV Toolkit

> One command. Paste your CV. Your agent does the rest.

cvkit turns your AI agent into a career copilot. Give it your CV once, then whenever you find a job offer, the agent generates a tailored ATS-friendly LaTeX CV — interactive, reviewed, and ready to send. No LaTeX knowledge needed.

---

## Quick Start

**Step 1** — Copy-paste this into your terminal:

```bash
git clone https://github.com/yannassoumou/cvkit.git ~/cv && cd ~/cv && mkdir -p ~/.hermes/skills/ && cp -r .agents/skills/* ~/.hermes/skills/
```

**Step 2** — Install LaTeX (one-time):

```bash
# Ubuntu/Debian
sudo apt install -y texlive-latex-recommended texlive-lang-french poppler-utils

# macOS
brew install --cask mactex && brew install poppler

# Fedora
sudo dnf install -y texlive-scheme-medium texlive-babel-french poppler-utils
```

**Step 3** — Start Hermes and paste this:

```
cd ~/cv && set up my CV project
```

That's it. The agent reads the project, asks about your Git setup, takes your CV, fills the template, and you're ready.

---

## What Happens Next

Once set up, every time you share a job offer, the agent:

1. Extracts the role, company, and requirements
2. Shows you the header and asks you to approve
3. Writes a tailored profile in first person ("je") — you review and tweak
4. Suggests which of your projects to include — you pick
5. Generates the LaTeX CV, compiles it to PDF, and reviews it automatically
6. Commits everything to Git (pushes to GitHub if you have a remote)

No code. No templates. Just paste the offer and say yes or no.

---

## What's Inside

```
~/cv/
├── AGENTS.md                ← Agent reads this first (instructions + rules)
├── README.md                 ← This file (you're reading it)
├── cvkit.md                  ← Setup guide for agents
├── CV_Master_template.txt    ← Reference format for your CV
├── CV_Master_texte.txt       ← Your CV — created by the agent on setup
├── .gitignore
├── .agents/skills/           ← Hermes skills (installed in ~/.hermes/skills/)
│   ├── cv-job-application-workflow/
│   ├── cv-review/
│   └── camofox-browser/
├── templates/
│   └── cv_template.tex       ← LaTeX template (ATS-friendly, navy blue)
├── scripts/
│   ├── generate_all_latex_cvs.py   ← Bulk regenerate all CVs
│   └── cv_web_server.py           ← Web dashboard
└── Offers/                   ← Your tailored CVs (one folder per offer)
    ├── offer1_company_role/
    │   ├── CV_Company_Role_Date.tex
    │   ├── CV_Company_Role_Date.pdf
    │   └── offre_data.md
    └── ...
```

---

## Requirements

- **Python 3.10+**
- **LaTeX** (pdflatex) — for PDF compilation
- **poppler-utils** (pdftotext, pdfinfo) — for CV review
- **Git** — for version control
- **Hermes** or any AGENTS.md-compatible AI agent (Claude Code, Cursor, OpenCode, Copilot)

---

## No GitHub Repo? No Problem

The agent asks you upfront. If you don't have a repo, it runs `git init` locally. All your CVs are versioned — you can push to GitHub/GitLab whenever you're ready.

---

## FAQ

**Can I use this with Claude Code / Cursor / OpenCode instead of Hermes?**

Yes. Open the `~/cv` folder in any AGENTS.md-compatible agent. It reads the same instructions.

**Do I need to know LaTeX?**

No. The agent writes all the LaTeX. You just review and approve.

**My CV is 3 pages. How do I fix it?**

The agent's auto-review catches this. Tell it to cut a project or shorten bullets.

**How do I add a new job offer?**

Paste the offer into your agent's chat. That's it.

**Can I customize the template?**

Edit `templates/cv_template.tex`. The agent preserves your changes.

---

## Credits

Built for humans who want AI to handle the boring part of job hunting. LaTeX template inspired by modern ATS-friendly designs.

**License**: MIT
