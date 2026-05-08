     1|     1|---
     2|     2|name: cv-job-application-workflow
     3|     3|description: Complete workflow for managing CV adaptations and cover letters for job applications
     4|     4|category: productivity
     5|     5|---
     6|     6|
     7|     7|# CV Job Application Workflow
     8|     8|
     9|     9|Complete system for managing CV adaptations and cover letters for job applications.
    10|    10|
    11|    11|## Trigger Conditions
    12|    12|- User receives a job offer (via email, LinkedIn, etc.)
    13|    13|- User wants to customize CV for a specific position
    14|    14|- User wants to create a cover letter
    15|    15|
    16|    16|## Workflow Steps
    17|    17|
    18|    18|### 1. Extract Job Offer Details
    19|    19|Parse the job offer to extract:
    20|    20|- **Job title** (intitulé du poste)
    21|    21|- **Company name**
    22|    22|- **Location**
    23|    23|- **Salary/rémunération**
    24|    24|- **Contract type** (CDI, CDD, etc.)
    25|    25|- **Technical requirements** (Savoirs)
    26|    26|- **Soft skills** (Savoir-être)
    27|    27|- **Benefits** (Conditions)
    28|    28|- **Recruitment process** (Parcours de recrutement)
    29|    29|- **Lien of the offer**
    30|    30|
    31|    31|**Methods:**
    32|    32|- Use Tavily API for web research: `curl -X POST "https://api.tavily.com/search" -H "Content-Type: application/json" -d '{"api_key": "YOUR_TAVILY_API_KEY", "query": "company job title", "search_depth": "advanced"}'`
    33|    33|- Use Camofox browser when available for full page extraction
    34|    34|
    35|    35|### 2. Use the Canonical Template
    36|    36|**ONE template only**: `templates/cv_template.tex` is the sole canonical LaTeX template.
    37|    37|- DOCX templates (standard, delescin) have been **deleted** — do not generate DOCX files
    38|    38|- Copy the preamble from `templates/cv_template.tex` verbatim for every adapted CV
    39|    39|- The preamble includes: `\documentclass[10pt,a4paper]{article}`, all `\usepackage`, colors,
    40|    40|  `\hypersetup`, `\titleformat`, `\setlist`, and custom commands (`\cvsection`, `\cvsubsection`, `\cvsubsubsection`)
    41|    41|- All adapted CVs must use the same preamble — consistency across offers
    42|    42|
    43|    43|### 3. Interactive Adaptation (Plan Mode)
    44|    44|
    45|    45|**CRITICAL**: CV generation is now INTERACTIVE. Do NOT auto-generate the full CV. Instead, work through each section with the user like a plan/review mode.
    46|    46|
    47|    47|#### Step 3a: Header Format Review
    48|    48|After extracting the offer details, **show the header format** BEFORE the profile.
    49|    49|
    50|    50|The header must use this format (each element on its OWN line, NOT compressed with `$|$`):
    51|    51|```
    52|    52|YOUR FULL NAME                    ← name on its own line
    53|    53|Your Job Title       ← job title below, centered
    54|    54|                                   ← blank space
    55|    55|Your Address, City, Country        ← address on its own line
    56|    56|+33 X XX XX XX XX                  ← phone on its own line
    57|    57|your.email@example.com             ← email on its own line
    58|    58|                                   ← blank space
    59|    59|linkedin...  |  github...          ← links on one line with spacing
    60|    60|```
    61|    61|In LaTeX, this means each line is a separate `{\small\color{accent} ...}` block with `\vspace{2pt}` between them — never use `$|$` to cram multiple items on one line.
    62|    62|Present the header using `clarify` tool: "Voici le format du header. OK ?"
    63|    63|Only proceed to profile after header is approved.
    64|    64|
    65|    65|#### Step 3b: Profile Review
    66|    66|After the header is approved, **draft a tailored profile paragraph** and present it to the user BEFORE generating the full CV.
    67|    67|
    68|    68|- Write in **first person "je"** (NOT "A conçu" — use "J'ai conçu et déployé...")
    69|    69|- Emphasize keywords from the job description
    70|    70|- Mention the company/industry context naturally
    71|    71|- Keep it concise (3-5 lines ideal for LaTeX)
    72|    72|- Use the `clarify` tool to present the profile suggestion with these choices:
    73|    73|  - "Approuver ce profil" (approve)
    74|    74|  - "Modifier : [user types changes]" (modify)
    75|    75|  - Do NOT proceed to project selection until the profile is approved.
    76|    76|
    77|    77|#### Step 3c: Project Selection
    78|    78|Once the profile is approved, **present the list of projects** from the master CV and let the user select which ones to include.
    79|    79|
    80|    80|- List ALL projects from `CV_Master_texte.txt` that are NOT prototypes (exclude llama-tracker and any experimental work)
    81|    81|- For each project, add a brief 1-line rationale showing why it's relevant to THIS offer
    82|    82|- Sort by relevance (most relevant first)
    83|    83|- Present using `clarify` tool with choices:
    84|    84|  - "Selectionner [project names]" — user types which ones to include
    85|    85|  - "Tout inclure" (include all)
    86|    86|  - "Montrer plus de projets" (load more projects — the user may have projects not in the master CV)
    87|    87|- After selection, confirm the final list: "Tu as sélectionné : [list]. Confirmer ?"
    88|    88|- If the user says "load more" or "montre plus", ask them what additional projects they have in mind
    89|    89|
    90|    90|#### Step 3d: Cover Letter (Optional)
    91|    91|After CV is generated, **ask the user if they want a cover letter**.
    92|    92|
    93|    93|- If yes: generate a personalized cover letter using LaTeX (same preamble as the CV)
    94|    94|- 4 paragraphs: (1) Motivation for this specific company/role, (2) Relevant experience and key skills, (3) Concrete achievements and projects that match their needs, (4) Availability and call to action
    95|    95|- Header with name, title, contact info — same format as CV header
    96|    96|- Date and recipient block
    97|    97|- Use `clarify` tool to present the letter: "Voici la lettre de motivation. Modifications ?"
    98|    98|- User can approve, modify, or skip
    99|    99|- Compile with pdflatex, same naming: `Lettre_Motivation_[Company]_[Date].tex`
   100|   100|- Place in the same offer directory as the CV
   101|   101|
   102|   102|#### Step 3e: Final Generation
   103|   103|After header, profile and projects are approved:
   104|   104|- **Update job title** to match target position
   105|   105|- **Filter skills** for role relevance: strip frontend skills (React, Material-UI, Tailwind CSS) for AI/Data roles
   106|   106|- **Generate the .tex** using the canonical template preamble from `templates/cv_template.tex`
   107|   107|- **Add `\needspace{15\baselineskip}` before `\cvsection{PROJETS PERSONNELS}`** — this is critical to prevent the section header from being orphaned at the bottom of page 1
   108|   108|- **Compile** with `pdflatex -interaction=nonstopmode`, clean aux/log/out
   109|   109|- **Run cv-review skill** immediately after compilation to catch truncation, third-person, header format issues
   110|   110|- **Use production-ready language**: Present projects as production systems (avoid "POC" terminology)
   111|   111|
   112|   112|### 4. Create Cover Letter
   113|   113|Generate personalized cover letter:
   114|   114|- **Header** with name, title, contact info
   115|   115|- **Date and recipient block** (left column)
   116|   116|- **5 paragraphs**:
   117|   117|  1. Motivation for the specific position
   118|   118|  2. Presentation with relevant experience
   119|   119|  3. Key competencies (bullet points)
   120|   120|  4. Value proposition (projects, achievements)
   121|   121|  5. Availability and call to action
   122|   122|- **Signature** with contact info
   123|   123|
   124|   124|#### PDF Generation Options
   125|   125|- **LaTeX** (default) — ATS-friendly, compact, user's preferred format
   126|   126|- **WeasyPrint** (HTML/CSS → PDF) — For visually rich documents:
   127|   127|  - Portfolio PDFs with custom CSS styling
   128|   128|  - Creative cover letters with modern layouts
   129|   129|  - Consulting reports, executive summaries
   130|   130|  - Install: `pip install weasyprint`
   131|   131|  - Usage: `HTML(string=html_content).write_pdf("output.pdf")`
   132|   132|  - Works with Jinja2 templates for dynamic data
   133|   133|  - Better than ReportLab for styled documents (CSS3 support)
   134|   134|  - Source: https://github.com/Kozea/WeasyPrint
   135|   135|
   136|   136|### 5. Organize Files
   137|   137|Create structured folders in `Offers/` directory (uppercase):
   138|   138|```
   139|   139|Offers/offerX_[company]_[job_title]/
   140|   140|├── offre_data.md              # Complete offer details
   141|   141|├── README.md                  # Candidature summary
   142|   142|├── CV_[Company]_[Role]_[Date].tex   # LaTeX source
   143|   143|├── CV_[Company]_[Role]_[Date].pdf   # Compiled PDF (compact, 2 pages max)
   144|   144|├── Lettre_Motivation_[Company]_[Date].tex   # Cover letter (optional)
   145|   145|└── Lettre_Motivation_[Company]_[Date].pdf   # Cover letter PDF (optional)
   146|   146|```
   147|   147|
   148|   148|**IMPORTANT**: Use `Offers/` (UPPERCASE) directory, NOT `offers/` (lowercase).
   149|   149|**Naming convention**: `CV_[Company]_[Role]_[Date].tex` — standardized across all offers.
   150|   150|**Naming convention**: Use short, clean names. Example: `CV_Example_Company_Position_2026-04-16.tex`, not `CV_Example_Company_Position_Ingénieur_IA_-_Compliance_and_Corporate__2026-04-16.tex`.
   151|   151|**File cleanup**: After regenerating a CV, delete old `.tex` and `.pdf` files from past generations to keep the directory clean (one CV per offer).
   152|   152|
   153|   153|### LaTeX Compact Version
   154|   154|For LaTeX-generated CVs, create a compact variant by:
   155|   155|- Reducing `\\vspace` calls (use 2-3pt instead of 4-6pt)
   156|   156|- Using `10pt` document class option instead of `11pt`
   157|   157|- Reducing `\\setlist` `topsep` to `2pt`
   158|   158|- Reducing section margins to `0.7in` via geometry
   159|   159|- This keeps the CV to 1-2 pages maximum
   160|   160|
   161|   161|**MANDATORY: Prevent section cuts across pages.** Use `\needspace{3\baselineskip}` before every `\cvsection`, `\needspace{2\baselineskip}` before every `\cvsubsection`, and `\needspace{3\baselineskip}` before every `\cvsubsubsection` (project entries). This forces the page break BEFORE the section block rather than cutting it in half. **One `\baselineskip` is NOT enough** — projects with 3+ bullet points need at least 3 lines of reserve space.
   162|   162|
   163|   163|**MANDATORY: Be concise.** When content threatens a third page, prioritize: (1) profil, (2) compétences, (3) expériences récentes, (4) projets pertinents. Trim older/less relevant items first. Drop details that don't directly support the target role.
   164|   164|
   165|   165|**MANDATORY: Section ordering for this user** (always apply this hierarchy):
   166|   166|1. Profil (first person "je")
   167|   167|2. Compétences
   168|   168|3. Expérience Professionnelle
   169|   169|4. Projets (production only, no prototypes)
   170|   170|5. Certifications
   171|   171|6. Formation
   172|   172|7. Langues
   173|   173|
   174|   174|Place certifications at the bottom, skills near the top, and formation right before langues.
   175|   175|
   176|   176|### 6. Bulk Regeneration (All Offers)
   177|   177|
   178|   178|When regenerating ALL offer CVs from the master (e.g. after a master CV update):
   179|   179|
   180|   180|1. **Test first**: Generate ONE offer, compile, verify PDF — then batch the rest
   181|   181|2. **Copy preamble** from `templates/cv_template.tex` (everything before `\begin{document}`)
   182|   182|3. **Tailor per offer**: profile paragraph, 2-4 most relevant projects, emphasize matching skills
   183|   183|4. **Strip frontend skills** (Material-UI, Tailwind CSS, React) for AI/Data roles
   184|   184|5. **Generate .tex**, compile with `pdflatex -interaction=nonstopmode`, clean `*.aux *.log *.out`
   185|   185|6. **Delete old files** from previous generations to keep one CV per offer
   186|   186|7. **Verify page count**: target 2 pages max, ~120KB PDF
   187|   187|
   188|   188|### 7. Update Application Journal
   189|   189|Log in `Offers/README.md` (not in `offers/application_journal.md`):
   190|   190|```markdown
   191|   191|## YYYY-MM-DD - Company
   192|   192|- Poste : [Job title]
   193|   193|- Lieu : [Location]
   194|   194|- Statut : CV généré et prêt
   195|   195|- Fichiers : CV_Adapté.docx, CV_Adapté.pdf
   196|   196|- Lien : [Offer URL]
   197|   197|```
   198|   198|
   199|   199|### 8. Commit and Push
   200|   200|```bash
   201|   201|cd ~/cv/
   202|   202|
   203|   203|# Stage changes
   204|   204|git add -A
   205|   205|
   206|   206|# Commit with detailed message
   207|   207|git commit -m "Update CV for [Company] — [Role]"
   208|   208|
   209|   209|# Push to remote
   210|   210|git push origin main
   211|   211|
   212|   212|# If push fails (auth), use gh CLI:
   213|   213|gh auth status || gh auth login --hostname github.com --git-protocol https --web --scopes repo
   214|   214|git push origin main
   215|   215|```
   216|   216|
   217|   217|**MANDATORY**: Verify push succeeded. If `fatal: could not read Username`, authenticate with `gh auth login` first. The user expects to see changes on GitHub immediately.
   218|   218|
   219|   219|### 9. Start CV Web Server (Browse & Edit from Any Device)
   220|   220|
   221|   221|After commit/push, start a local HTTP server so you can browse all offers and edit the master CV from any device on your network (phone, tablet, laptop).
   222|   222|
   223|   223|```bash
   224|   224|cd ~/cv/
   225|   225|
   226|   226|# Kill any existing CV web server
   227|   227|pkill -f "cv_web_server.py" 2>/dev/null || true
   228|   228|sleep 0.5
   229|   229|
   230|   230|# Start the server in background (python3 -u for unbuffered output)
   231|   231|python3 -u scripts/cv_web_server.py > /tmp/cv-web-server.log 2>&1 &
   232|   232|SERVER_PID=$!
   233|   233|echo $SERVER_PID > /tmp/cv-web-server.pid
   234|   234|
   235|   235|# Wait for server to start and get the URL
   236|   236|sleep 1
   237|   237|URL=$(grep "URL:" /tmp/cv-web-server.log | tail -1 | sed 's/.*URL: //')
   238|   238|echo "$URL"
   239|   239|```
   240|   240|
   241|   241|**What the server provides:**
   242|   242|- **Dashboard** (`/`) — Stats overview (number of offers, files)
   243|   243|- **Offer browser** (`/api/offers`) — Click any offer to see its files
   244|   244|- **PDF preview** — Inline PDF viewing for CVs and cover letters
   245|   245|- **File download** — One-click download of any file
   246|   246|- **Master CV editor** (`/api/cv-text` + `POST /api/save-cv-text`) — Edit `CV_Master_texte.txt` directly in the browser
   247|   247|- **Offer data editor** — Edit `offre_data.md` files inline
   248|   248|
   249|   249|**Access URL:** `http://<machine-ip>:<port>` (printed in server output)
   250|   250|
   251|   251|**Dashboard features:**
   252|   252|- Dark-themed sidebar listing all offers with file counts
   253|   253|- Click an offer → browse files, preview PDFs, download DOCX
   254|   254|- Click "Master CV" → full-text editor for `CV_Master_texte.txt` with Save button
   255|   255|- Click `offre_data.md` files → inline editor with Save button
   256|   256|- Tab support in text editor
   257|   257|
   258|   258|**Server lifecycle:**
   259|   259|- Runs as background process (PID saved to `/tmp/cv-web-server.pid`)
   260|   260|- Bind to `0.0.0.0` (accessible from any device on the network)
   261|   261|- Auto-assigns random available port
   262|   262|- Kill with: `pkill -f "cv_web_server.py"` or `kill $(cat /tmp/cv-web-server.pid)`
   263|   263|
   264|   264|**When to use:**
   265|   265|- After every commit/push to keep the server fresh
   266|   266|- When you want to review all offers from your phone/tablet
   267|   267|- When you need to edit the master CV on the go
   268|   268|- When sharing your CV setup with someone on the same network
   269|   269|
   270|   270|## Git Repository Structure
   271|   271|```
   272|   272|cv/
   273|   273|├── CV_Master_texte.txt          # Source of truth — master CV in plain text
   274|   274|├── CV_Master_template.txt       # Template with placeholders (reference)
   275|   275|├── .gitignore                   # Ignores *.aux *.log *.out *.pyc __pycache__
   276|   276|├── templates/
   277|   277|│   └── cv_template.tex          # ONE canonical LaTeX template (preamble + full CV)
   278|   278|├── scripts/
   279|   279|│   ├── cv_web_server.py         # HTTP dashboard for browsing offers
   280|   280|│   └── generate_all_latex_cvs.py # Batch generation (update OFFERS dict before use)
   281|   281|├── Offers/                      # UPPERCASE — all adapted CVs
   282|   282|│   ├── offerX_[company]_[role]/
   283|   283|│   │   ├── offre_data.md
   284|   284|│   │   ├── README.md
   285|   285|│   │   ├── CV_[Company]_[Role]_[Date].tex
   286|   286|│   │   └── CV_[Company]_[Role]_[Date].pdf
   287|   287|│   └── README.md                # Application journal
   288|   288|└── .agents/skills/              # Agent skill documentation
   289|   289|```
   290|   290|
   291|   291|## Tools Required
   292|   292|- Python with python-docx
   293|   293|- LibreOffice (for PDF conversion)
   294|   294|- Tavily API key: `YOUR_TAVILY_API_KEY`
   295|   295|- Git repository: https://github.com/YOUR_USERNAME/cv
   296|   296|
   297|   297|## Template Specifications
   298|   298|
   299|   299|### Canonical LaTeX Template
   300|   300|**Single template**: `templates/cv_template.tex` — the ONLY template.
   301|   301|
   302|   302|- **Document class**: `10pt,a4paper` (compact)
   303|   303|- **Margins**: `0.7in` via geometry
   304|   304|- **Colors**: Navy blue `primary` (RGB 0,51,102), gray `secondary` (RGB 100,100,100)
   305|   305|- **Section commands**: `\cvsection`, `\cvsubsection`, `\cvsubsubsection` defined in preamble
   306|   306|- **List spacing**: `topsep=2pt`, compact `before=\vspace{1pt}`
   307|   307|- **Page-break guard**: `\needspace{\baselineskip}` before every `\cvsection`
   308|   308|- **Links**: `\href` with `urlcolor=primary`, hyperref configured
   309|   309|- **Output**: 1-2 pages, ~120KB PDF via `pdflatex`
   310|   310|
   311|   311|All adapted CVs copy this preamble verbatim — do NOT create new preamble variants per offer.
   312|   312|
   313|   313|### Pitfalls to Avoid
   314|   314|1. Don't lie about skills/experiences
   315|   315|2. Don't over-optimize (maintain authenticity)
   316|   316|3. Keep track of versions (which CV sent where)
   317|   317|4. Maintain original CV as reference
   318|   318|5. **CRITICAL**: Use `Offers/` (UPPERCASE) directory, NOT `offers/` (lowercase)
   319|   319|6. **CRITICAL**: Delete the legacy `offers/` folder when upgrading to new workflow
   320|   320|7. Don't delete real tickets/data without authorization
   321|   321|8. Always backup data before updates
   322|   322|9. **NEVER include prototype/learning projects on the CV** — user explicitly excludes experimental work (llama-tracker, etc.)
   323|   323|10. **Always write profil in first person "je"** — never third person like "A conçu"
   324|   324|11. **ALWAYS use `\needspace{\baselineskip}` before each `\section{}`** to prevent sections being cut across pages
   325|   325|12. **For Python/Gen AI roles, strip frontend skills** (React, Material-UI, Tailwind CSS) — they clutter and dilute relevance
   326|   326|13. **Prioritize conciseness** — if content threatens a 3rd page, cut older/less relevant items before expanding
   327|   327|14. **generate_all_latex_cvs.py OFFERS dict is incomplete** — it only contains 1 offer (credit_agricole_cib). Update the dict before running, or generate per-offer individually
   328|   328|15. **Master CV itself can violate your rules** — the source `CV_Master_texte.txt` may contain third-person prose ("A conçu") when your skill mandates "je", or include prototype projects when you explicitly exclude them. Always audit the master before generating adapted CVs
   329|   329|16. **Filenames can be corrupted by copy-paste** — after generating CVs, verify filenames match the offer. Example: ElevenLabs PDFs were named `CV_IBM_Data_AI_Engineer_*` inside the ElevenLabs directory — a copy-paste error from the IBM offer
   330|   330|17. **No .gitignore → aux file pollution** — LaTeX generates `.aux`, `.log`, `.out` files in every offer directory. Create `.gitignore` with `*.aux`, `*.log`, `*.out`, `__pycache__/`, `*.pyc` at project root
   331|   331|18. **Test one offer first** — before regenerating all 10 CVs, generate ONE, compile, verify the PDF, then batch the rest. Avoids wasting time on a broken template
   332|   332|19. **NEW OFFERS = INTERACTIVE MODE** — For any NEW job offer, the workflow is interactive: draft profile → user approves → list projects → user selects → generate CV. Do NOT auto-generate a full CV without user review. Bulk regeneration (Step 6) is only for updating EXISTING offers after a master CV change — it's a batch operation, not the default.
   333|   333|20. **Section truncation is UNACCEPTABLE** — A section title must NEVER appear at the bottom of a page with its content on the next page, and section content must NEVER be cut mid-sentence across pages. Three layers of protection in the preamble: (a) `\needspace{\baselineskip}` before every `\cvsection`, (b) `\usepackage{needspace}` loaded, (c) if content still overflows despite these, CUT content (fewer projects, fewer bullet points) rather than risking truncation. Always verify in the compiled PDF that every section starts on the same page as its first bullet.
   334|   334|
   335|   335|## Example Usage
   336|   336|
   337|   337|```
   338|   338|User: "Voici l'offre : [copie l'offre]"
   339|   339|Agent:
   340|   340|1. Extract offer details (company, position, requirements)
   341|   341|2. Draft a tailored profile paragraph in first person "je"
   342|   342|3. Use clarify() to present the profile: "Voici ma suggestion de profil..."
   343|   343|4. User approves or modifies the profile
   344|   344|5. List eligible projects from master CV with relevance notes
   345|   345|6. Use clarify() to ask: "Quels projets souhaites-tu inclure ?"
   346|   346|7. User selects projects (or asks to show more)
   347|   347|8. Generate adapted CV (.tex) using canonical template preamble
   348|   348|9. Compile to PDF with pdflatex, clean aux/log/out
   349|   349|10. Organize in Offers/ folder, delete old .tex/.pdf
   350|   350|11. Update application journal in Offers/README.md
   351|   351|12. Commit and push to GitHub
   352|   352|```
   353|   353|
   354|   354|## Directory Naming Convention
   355|   355|
   356|   356|**IMPORTANT**: Use `Offers/` (UPPERCASE) for the new LaTeX-based workflow.
   357|   357|
   358|   358|**DO NOT USE**: `offers/` (lowercase) - this is the legacy folder that should be deleted.
   359|   359|
   360|   360|Example structure:
   361|   361|```
   362|   362|Offers/
   363|   363|├── offer1_example_company/
   364|   364|├── offer2_example_company/
   365|   365|└── README.md
   366|   366|```
   367|   367|
   368|   368|## Verification Steps
   369|   369|- Check all files generated (.tex + .pdf for CV, plus cover letter if requested)
   370|   370|- Verify PDF is valid (not corrupted): `file CV_*.pdf`
   371|   371|- Verify page count: should be 1-2 pages, ~120-150KB
   372|   372|- Confirm template preamble matches `templates/cv_template.tex`
   373|   373|- Ensure Git commit message is descriptive
   374|   374|- Test that push succeeded and files are accessible from GitHub
   375|   375|- **VERIFY**: Directory is `Offers/` (UPPERCASE), NOT `offers/` (lowercase)
   376|   376|- **CLEANUP**: Delete old `.tex` and `.pdf` from previous generations so only the latest CV remains
   377|   377|## Related Skills
   378|   378|
   379|   379|- `web-research-with-tavily`: Extract job offer details
   380|   380|- `camofox-browser`: Anti-detection browser for job offer extraction
   381|   381|- `references/exalt-it-adaptation.md`: Session-specific notes for eXalt IT CV adaptation patterns
   382|   382|- `references/bulk-regeneration.md`: Deep cleanup and bulk regeneration workflow
   383|   383|- `cv-adaptation`: (absorbed into this skill)
   384|   384|- `cv-creation-from-scratch`: (absorbed into this skill)
   385|   385|- `cv-job-matching`: (absorbed into this skill)
   386|   386|- `cv-web-server`: (absorbed into this skill)
   387|   387|- `cvkit-project-setup`: (absorbed into this skill)
   388|   388|- `cv-improvement-workflow`: (absorbed into this skill)
   389|   389|- `modern-ats-friendly-cv-template`: (absorbed into this skill)
   390|   390|
   391|   391|---
   392|   392|
   393|   393|## Appendix: CV Improvement (ATS Design & Optimization)
   394|   394|
   395|   395|### ATS Compatibility Audit
   396|   396|
   397|   397|Check for these issues:
   398|   398|- ❌ Tables, columns, text boxes
   399|   399|- ❌ Icons, graphics, images
   400|   400|- ❌ Non-standard fonts
   401|   401|- ❌ Headers/footers with critical info
   402|   402|- ❌ Uncommon section headings
   403|   403|- ❌ Low contrast text
   404|   404|- ❌ Complex layouts
   405|   405|
   406|   406|### Modern Design Guidelines
   407|   407|
   408|   408|- Single column layout
   409|   409|- Professional navy blue (#003366) for headers
   410|   410|- Clean, minimalist layout
   411|   411|- Standard section headings (Work Experience, Education, Skills)
   412|   412|- Standard fonts (Calibri, Arial, Helvetica)
   413|   413|- Consistent spacing and bold section headers
   414|   414|
   415|   415|### Skills Section Enhancement
   416|   416|
   417|   417|Format skills in categorized blocks:
   418|   418|```
   419|   419|LANGAGES DE PROGRAMMATION
   420|   420|Python (expert) - Data science, ML, automation •
   421|   421|Java (avancé) - Spring Boot, applications enterprise •
   422|   422|
   423|   423|FRAMEWORKS & TECHNOLOGIES
   424|   424|Machine Learning : TensorFlow, PyTorch, Scikit-learn •
   425|   425|Big Data : Hadoop, Spark, Kafka •
   426|   426|Cloud : GCP, AWS •
   427|   427|```
   428|   428|
   429|   429|### Output Files
   430|   430|- `CV_Improved_[JobTitle]_[Company]_[Date].docx`
   431|   431|- `CV_Improved_[JobTitle]_[Company]_[Date].pdf`
   432|   432|- `CV_Improvement_Report_[Company]_[Date].txt`
   433|   433|
   434|   434|---
   435|   435|
   436|   436|## Appendix: CV Creation from Scratch
   437|   437|
   438|   438|### When to Use
   439|   439|- User wants to create a new CV from scratch
   440|   440|- User wants to update existing CV with new experiences/certifications
   441|   441|- User needs to extract CV content from PDF
   442|   442|
   443|   443|### PDF to Text Extraction
   444|   444|```bash
   445|   445|# Convert PDF to PNG
   446|   446|convert -density 300 input.pdf -quality 100 output.png
   447|   447|# Use vision_analyze to extract all text
   448|   448|```
   449|   449|
   450|   450|### DOCX Generation with python-docx
   451|   451|```python
   452|   452|from docx import Document
   453|   453|from docx.shared import Pt, RGBColor
   454|   454|from docx.enum.text import WD_ALIGN_PARAGRAPH
   455|   455|
   456|   456|doc = Document()
   457|   457|style = doc.styles['Normal']
   458|   458|font = style.font
   459|   459|font.name = 'Calibri'
   460|   460|font.size = Pt(11)
   461|   461|```
   462|   462|
   463|   463|### Formatting Rules
   464|   464|- **Font**: Calibri
   465|   465|- **Name**: 24pt, bold, blue (RGB 0,51,102)
   466|   466|- **Headings**: Heading 2 (14pt) and Heading 3 (12pt)
   467|   467|- **Lists**: Built-in bullet styles
   468|   468|- **Margins**: Standard (1 inch)
   469|   469|- **Length**: 1-2 pages maximum
   470|   470|
   471|   471|### Pitfalls
   472|   472|1. **python-docx runs[] IndexError**: Always check if `p.runs` exists before accessing
   473|   473|2. **PDF extraction**: Vision analysis works better than trying to parse PDF directly
   474|   474|3. **Special characters**: Ensure UTF-8 encoding for French characters
   475|   475|
   476|   476|---
   477|   477|
   478|   478|## Appendix: CV Web Server
   479|   479|
   480|   480|### Quick Start
   481|   481|```bash
   482|   482|cd ~/cv/
   483|   483|pkill -f "cv_web_server.py" 2>/dev/null || true
   484|   484|sleep 0.5
   485|   485|python3 -u scripts/cv_web_server.py > /tmp/cv-web-server.log 2>&1 &
   486|   486|SERVER_PID=$!
   487|   487|echo $SERVER_PID > /tmp/cv-web-server.pid
   488|   488|sleep 1
   489|   489|URL=$(grep "URL:" /tmp/cv-web-server.log | tail -1 | sed 's/.*URL: //')
   490|   490|echo "$URL"
   491|   491|```
   492|   492|
   493|   493|### Server Features
   494|   494|- Dashboard (`/`) — Dark-themed UI with stats
   495|   495|- API: `GET /api/offers`, `GET /api/cv-text`, `POST /api/save-cv-text`
   496|   496|- PDF preview inline, DOCX download
   497|   497|- Master CV editor (`/api/cv-text`) with Save button
   498|   498|- Offer data editor for `offre_data.md` files
   499|   499|
   500|   500|### Pitfalls
   501|