     1|---
     2|name: cv-review
     3|description: Auto-review compiled CV PDFs for quality issues — section truncation, page breaks, formatting errors, and ATS compliance. Reads PDF via pdftotext and auto-fixes the .tex source.
     4|category: productivity
     5|---
     6|
     7|# CV Review — Automated Quality Checks
     8|
     9|Load this skill after generating a CV to verify quality before sending.
    10|
    11|## Trigger Conditions
    12|- After generating a new CV (.tex + .pdf)
    13|- User asks "review this CV" or "check the CV"
    14|- Before committing/pushing a new CV to GitHub
    15|
    16|## Review Steps
    17|
    18|### 1. Extract text from PDF
    19|```bash
    20|pdftotext -layout CV_[Company]_[Role]_[Date].pdf - | grep -n .
    21|```
    22|This shows line numbers and content, with `\f` marking page breaks.
    23|
    24|### 2. Check for section truncation (CRITICAL)
    25|A section header must NEVER appear on one page with its content on the next page.
    26|```bash
    27|# Check if any section header is immediately followed by \f (page break)
    28|pdftotext -layout CV_*.pdf - | grep -B1 $'\f' | grep -E "(PROFIL|COMPÉTENCES|EXPÉRIENCES|PROJETS|CERTIFICATIONS|FORMATION|LANGUES)"
    29|```
    30|If any match is found → **FAIL**. The section header is isolated at the bottom of a page.
    31|
    32|Fix: Add `\needspace{15\baselineskip}` before the offending `\cvsection{}` command in the .tex file.
    33|
    34|### 3. Check for content truncation
    35|A bullet point or paragraph must not be split across pages.
    36|```bash
    37|# Check if a bullet item is split across pages
    38|pdftotext -layout CV_*.pdf - | grep -A1 $'\f' | grep "•"
    39|```
    40|If bullets appear immediately after page breaks → check if they're continuations or orphans.
    41|
    42|### 4. Header format check
    43|Verify the header uses one-element-per-line format (NOT compressed with `$|$`):
    44|```bash
    45|grep -c '\$|\\$' CV_*.tex
    46|```
    47|If > 0 → **FAIL**. Elements are compressed. Each line (address, phone, email) should be its own `{\small\color{accent}...}` block.
    48|
    49|### 5. Page count
    50|```bash
    51|pdfinfo CV_*.pdf | grep Pages
    52|```
    53|- Target: 1–2 pages
    54|- If 3+ pages → trim content (fewer projects, shorter bullets)
    55|
    56|### 6. File size
    57|```bash
    58|ls -lh CV_*.pdf
    59|```
    60|- Target: 100–150 KB for 2 pages
    61|- If >200KB → check for embedded images (shouldn't have any)
    62|
    63|### 7. Profile person check
    64|```bash
    65|grep -c "A conçu\|A développé\|A déployé" CV_*.tex
    66|```
    67|If > 0 → **FAIL**. Profile must use first person "je" (J'ai conçu, J'ai développé).
    68|
    69|### 8. Prototype check
    70|```bash
    71|grep -ci "llama-tracker\|POC\|prototype" CV_*.tex
    72|```
    73|If > 0 → **FAIL**. Prototype projects must not appear on the CV.
    74|
    75|### 9. Frontend skills check (for AI/Data roles)
    76|```bash
    77|grep -ci "Material-UI\|Tailwind CSS\|React" CV_*.tex
    78|```
    79|If > 0 → **FLAG**. Frontend skills may not be relevant for AI/Data roles.
    80|
    81|### 10. Auto-fix
    82|When issues are found, patch the .tex file directly:
    83|- Section truncation → add `\needspace{15\baselineskip}` before the `\cvsection`
    84|- Third person → replace "A conçu" → "J'ai conçu", etc.
    85|- Frontend skills → remove the lines mentioning them
    86|- Recompile after fixes: `pdflatex -interaction=nonstopmode [file].tex`
    87|
    88|## Quick Check (one-liner)
    89|```bash
    90|cd ~/cv/Offers/[offer_dir]/
    91|# Run all checks on the latest PDF
    92|PDF=$(ls -t CV_*.pdf | head -1)
    93|TEX=$(ls -t CV_*.tex | head -1)
    94|echo "=== PAGE COUNT ===" && pdfinfo "$PDF" | grep Pages
    95|echo "=== SECTION TRUNCATION ===" && pdftotext -layout "$PDF" - | grep -B1 $'\f' | grep -E "(PROFIL|COMPÉTENCES|EXPÉRIENCES|PROJETS|CERTIFICATIONS|FORMATION|LANGUES)" && echo "FAIL - section truncated!" || echo "OK"
    96|echo "=== HEADER FORMAT ===" && grep -c '\$|\\$' "$TEX" && echo "FAIL - compressed header!" || echo "OK"
    97|echo "=== PERSON CHECK ===" && grep -c "A conçu\|A développé" "$TEX" && echo "FAIL - third person!" || echo "OK"
    98|echo "=== PROTOTYPE ===" && grep -ci "llama-tracker" "$TEX" && echo "FAIL - prototype!" || echo "OK"
    99|```
   100|
   101|## Common Pitfalls
   102|- `\needspace{1\baselineskip}` is TOO WEAK for project sections — use `\needspace{15\baselineskip}`
   103|- Running pdftotext requires `poppler-utils`: `sudo apt install poppler-utils`
   104|- The `\f` character in pdftotext output marks a page break — use `grep -B1 $'\f'` to find what's right before it
   105|- Always recompile after patching the .tex file and re-run the review