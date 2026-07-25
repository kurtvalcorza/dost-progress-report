# dost-progress-report

**A working build project for DOST progress reports.** Write one Markdown file,
get a Word document that matches the DOST prescribed format — Arial 11, chapters
on new pages, every required part present — and a set of checks that catch the
structural mistakes long reports actually make.

Covers both formats:

- **Semi-annual** — DOST Form 6
- **Annual** — DOST Form 7

> Not affiliated with or endorsed by DOST. Built from the published format
> instructions. **Forms change — check the skeletons against your funder's
> current forms** ([`docs/dost-format-reference.md`](docs/dost-format-reference.md)
> shows exactly what this template assumes).

---

## Contents

- [Why this exists](#why-this-exists)
- [Before you start](#before-you-start)
- [Getting started](#getting-started)
- [The daily loop](#the-daily-loop)
- [Writing the report](#writing-the-report)
- [The nine checks](#the-nine-checks)
- [Figures](#figures)
- [Changing the structure](#changing-the-structure)
- [Working with a co-author](#working-with-a-co-author)
- [Decisions you have to make](#decisions-you-have-to-make)
- [What's in the repository](#whats-in-the-repository)
- [Troubleshooting](#troubleshooting)
- [Governance (optional)](#governance-optional)
- [Contributing](#contributing)

---

## Why this exists

Long reports fail in specific, boring ways. A chapter goes missing from the final
document and nobody notices. A cross-reference says "see Section 5.3" and 5.3 is
now about something else. A citation is in the text but not the reference list.
Someone edits the Word file and their changes vanish at the next rebuild.

None of those are writing problems, and none are caught by reading carefully.
This repository is the machinery that catches them.

**What you get**

- One authored file, `REPORT.md` — no chapter files to keep in sync
- A **hard build failure** if a chapter would be silently dropped from the render
- Arial 11 and chapter page breaks applied automatically
- Nine checks over structure, cross-references, citations, and figures
- Skeletons for both formats with the requirements written into them, so you can
  see what each part is supposed to contain while you write it

**What it does not do**

It does not write the report, submit it, or produce DOST Forms 6, 8, 9, 11, or
12. It does not check whether your claims are true.

---

## Before you start

You need two things.

| | | Check with |
|:--|:--|:--|
| **[Quarto](https://quarto.org/docs/get-started/)** 1.5+ | renders the document; bundles pandoc | `quarto --version` |
| **Python** 3.9+ | runs the checks | `python --version` |

**You do not need to install any Python packages** to write and check a report.
The checker and the formatting patcher use only the standard library. Packages
are needed only if you generate figures — see [Figures](#figures).

Commands below are PowerShell (Windows). On macOS or Linux the Python parts work
unchanged; the two `.ps1` scripts need
[PowerShell 7+](https://github.com/PowerShell/PowerShell), which is a normal
install. **This has been tested on Windows only** — if you run it elsewhere,
please report what happened.

---

## Getting started

**1. Get the files.** On GitHub click **Use this template** → *Create a new
repository*. Or clone:

```powershell
git clone https://github.com/kurtvalcorza/dost-progress-report.git my-project-report
cd my-project-report
```

**2. Choose your format.**

```powershell
.\init.ps1 -Format semi-annual
```

or `-Format annual`. This copies the right skeleton to `REPORT.md`, the matching
`_quarto.yml`, and generates `reference.docx` (which carries Arial 11 and the
page breaks).

**3. Fill in who you are.** Two places:

- the frontmatter at the top of `REPORT.md` — project title, leader, agencies,
  duration, reporting period, budget
- the `title:`, `subtitle:`, and `author:` block in `_quarto.yml` — this is what
  renders as your **title page**, so replace every `<angle-bracket>` placeholder

**4. Build it once, before writing anything.**

```powershell
.\build.ps1
quarto render --to docx
```

Open `_output\*.docx`. You should see a title page, a table of contents, and
every required part as an empty heading. That is your skeleton, and it already
satisfies the format's structure.

---

## The daily loop

```powershell
.\build.ps1                              # split REPORT.md into chapter files
quarto render --to docx                  # produce the Word document
python tools\report-check.py REPORT.md   # run the nine checks
```

Then **read the gate 5 output** — see [The nine checks](#the-nine-checks).

Copy the finished document somewhere sensible when you hand it over:

```powershell
Copy-Item _output\*.docx "output\My Project - Semi-Annual Progress Report.docx"
```

### The one rule

> **`REPORT.md` is the only file you edit. Changes made in the Word document are
> destroyed on the next build.**

There is no recovery. If a reviewer marks up the `.docx`, type their changes back
into `REPORT.md` before anyone rebuilds. If you review in Word yourself, send the
marked-up copy back rather than assuming it will be picked up.

---

## Writing the report

Open `REPORT.md`. Every part is already there as a heading, and most carry an
HTML comment explaining what the format expects. Those comments never appear in
the rendered document, so you can leave them in place while you write — they are
the specification, sitting where you need it.

**Structure rules the build depends on:**

| Write | For |
|:--|:--|
| `# CHAPTER 3. METHODOLOGY` | a numbered chapter |
| `## 3.1 Variables Measured` | a section inside it |
| `### Some Sub-topic` | anything below that — never numbered by hand |
| `# APPENDICES` | front or back matter (no `CHAPTER n.` = unnumbered) |

Quarto adds the numbers when rendering, so `# CHAPTER 3.` becomes "3." on the
page — you will not see double numbering.

**Never write a bold line as a heading.** `**4.4 Market Drivers**` looks like a
heading and is not one: it stays out of the table of contents, and it keeps its
old number forever when you renumber. Check 3 catches this.

### Parts that do not apply to your project

Do not delete the heading. Say it does not apply and why:

> **4.2 Treatments and Layout** — Not applicable. This is a systems-development
> project with no experimental treatments. The analogous element is the set of
> benchmark configurations described in §4.3.

The format explicitly permits omitting non-applicable items for non-R&D projects.
But a deleted heading is indistinguishable from an oversight, and a reviewer
working down a checklist will mark it missing.

### Citations

Write them as `[1]`, `[2]`, `[3]` in the text, with matching entries under
`# References`:

```
[1] J. Dela Cruz, "Title of the Work," Journal Name, 2025. [Online].
    Available: https://example.org/paper
```

Numbers ascend with no gaps; every entry is cited at least once; every citation
is listed. Check 7 enforces all three. Ranges work: `[3-5]` counts as three
citations.

See [Decisions you have to make](#decisions-you-have-to-make) — the format
actually asks for alphabetical author-year, and this template ships IEEE numeric
for a reason you should know about.

---

## The nine checks

```powershell
python tools\report-check.py REPORT.md
```

| # | Catches |
|:--|:--|
| 1–2 | A chapter or section number skipped — `3, 4, 6` |
| 3 | A bold line pretending to be a heading |
| 4 | A reference to a chapter or section that does not exist |
| **5** | **Prints every `§n.m` reference beside the title it points at** |
| 6 | A bare "Section 5" — ambiguous, and invisible to the other checks |
| 7 | Citations cited but not listed, listed but never cited, numbering gaps |
| 8 | A figure referenced in the text but missing from disk |
| 9 | Marketing language, with reference entries excluded |

Add `--strict` to make it exit non-zero on failure, for a CI pipeline.

### Check 5 needs you

It never fails. It prints a list like this and stops:

```
L235   1.2    -> "Purpose and Objectives"
       ...answer the objectives set out in Section 1.2
```

**Read it.** A reference to §5.3 resolves perfectly even when the content it
meant moved to §6.3 during a renumber. No tool can tell the difference, because
what you *meant* is not in the document. This is the single most common way a
restructured report ships broken.

### What a PASS does not mean

Four things nothing checks:

- whether the acronym list matches the acronyms you actually used
- whether the list of tables and figures matches the figures on disk
- whether bare `Chapter n` references still point at the right chapter — check 5
  shows `§n.m` only
- whether any claim in the report is true

Reconcile the first two by hand before submitting. For the third, see
[Changing the structure](#changing-the-structure).

---

## Figures

Figures are **generated from code**, not exported from a spreadsheet, so they can
be reproduced when a number changes and reviewed by whoever checks the report.

```powershell
python -m pip install -r requirements.txt
python figures\make_figures.py
```

It writes PNG into `assets/`. Reference them from `REPORT.md`:

```markdown
![Targeted versus actual output by objective.](assets/fig-01-targeted-vs-actual.png)
```

`assets/` is gitignored — figures are reproducible, so they are not tracked.
Anyone who clones the repository runs the script to get them.

**Use PNG, not SVG.** Pandoc cannot size SVG without `rsvg-convert`, and an
unsized SVG renders unpredictably in Word.

**Look at every figure before wiring it in.** Clipped labels and text running off
the canvas do not raise errors.

> The shipped example uses invented numbers and says so *inside the image*, so a
> placeholder cannot be mistaken for a finding if it reaches a draft. Replace it.

---

## Changing the structure

Adding, removing, or moving a chapter shifts every number after it — and stale
references to the old numbering still *resolve*, so no check catches them.

1. **Script the renumber.** Work **descending** (11→8, then 10→7, then 9→6), and
   substitute into a sentinel you strip at the end, so no replacement cascades
   into the next rule's input. Guard `n.10` against the `n.1` pattern.
2. **Update `_quarto.yml`** — `build.ps1` will refuse to build until you do.
3. **Sweep bare `Chapter n` references by hand.** Check 5 does not show them:

   ```powershell
   python -c "import io,re;t=io.open('REPORT.md',encoding='utf-8').read();ch=dict(re.findall(r'^# CHAPTER (\d+)\.\s+(.+)$',t,re.M));[print(m,'->',ch.get(m,'MISSING')) for m in sorted(set(re.findall(r'Chapters?\s+(\d+)',t)))]"
   ```

4. **Check for orphans.** A dropped chapter can leave acronyms nothing uses and
   promises nothing fulfils.
5. **Re-run the checks, read gate 5, rebuild,** and confirm the rendered heading
   sequence.

---

## Working with a co-author

The repository is self-contained: your co-author clones it, installs Quarto and
Python, and can build, render, and check without anything from your machine.

Agree three things up front:

1. **Changes come back as edits to `REPORT.md`**, never as a marked-up `.docx`.
2. **Both of you run the checks before handing work back** — and read gate 5.
3. **Who owns which chapters**, so you are not editing the same file at the same
   time. `[P]`-style parallelism is fine for *writing*; it is still one file in
   git, so coordinate.

---

## Decisions you have to make

This template deliberately leaves three open, because the right answer depends on
your funder and your project's history.

### 1. Citation style

The format prescribes **"Literature Cited", alphabetical by author**. This
template ships **IEEE numeric `[n]`** under a "References" heading.

The reason is check 7: it validates IEEE numeric only. An author-year list
registers as zero entries and *silently* disables the dangler, orphan, and gap
checks — you would get a clean report that checked nothing.

Pick one and record it:

- **Keep IEEE** — a declared departure. Note it in the `REPORT.md` header and
  here in your README. Some funders accept it; ask rather than assume.
- **Switch to author-year** — compliant with the letter of the format. If you do,
  drop check 7 from your routine rather than letting it report a false clean.

### 2. Are they 6Ps or 7Ps?

**Six.** The DOST form's own definition names Publication, Patent/Intellectual
Property, Product, People Service, Place and Partnership, and Policy — and its
table has six rows.

The narrative format's prose *reads* as seven because it gives two examples of
People Service ("people trained and graduated, public service provided"). Some
projects report "7Ps" and have been accepted. If yours does, split §6.4, retitle
the chapter, and declare the departure.

### 3. Do the attached forms belong in the report?

The format lists "Attachments" (Forms 8, 11, 12 — and for the annual, 6 and 9) as
a part of the report. In practice they are separate documents submitted alongside
it.

The skeletons include the part. If your project omits it, **declare that** in the
`REPORT.md` header and your README rather than leaving a reviewer to wonder.

---

## What's in the repository

```
REPORT.md                    ← you write this, and nothing else
_quarto.yml                  title page + chapter list
build.ps1                    splits REPORT.md into chapter files
init.ps1                     one-time format setup
reference.docx               Arial 11 + chapter page breaks
patch-reference-docx.py      regenerates that
requirements.txt             matplotlib, for figures only
tools/report-check.py        the nine checks
figures/make_figures.py      figure generator
templates/semi-annual/       Form 6 skeleton + _quarto.yml
templates/annual/            Form 7 skeleton + _quarto.yml
docs/                        the format reference
.specify/                    optional governance — see below
```

**Not tracked** (all reproducible): `*.qmd`, `_output/`, `output/`, `assets/`,
`*.bak`.

---

## Troubleshooting

**"Chapter(s) generated but NOT listed in `_quarto.yml`"**
Working as designed. You added a chapter; add the filename it names to the
`chapters:` list, in the position you want it. Without this guard the chapter
would simply be absent from your document with no warning.

**"Two headings produce the same chapter file"**
Two chapter titles reduce to the same filename, and the second would overwrite
the first. Rename one.

**A chapter is missing from the Word document, and there was no error**
You are running an older `build.ps1` without the guard, or you edited a `.qmd`
directly. Rebuild from `REPORT.md`.

**My edits disappeared**
You edited the `.docx` or a `.qmd`. Both are regenerated every build. Only
`REPORT.md` persists. See [The one rule](#the-one-rule).

**Headings render as "3. 3.1 Methodology"**
Something bypassed the numbering strip. Run `.\build.ps1` rather than editing
`.qmd` files by hand.

**The document is not in Arial 11**
`reference.docx` is missing or unpatched:

```powershell
pandoc -o reference.docx --print-default-data-file reference.docx
python patch-reference-docx.py reference.docx
```

Verify — this should print `0`:

```powershell
python -c "import zipfile,re; x=zipfile.ZipFile('reference.docx').read('word/styles.xml').decode(); print(len([f for f in re.findall(r'<w:rFonts\b[^>]*/>',x) if 'Arial' not in f]))"
```

**"Word cannot save" / the copy fails**
The document is open in Word, which locks it. Close it and retry — do not force.

**A test that deliberately fails leaves junk behind**
`build.ps1` stops on error, which aborts anything chained after it in the same
command line. Run cleanup as a separate command, or wrap the build in
`try`/`catch`.

**`python` is not recognised**
On Windows, try `py` instead, or reinstall Python with *Add to PATH* ticked.

---

## Governance (optional)

`.specify/` holds a **constitution** — seven principles covering single source of
truth, format compliance, evidence before assertion, and structural change —
plus templates for a spec-driven workflow.

You can ignore it entirely; nothing in the build depends on it. It is there
because the failure modes it encodes are the ones that actually cost time. If you
keep it, fill in the project name and ratification date, and amend it when
practice changes. A governance document that no longer describes how the project
works is worse than none.

---

## Contributing

Useful contributions, roughly in order:

1. **Corrections to the format skeletons.** If your funder's current Form 6 or 7
   differs from
   [`docs/dost-format-reference.md`](docs/dost-format-reference.md), that is the
   most valuable thing you can report. **The annual skeleton in particular was
   derived from a form comparison and has not been validated against an accepted
   annual submission.**
2. **Cross-platform fixes.** Tested on Windows only.
3. **New checks** — especially the acronym-list and list-of-figures
   reconciliations, which are known gaps.

MIT licensed. See [LICENSE](LICENSE).
