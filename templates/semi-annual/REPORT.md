---
title: "Semi-Annual Progress Report"
project_title: "TO BE COMPLETED"
program_title: "TO BE COMPLETED — omit if the project is not part of a program"
project_leader: "TO BE COMPLETED"
implementing_agency: "TO BE COMPLETED"
cooperating_agency: "TO BE COMPLETED"
funding_agency: "TO BE COMPLETED"
project_duration: "TO BE COMPLETED"
reporting_period: "TO BE COMPLETED"
tr_completion: "TO BE COMPLETED — years of TR completion"
total_budget: "TO BE COMPLETED"
format_basis: "DOST Format of the Semi-Annual Progress Report (Form 6)"
status: skeleton
---

<!-- ============================================================================
     CANONICAL SOURCE. The only file you author by hand.

     build.ps1 regenerates the .qmd chapter files from this file, and Quarto
     renders those. Everything else is machinery or a generated artefact.

     EDITS MADE IN THE RENDERED .docx ARE DESTROYED ON THE NEXT BUILD. If a
     reviewer marks up the Word file, port the change back here before
     rebuilding, or it is lost. There is no recovery.

       Build:  .\build.ps1  then  quarto render --to docx
       Check:  python tools\report-check.py REPORT.md

     STRUCTURE follows the DOST Format of the Semi-Annual Progress Report.
     Mapping from the DOST item numbers to this file:

       Preliminary  Title page ......... _quarto.yml title block
                    Summary sheet ...... PROJECT SUMMARY
                    Lists .............. LIST OF TABLES… / LIST OF ACRONYMS…
       1            Introduction ....... Chapter 1
       2            Review of lit ...... Chapter 2   (a)-(e) are §2.1-§2.5
       3            Scientific basis ... Chapter 3
       4            Methodology ........ Chapter 4   (a)-(e) are §4.1-§4.5
       5A           Results/findings ... Chapter 5
       5B           Outputs (6Ps) ...... Chapter 6
       5C           Outcomes ........... Chapter 7
       5D           Impacts (2Is) ...... Chapter 8
       6            Literature Cited ... References
                    Appendices ......... APPENDICES
                    Problems ........... PROBLEMS
                    Raw data ........... RAW DATA
                    Attachments ........ ATTACHMENTS

     Every numbered chapter is a DOST item and every DOST item is a chapter.
     Keep it that way — it is the cheapest structure for a reviewer to verify.

     CONVENTIONS THE BUILD DEPENDS ON:
       * one "# CHAPTER n. TITLE" per chapter, numbered contiguously
       * "## n.m Title" sections, contiguous within each chapter
       * "### Title" below that, never numbered by hand
       * a top-level heading WITHOUT "CHAPTER n." is treated as front or back
         matter and renders unnumbered — that rule is derived, not configured
       * never a bolded "**n.m Title**" — it is not a heading, it will not reach
         the table of contents, and it survives renumbering with the old number

     The format's note applies throughout: for non-R&D projects, items that are
     not applicable need not be provided. Where an item does not apply, SAY SO
     AND SAY WHY rather than deleting the heading — a reviewer cannot tell a
     deliberate omission from an oversight.
     ========================================================================= -->

# PROJECT SUMMARY

<!-- DOST preliminary page: the summary sheet. Required fields:
       Project Title
       Project Leader
       Implementing Agency
       Cooperating Agency/ies      — distinct from the funding agency
       Project Duration
       Source of Fund
       Total Budget                — the TOTAL, not the yearly split

     A table is the conventional presentation. Fill from the frontmatter above
     so the two cannot drift apart. -->

# LIST OF TABLES, FIGURES, AND ILLUSTRATIONS

<!-- Compile LAST, once the figure set is final. Every entry must correspond to
     a file in assets/. Gate 8 verifies that referenced figures exist on disk,
     but nothing verifies that this list matches them — reconcile it by hand.

     If the report carries no tables or figures, say so here rather than
     leaving the page blank. -->

# LIST OF ACRONYMS AND ABBREVIATIONS

<!-- Two columns, alphabetical by acronym. Expand every acronym here AND at
     first use in the text.

     Do not carry an acronym the text never uses. Nothing checks this
     automatically; it is a manual reconciliation before submission, and it is a
     common source of stale entries after a restructure. -->

# CHAPTER 1. INTRODUCTION

<!-- DOST item 1. A formally written declaration of the project: its idea and
     context, the goals and objectives to be reached, why the project is needed,
     and the amount of work planned for implementation. Written so it can double
     as communication material. -->

## 1.1 Background and Rationale

<!-- The problem the project answers to, and the mandate it operates under. Name
     the program objective and the funding authority this report answers to.
     State the reporting period in the first paragraph. -->

## 1.2 Purpose and Objectives

<!-- Numbered objectives, each one something this report can be judged against.
     Trace them to the approved workplan rather than restating them loosely —
     Chapter 5 compares accomplishments against exactly these. -->

## 1.3 Scope and Delimitations

<!-- What the period covers and what it does not. Where a component is at
     prototype or pilot stage rather than deployed, say so here rather than
     leaving a reader to infer it. -->

## 1.4 Planned Work for the Period

<!-- The format asks the introduction to describe the amount of work planned.
     Chapter 5 then compares that plan against what was delivered, so the two
     must stay consistent. State targets in the same units both places. -->

# CHAPTER 2. REVIEW OF LITERATURE

<!-- DOST item 2. The five required elements are §2.1 to §2.5, in the order the
     format gives them. Put subject-matter surveys as ### under §2.1. -->

## 2.1 Related Research and Current Technologies

<!-- Format element (a): related research already conducted, and the current
     technologies the project takes off from. Add ### subsections per topic.

     A literature section restated unchanged across reporting periods earns
     nothing — say what has moved since the last report. -->

## 2.2 Scientific and Technical Merit

<!-- Format element (b). State what is scientifically or technically new, and
     against what baseline. -->

## 2.3 Related Research by the Project Leader

<!-- Format element (c). Prior work by the project leader bearing on this
     project. If there is none for the period, say so plainly rather than
     omitting the section. -->

## 2.4 Prior Art Search

<!-- Format element (d). Record the databases searched, the search date, the
     query terms, and what was found. A prior art search with no method stated
     is not a prior art search. Feeds the patents line of Chapter 6. -->

## 2.5 Other Relevant Materials

<!-- Format element (e). -->

# CHAPTER 3. SCIENTIFIC BASIS AND THEORETICAL FRAMEWORK

<!-- DOST item 3. The scientific findings, conclusions, or assumptions used to
     justify the research, and the structure of concepts and theories that the
     data analysis and interpretation rest on.

     Add ## 3.1, ## 3.2 … sections for the domains your project draws on. -->

## 3.1 <Domain or Theoretical Basis>

## 3.2 <Domain or Theoretical Basis>

## 3.3 Ethics and Governance

<!-- Where personal data is involved, cite the applicable data-privacy statute
     and state who holds the data and how it is minimised. -->

# CHAPTER 4. METHODOLOGY

<!-- DOST item 4. Sections 4.1 to 4.5 are the format's elements (a) to (e), in
     order; §4.6 is the "strategies for implementation" the format attaches to
     element (e). Sections 4.7 and 4.8 are retained good practice, not required.

     Several of these use experimental-design language that may not fit a
     development or systems project. Where an element does not apply, keep the
     heading, state that it does not apply, and name what stands in its place. -->

## 4.1 Variables and Parameters Measured

<!-- Format element (a): what is measured, evaluated, or analysed. -->

## 4.2 Treatments and Layout

<!-- Format element (b). Experimental-design language. For a non-experimental
     project, state non-applicability and name the analogue — benchmark
     configurations, pilot cohorts, deployment sites. -->

## 4.3 Procedures and Design

<!-- Format element (c): experimental procedures and design. -->

## 4.4 Statistical Analysis

<!-- Format element (d). Name the tests and the software. The statistical-formula
     appendix depends on this section. -->

## 4.5 Evaluation Method and Observations

<!-- Format element (e): the evaluation method and the observations to be made. -->

## 4.6 Strategies for Implementation

<!-- The conceptual and analytical framework, plus the project timeline and
     technology roadmap. Show where the project stands against the approved
     roadmap at the close of the period — including slippage. -->

## 4.7 Data Handling, Privacy, and Ethics

<!-- Retained beyond the format. Name the applicable statute and who holds the
     data. -->

## 4.8 Limitations

<!-- Retained beyond the format. Enumerate. Each limitation should constrain how
     a finding may be read, not merely disclose that a shortcoming exists. -->

# CHAPTER 5. DISCUSSION OF RESULTS AND FINDINGS

<!-- DOST item 5A: data gathered, analysis, and interpretation of results,
     supported by tables, graphs, pictures, and maps — including the comparison
     of targeted against actual research and development output. -->

## 5.1 Data Gathered

<!-- Present the data. Every figure needs a caption stating what it shows and a
     sentence tying it to the argument. A figure with no argument attached is
     decoration. -->

## 5.2 Analysis and Interpretation

## 5.3 Targeted Versus Actual Output

<!-- The format requires this comparison explicitly. Compare against the targets
     stated in §1.4.

     Report shortfalls as shortfalls. A target quietly restated to match the
     outcome is the failure mode here, and a reviewer holding the approved
     workplan will see it. -->

# CHAPTER 6. OUTPUTS (6Ps)

<!-- DOST item 5B. The 6Ps, per the DOST form's own Operational Definition of
     Terms: Publication, Patent/Intellectual Property, Product, People Service,
     Place and Partnership, and Policy. Those six are §6.1 to §6.6 below.

     A NOTE ON "6Ps" vs "7Ps". The narrative format's prose lists the categories
     loosely — "…people trained and graduated, public service provided…" — which
     reads as seven. It is not: those are two examples of ONE P, People Service.
     Some projects nonetheless report "7Ps" and have been accepted. If yours
     does, split §6.4 and retitle the chapter, and record the departure in the
     header above and in your README — do not leave it undeclared.

     Proof of every output goes in the APPENDICES. An output claimed here
     without proof there is the first thing a reviewer will find. -->

## 6.1 Publications

<!-- Published aspect of the research, or the whole of it, in a peer-reviewed
     venue. -->

## 6.2 Patents and Intellectual Property

<!-- Proprietary invention or scientific process. Ties to the prior art search
     in §2.4. -->

## 6.3 Products

## 6.4 People Services

<!-- People trained and graduated, and public service provided. Both belong to
     this single P. -->

## 6.5 Places and Partnerships

<!-- Facilities and partnerships established. A partnership listed without an
     output is a name, not a result. -->

## 6.6 Policies

<!-- Science-based policy crafted and adopted by government or academe as a
     result of the study. -->

# CHAPTER 7. OUTCOMES

<!-- DOST item 5C: the change in practices, behaviour, skills, attitude,
     institutions, government policy and plans, and accessibility to programs
     resulting from the project's interventions or outputs.

     An outcome is a change in someone else's behaviour. An activity the project
     itself ran is an output and belongs in Chapter 6. -->

## 7.1 Changes in Practices, Behaviour, and Skills

## 7.2 Changes in Institutions, Policy, and Plans

## 7.3 Changes in Accessibility to Programs and Services

# CHAPTER 8. POTENTIAL IMPACTS (2Is)

<!-- DOST item 5D: the potential social and economic impacts. The format states
     that the theory of change carried from the proposal is what makes potential
     impacts determinable — so §8.3 is what the other two rest on, not an
     afterthought. -->

## 8.1 Potential Social Impacts

## 8.2 Potential Economic Impacts

## 8.3 Theory of Change

<!-- Carry this from the approved proposal. State the causal chain from outputs
     to outcomes to impacts, and the assumptions each link depends on. Impacts
     asserted without that chain are not projections. -->

# References

<!-- DOST item 6, "Literature Cited". The format prescribes references listed
     ALPHABETICALLY BY AUTHOR: author, year, title, edition (if a book), place
     of publication, publisher or journal name, page numbers (if an article).

     THIS TEMPLATE SHIPS IEEE NUMERIC [n] INSTEAD, and the heading is
     "References" rather than "Literature Cited", because gate 7 validates IEEE
     numeric only — it catches citations that are cited but unlisted, listed but
     never cited, and gaps in the numbering. An author-year list registers as
     zero entries and silently disables all three checks.

     Pick one and be deliberate:
       * Keep IEEE numeric — a declared departure from the format. Record it in
         the header above and in your README. Some funders accept it; some do
         not. Ask before assuming.
       * Switch to alphabetical author-year — compliant with the letter of the
         format, but you lose gate 7. If you do this, delete gate 7 from your
         verification routine rather than letting it report a false clean.

     IEEE format:
       [1] <Author>, "<Title>," <Publisher/Journal>, <Year>. [Online].
           Available: <URL>

     Add an entry only once something cites it — an uncited entry is an orphan
     and fails the gate. -->

# APPENDICES

<!-- The DOST format requires these four. Keep all four headings; where one does
     not apply, say so and say why. -->

## Statistical Formula and Analysis

<!-- Ties to §4.4. -->

## Sample Questionnaire, Survey Form, and Interview Schedule

<!-- Reproduce the blank instrument, not completed responses. Completed
     responses carry personal data and belong under RAW DATA, held outside the
     repository. -->

## Report of Income Generated

<!-- State "none for the period" if that is the case. Do not omit the heading. -->

## Proof of 6Ps

<!-- Copy of publication, patent application, signed MOU, policy issuance, and
     the rest — one per output claimed in Chapter 6. -->

# PROBLEMS

<!-- Cite ALL technical and administrative problems encountered, each with a
     recommended solution. A problem stated without a recommended solution does
     not satisfy the format.

     Include explanatory notes for deviations between targets and
     accomplishments, and any change in implementation dates. -->

# RAW DATA

<!-- Results of laboratory analysis and survey questionnaires, submitted upon
     request of the funding agency.

     Check every source file for personal data before it enters this repository.
     Survey and workshop exports routinely carry names, emails, and
     demographics. Keep aggregates here, hold identifiable data outside the
     repository, and record the handling decision alongside the data. -->

# ATTACHMENTS

<!-- The DOST format lists these as a part of the report. They are separate
     forms, not sections you draft here — this page records their status and
     transmittal.

     Some projects treat the forms purely as submission deliverables and omit
     this part entirely. That is defensible, but DECLARE IT if you do: in the
     header above, in your README, and to whoever assembles the submission. -->

## DOST Form No. 8 — Semi-Annual Financial Report

## DOST Form No. 11 — List of Personnel Involved

## DOST Form No. 12 — List of Equipment Purchased

<!-- Include the Property Acknowledgement Receipt (PAR) for each item. -->
