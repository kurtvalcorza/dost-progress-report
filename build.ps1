#requires -version 5
<#
.SYNOPSIS
  Split the canonical Markdown report into per-chapter Quarto .qmd files.

.DESCRIPTION
  REPORT.md is the SINGLE SOURCE OF TRUTH. This script keeps no second copy — it
  regenerates the .qmd chapter files from the source at build time. Edit the
  source, re-run this, then `quarto render`.

  Chapter slugs are DERIVED from the headings, and the emitted set is CHECKED
  against _quarto.yml. A chapter you add to the source but forget to list in
  _quarto.yml is a hard error here, not a silent omission from the render.

  Transformations:
    * split on each top-level "# " heading -> one .qmd per chapter
    * strip manual "CHAPTER N." and "N.M " numbering so Quarto auto-numbers
      (prevents "4. 4.1 Foo")
    * mark front and back matter {.unnumbered} — see -Unnumbered below
    * mirror <source-dir>/assets/ when the source lives elsewhere

.PARAMETER Source
  Path to the canonical .md file. Defaults to REPORT.md beside this script, so
  the script runs with no arguments.

.PARAMETER OutDir
  Quarto project directory. Defaults to the script's own directory.

.PARAMETER Unnumbered
  Headings to render without a chapter number. LEAVE THIS EMPTY — by default the
  rule is derived: any top-level heading that is not "# CHAPTER n. ..." is front
  or back matter and renders unnumbered. Pass an explicit list only to override
  that for a report using a different convention.
#>
[CmdletBinding()]
param(
  [string]$Source = (Join-Path $PSScriptRoot 'REPORT.md'),
  [string]$OutDir = $PSScriptRoot,
  [string[]]$Unnumbered = @()
)

$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Source)) {
  throw ("Source not found: $Source`n" +
         "Run .\init.ps1 to choose a report format first.")
}

# --- assets mirror -----------------------------------------------------------
# When the source lives outside this directory, mirror its assets/ here so one
# relative path resolves in both places. When source and build share a
# directory, copying a file onto itself throws — skip.
$srcDir = (Resolve-Path -LiteralPath (Split-Path -Parent $Source)).Path
$sameDir = $srcDir -eq (Resolve-Path -LiteralPath $OutDir).Path
$srcAssets = Join-Path $srcDir 'assets'
if ($sameDir) {
  Write-Host "  assets: source and build share a directory, no mirror needed"
}
elseif (Test-Path -LiteralPath $srcAssets) {
  $dstAssets = Join-Path $OutDir 'assets'
  if (-not (Test-Path -LiteralPath $dstAssets)) {
    New-Item -ItemType Directory -Path $dstAssets | Out-Null
  }
  $figs = Get-ChildItem -LiteralPath $srcAssets -File |
          Where-Object { $_.Name -ne 'desktop.ini' }   # file-sync clients inject these
  foreach ($f in $figs) { Copy-Item -LiteralPath $f.FullName -Destination $dstAssets -Force }
  Write-Host ("  mirrored {0} asset(s)" -f $figs.Count)
}

function Get-Slug([string]$title) {
  $s = $title -replace '^CHAPTER\s+\d+\.\s*', ''
  $s = $s.ToLower() -replace '[^a-z0-9]+', '-'
  return ($s.Trim('-'))
}

# --- split -------------------------------------------------------------------
$lines = Get-Content -LiteralPath $Source -Encoding UTF8
$blocks = New-Object System.Collections.Generic.List[object]
$cur = $null
foreach ($line in $lines) {
  if ($line -match '^#\s') {
    if ($null -ne $cur) { $blocks.Add($cur) }
    $cur = New-Object System.Collections.Generic.List[string]
  }
  if ($null -ne $cur) { $cur.Add($line) }
}
if ($null -ne $cur) { $blocks.Add($cur) }
if ($blocks.Count -eq 0) { throw "No '# ' headings found in $Source" }

$utf8 = New-Object System.Text.UTF8Encoding($false)   # no BOM
$emitted = New-Object System.Collections.Generic.List[string]
$seen = @{}          # slug -> heading, for the collision guard

$first = $true
foreach ($b in $blocks) {
  $head = $b[0] -replace '^#\s+', ''
  $slug = Get-Slug $head

  # Collision guard. Two headings reducing to the same filename would silently
  # overwrite — the same class of loss the _quarto.yml guard exists to prevent,
  # arriving by a different route.
  if ($seen.ContainsKey($slug)) {
    throw ("Two headings produce the same chapter file '$slug.qmd' — the second " +
           "would silently overwrite the first:`n" +
           "    $($seen[$slug])`n    $head`n" +
           "Rename one so their slugs differ.")
  }
  $seen[$slug] = $head

  # Quarto's book project requires its first chapter to be index.qmd.
  $file = if ($first) { 'index.qmd' } else { "$slug.qmd" }
  $first = $false

  # Derived rule: a top-level heading that is not "CHAPTER n." is front or back
  # matter, so it renders without a number. An explicit -Unnumbered overrides.
  $isUn = if ($Unnumbered.Count -gt 0) { $Unnumbered -contains $head }
          else { $head -notmatch '^CHAPTER\s+\d+\.' }

  $title = $head -replace '^CHAPTER\s+\d+\.\s*', ''
  # ALL-CAPS heading -> Title Case, with small words lowered after the first and
  # common acronyms restored. Without this, "REVIEW OF LITERATURE" renders as
  # "Review Of Literature", and a heading carrying a lowercase-suffixed acronym
  # ("OUTPUTS (6Ps)") is skipped entirely and stays shouting beside its siblings.
  if ($title -cnotmatch '[a-z]{2,}') {
    $ti = (Get-Culture).TextInfo
    $title = $ti.ToTitleCase($title.ToLower())
    $small = 'a','an','and','as','at','but','by','for','in','nor','of','on','or','the','to','via','with'
    $words = $title -split ' '
    for ($i = 1; $i -lt $words.Count; $i++) {
      if ($small -contains $words[$i].ToLower()) { $words[$i] = $words[$i].ToLower() }
    }
    $title = $words -join ' '
    foreach ($pair in @(@('Ps','Ps'), @('Is','Is'), @('Dost','DOST'), @('R&d','R&D'))) {
      $title = $title -creplace ('\b' + $pair[0] + '\b'), $pair[1]
    }
  }

  $out = New-Object System.Collections.Generic.List[string]
  $out.Add('# ' + $title + $(if ($isUn) { ' {.unnumbered}' } else { '' }))
  foreach ($l in $b[1..($b.Count - 1)]) {
    # strip manual sub-numbering: "## 4.1 Foo" -> "## Foo"
    $out.Add(($l -replace '^(#{2,6})\s+\d+(\.\d+)*\s+', '$1 '))
  }
  [System.IO.File]::WriteAllLines((Join-Path $OutDir $file), $out, $utf8)
  $emitted.Add($file)
  Write-Host ("  wrote {0,-46} <- {1}" -f $file, $head)
}

# --- guard: emitted set must match _quarto.yml -------------------------------
$qy = Join-Path $OutDir '_quarto.yml'
if (Test-Path -LiteralPath $qy) {
  $listed = Select-String -LiteralPath $qy -Pattern '^\s*-\s+([A-Za-z0-9._-]+\.qmd)' |
            ForEach-Object { $_.Matches[0].Groups[1].Value }
  $missing = $emitted  | Where-Object { $listed -notcontains $_ }
  $stale   = $listed   | Where-Object { $emitted -notcontains $_ }
  if ($missing) {
    throw ("Chapter(s) generated but NOT listed in _quarto.yml — they would be " +
           "silently omitted from the render: " + ($missing -join ', ') + "`n" +
           "Add them to the chapters: list, in the order they should appear.")
  }
  if ($stale) {
    Write-Warning ("_quarto.yml lists .qmd file(s) the source no longer produces: " +
                   ($stale -join ', '))
  }
}
else {
  Write-Warning ("_quarto.yml not found — the silent-omission guard did not run. " +
                 "This is expected only on a first pass, to discover slugs.")
}

Write-Host ""
Write-Host ("Done: {0} chapter file(s) in {1}" -f $emitted.Count, $OutDir)
Write-Host "Next: quarto render --to docx"
