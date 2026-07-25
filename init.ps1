#requires -version 5
<#
.SYNOPSIS
  Choose a report format and set the project up to build.

.DESCRIPTION
  Copies the chosen format's REPORT.md and _quarto.yml from templates/ into the
  repository root, generates the Arial 11 reference document, and tells you what
  to do next.

  Run this once, first. After that you never need it again — you author
  REPORT.md and run build.ps1.

.PARAMETER Format
  'semi-annual' (DOST Form 6) or 'annual' (DOST Form 7).

.PARAMETER Force
  Overwrite an existing REPORT.md. Refused by default — REPORT.md is the single
  source of truth and overwriting it destroys your writing.

.EXAMPLE
  .\init.ps1 -Format semi-annual
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [ValidateSet('semi-annual', 'annual')]
  [string]$Format,
  [switch]$Force
)

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$src = Join-Path $root "templates\$Format"

if (-not (Test-Path -LiteralPath $src)) { throw "No template for format '$Format' at $src" }

$report = Join-Path $root 'REPORT.md'
if ((Test-Path -LiteralPath $report) -and -not $Force) {
  throw ("REPORT.md already exists. It is the single source of truth — " +
         "overwriting it would destroy your writing.`n" +
         "If you are certain, re-run with -Force. Consider committing first.")
}

Copy-Item (Join-Path $src 'REPORT.md')   $report -Force
Copy-Item (Join-Path $src '_quarto.yml') (Join-Path $root '_quarto.yml') -Force
Write-Host "  copied REPORT.md and _quarto.yml for the $Format format"

# --- reference document: Arial 11 + chapter page breaks ----------------------
$ref = Join-Path $root 'reference.docx'
if (-not (Test-Path -LiteralPath $ref)) {
  if (-not (Get-Command pandoc -ErrorAction SilentlyContinue)) {
    Write-Warning ("pandoc not found, so reference.docx was not generated. " +
                   "Install Quarto (it bundles pandoc), then run:`n" +
                   "    pandoc -o reference.docx --print-default-data-file reference.docx`n" +
                   "    python patch-reference-docx.py reference.docx")
  }
  else {
    Push-Location $root
    try {
      pandoc -o reference.docx --print-default-data-file reference.docx
      python patch-reference-docx.py reference.docx | ForEach-Object { "  $_" }
    }
    finally { Pop-Location }
  }
}
else {
  Write-Host "  reference.docx already present, left alone"
}

Write-Host ""
Write-Host "Ready. Next:"
Write-Host "  1. Fill the frontmatter in REPORT.md and the title block in _quarto.yml"
Write-Host "  2. .\build.ps1"
Write-Host "  3. quarto render --to docx"
Write-Host "  4. python tools\report-check.py REPORT.md   (and READ gate 5)"
Write-Host ""
Write-Host "See README.md for the full guide."
