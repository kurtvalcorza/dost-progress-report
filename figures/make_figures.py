"""
Report figure generator.

Writes PNG into this repository's assets/. REPORT.md references figures by the
relative path assets/<name>.png, which resolves the same in an editor and in the
render.

Run it with no arguments:

    python figures/make_figures.py

Override the destination with --out, or the REPORT_ASSETS environment variable.

WHY GENERATE FIGURES INSTEAD OF DRAWING THEM
--------------------------------------------
A figure that exists only as an exported image cannot be reviewed, corrected, or
reproduced when the underlying number changes — someone has to remember which
spreadsheet it came from. A figure that is code can be re-run, diffed, and
checked by whoever reviews the report.

assets/ is gitignored: figures are reproducible from this script, so they are
not tracked. Anyone who clones the repository runs this to get them.

PNG, NOT SVG
------------
Pandoc cannot size SVG without rsvg-convert installed, and an unsized SVG renders
unpredictably in Word. Use PNG at ~200 dpi.

CONVENTIONS THE EXAMPLE BELOW DEMONSTRATES
------------------------------------------
  * muted palette, one accent colour, no chart junk
  * caption text carried under the axes rather than in a floating legend
  * a stated source line, so the figure carries its own provenance
  * top and right spines removed

REPLACE THE EXAMPLE with your report's own figures. It is a placeholder using
invented numbers and is labelled as such in the figure itself, so that a
placeholder can never be mistaken for a finding if it reaches a draft.
"""
import argparse
import io
import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Default to <repo root>/assets — this file lives in <repo root>/figures/.
_DEFAULT_OUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')

_ap = argparse.ArgumentParser(
    description="Generate the report's figures as PNG into assets/.")
_ap.add_argument('--out', default=os.environ.get('REPORT_ASSETS', _DEFAULT_OUT),
                 help='destination assets directory (default: <repo root>/assets)')
_args, _ = _ap.parse_known_args()
OUT = _args.out
os.makedirs(OUT, exist_ok=True)

WROTE = []   # only what this run produced, so the summary cannot over-report

INK = '#1f2937'      # near-black text
MUTED = '#6b7280'    # secondary text
RULE = '#9ca3af'     # axes and rules
ACCENT = '#1d4ed8'
FILL = '#dbeafe'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'text.color': INK,
    'axes.edgecolor': RULE,
    'axes.labelcolor': INK,
    'xtick.color': MUTED,
    'ytick.color': MUTED,
    'savefig.dpi': 200,
    'savefig.bbox': 'tight',
})

# --------------------------------------------------------------- Example figure
# Targeted vs actual output by objective — the comparison DOST item 5A requires.
# The numbers are invented. Replace them, and delete the PLACEHOLDER banner.

objectives = ['Objective 1', 'Objective 2', 'Objective 3', 'Objective 4']
targeted = [12, 8, 20, 5]
actual = [12, 5, 21, 2]

fig, ax = plt.subplots(figsize=(6.8, 3.6))
y = range(len(objectives))
h = 0.36

ax.barh([i + h / 2 for i in y], targeted, height=h, color=FILL,
        edgecolor='none', label='Targeted', zorder=2)
ax.barh([i - h / 2 for i in y], actual, height=h, color=ACCENT,
        edgecolor='none', label='Actual', zorder=2)

for i, (t, a) in enumerate(zip(targeted, actual)):
    ax.text(t + 0.4, i + h / 2, str(t), va='center', fontsize=8.4, color=MUTED)
    ax.text(a + 0.4, i - h / 2, str(a), va='center', fontsize=8.4, color=INK,
            fontweight='bold')

ax.set_yticks(list(y))
ax.set_yticklabels(objectives, fontsize=9)
ax.invert_yaxis()
ax.set_xlabel('Deliverables', fontsize=9.5, labelpad=8)
ax.set_xlim(0, max(targeted + actual) * 1.18)
for s in ('top', 'right', 'left'):
    ax.spines[s].set_visible(False)
ax.tick_params(length=3)
ax.legend(frameon=False, fontsize=8.6, loc='lower right', ncol=2)

# The caption sits below the x-axis label. With savefig.bbox='tight', both are
# placed in figure coordinates and WILL overlap if the caption is too close —
# the axis label and the first caption line land on top of each other and the
# figure is unreadable. Leave enough clearance, and look at the PNG after any
# change to either. This exact collision shipped once.
fig.text(0.5, -0.17,
         'PLACEHOLDER — invented numbers, for layout only. Replace before use.\n'
         'Shortfalls against Objectives 2 and 4 are shown as shortfalls; explain each\n'
         'in the PROBLEMS part with a recommended solution, as the format requires.',
         ha='center', fontsize=8, color=MUTED, linespacing=1.5)

_p = os.path.join(OUT, 'fig-01-targeted-vs-actual.png')
fig.savefig(_p, facecolor='white')
WROTE.append(_p)
plt.close(fig)

# Console-safe: a destination path may contain non-cp1252 characters, which
# crash stdout on a Windows code page.
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
print('wrote %d figure(s) to %s' % (len(WROTE), OUT))
for p in WROTE:
    print('   %-34s %7d bytes' % (os.path.basename(p), os.path.getsize(p)))
print('\nNOTE: this is a PLACEHOLDER with invented numbers, shipped to show the')
print('      conventions. Replace it before referencing any figure in REPORT.md.')
