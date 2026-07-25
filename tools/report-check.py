#!/usr/bin/env python3
"""
report-check.py — structural and citation integrity gate for a long-form Markdown report.

Consolidates the checks that a multi-chapter report needs and that ordinary
link-checkers miss. Run after ANY restructuring (new chapter, renumbering,
section move) and before every render.

    python report-check.py "<path-to-report.md>" [--strict]

Exit code 0 = all gates pass; 1 = at least one gate failed (with --strict).

Checks
------
 1. Chapter sequence          contiguous CHAPTER n, no gaps
 2. Section sequence          n.1..n.k contiguous within each chapter
 3. Pseudo-headings           **4.4 Title** style bolded lines masquerading as
                              headings — invisible to heading checks and to the
                              rendered ToC, and a classic renumbering survivor
 4. Cross-reference RESOLUTION   every "Chapter n" / "Section n.m" / "§n.m" exists
 5. Cross-reference SEMANTICS    prints each ref with the TITLE it points at, so a
                              stale-but-resolvable ref (§5.3 -> wrong section) is
                              visible. THIS IS THE ONE AUTOMATION CANNOT DECIDE.
 6. Bare "Section n"          decimal-less refs that regex checks silently skip
 7. Citation gate             listed vs cited, danglers, orphans, numbering gaps;
                              ranges like [11-13] expanded numerically
 8. Figure assets             every ![](path) target exists on disk
 9. Anti-style sweep          hype and filler, with citation lines excluded
"""
import io
import os
import re
import sys
from collections import Counter

ANTI_STYLE = (r'\b(groundbreaking|revolutionary|cutting-edge|game-chang\w+|seamless\w*|'
              r'leverag\w+|delve|robust|state-of-the-art|unprecedented|transformative|'
              r'vital|crucial|paramount|it is important to note|it is worth noting)\b')

ok = True


def fail(msg):
    global ok
    ok = False
    print('  FAIL  ' + msg)


def load(path):
    return io.open(path, encoding='utf-8').read()


def expand_refs(text):
    """Citation numbers, with [11-13] / [11–13] ranges expanded."""
    c = Counter()
    for m in re.finditer(r'\[([\d\s,–—-]+)\]', text):
        for part in m.group(1).split(','):
            p = part.strip()
            r = re.match(r'^(\d+)\s*[–—-]\s*(\d+)$', p)
            if r:
                for i in range(int(r.group(1)), int(r.group(2)) + 1):
                    c[i] += 1
            elif p.isdigit():
                c[int(p)] += 1
    return c


def main(path, strict=False):
    text = load(path)
    lines = text.split('\n')
    root = os.path.dirname(os.path.abspath(path))

    chapters, sections = {}, {}
    for ln in lines:
        m = re.match(r'^# CHAPTER (\d+)\.\s+(.+)$', ln)
        if m:
            chapters[int(m.group(1))] = m.group(2).strip()
        m = re.match(r'^## (\d+)\.(\d+)\s+(.+)$', ln)
        if m:
            sections['%s.%s' % (m.group(1), m.group(2))] = m.group(3).strip()

    print('== 1-2. STRUCTURE ==')
    if not chapters:
        fail('no "# CHAPTER n. Title" headings found')
    else:
        gaps = [n for n in range(1, max(chapters) + 1) if n not in chapters]
        print('  chapters: %d (1..%d)' % (len(chapters), max(chapters)))
        if gaps:
            fail('chapter-number gaps: %s' % gaps)
        by_ch = {}
        for s in sections:
            by_ch.setdefault(int(s.split('.')[0]), []).append(int(s.split('.')[1]))
        for c in sorted(by_ch):
            nums = sorted(by_ch[c])
            if nums != list(range(1, len(nums) + 1)):
                fail('ch%d sections non-sequential: %s' % (c, nums))
        print('  sections: %d across %d chapters' % (len(sections), len(by_ch)))

    print('== 3. PSEUDO-HEADINGS ==')
    hits = [(i, l) for i, l in enumerate(lines, 1) if re.match(r'^\*\*\d+\.\d+\s', l)]
    for i, l in hits:
        fail('line %d bolded pseudo-heading (not in ToC): %s' % (i, l.strip()[:60]))
    if not hits:
        print('  none')

    print('== 4/6. CROSS-REFERENCE RESOLUTION ==')
    bad = []
    for i, ln in enumerate(lines, 1):
        for m in re.finditer(r'Chapters?\s+(\d+)(?:\s*[–-]\s*(\d+))?', ln):
            a = int(m.group(1))
            b = int(m.group(2)) if m.group(2) else a
            for n in range(a, b + 1):
                if n not in chapters:
                    bad.append((i, 'Chapter %d' % n))
        for m in re.finditer(r'(?:Section\s+|§)(\d+\.\d+)', ln):
            if m.group(1) not in sections:
                bad.append((i, 'Section %s' % m.group(1)))
        for m in re.finditer(r'Section\s+(\d+)(?!\s*\.\d)', ln):
            bad.append((i, 'bare "Section %s" - ambiguous, use Chapter n or Section n.m'
                        % m.group(1)))
    for i, r in bad:
        fail('line %d unresolved/ambiguous: %s' % (i, r))
    if not bad:
        print('  all resolve')

    print('== 5. CROSS-REFERENCE SEMANTICS (review by eye) ==')
    seen = set()
    for i, ln in enumerate(lines, 1):
        for m in re.finditer(r'(?:Section\s+|§)(\d+\.\d+)', ln):
            r = m.group(1)
            if (i, r) in seen:
                continue
            seen.add((i, r))
            s = max(0, m.start() - 50)
            print('  L%-5s %-6s -> "%s"' % (i, r, sections.get(r, '!! MISSING !!')))
            print('         ...%s' % ln[s:m.end()].strip())
    if not seen:
        print('  (no section cross-references)')

    print('== 7. CITATIONS ==')
    ridx = next((i for i, l in enumerate(lines) if re.match(r'^#+\s*References\s*$', l)), None)
    if ridx is None:
        fail('no "# References" heading')
    else:
        body = '\n'.join(lines[:ridx])
        listed = set()
        for l in lines[ridx:]:
            m = re.match(r'^\[(\d+)\]\s', l)
            if m:
                listed.add(int(m.group(1)))
        cited = set(expand_refs(body))
        dang = sorted(cited - listed)
        orph = sorted(listed - cited)
        gaps = [i for i in range(1, (max(listed) if listed else 0) + 1) if i not in listed]
        print('  listed=%d cited=%d' % (len(listed), len(cited)))
        if dang:
            fail('danglers (cited, not listed): %s' % dang)
        if orph:
            fail('orphans (listed, never cited): %s' % orph)
        if gaps:
            fail('numbering gaps: %s' % gaps)
        if not (dang or orph or gaps):
            print('  0 danglers / 0 orphans / 0 gaps')

    print('== 8. FIGURE ASSETS ==')
    figs = re.findall(r'!\[[^\]]*\]\(([^)\s]+)', text)
    for f in figs:
        p = os.path.join(root, f.replace('/', os.sep))
        if os.path.exists(p):
            print('  ok   %s (%d bytes)' % (f, os.path.getsize(p)))
        else:
            fail('missing asset: %s' % f)
    if not figs:
        print('  (no figures)')

    print('== 9. ANTI-STYLE (citation lines excluded) ==')
    found = Counter()
    for i, ln in enumerate(lines, 1):
        if re.match(r'^\[\d+\]\s', ln) or 'http' in ln:
            continue          # reference entries legitimately quote vendor titles
        for m in re.finditer(ANTI_STYLE, ln, re.I):
            found[m.group(0).lower()] += 1
            print('  L%-5s %s' % (i, m.group(0)))
    if not found:
        print('  clean')

    print('\n== RESULT: %s ==' % ('PASS' if ok else 'FAIL'))
    return 0 if (ok or not strict) else 1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.exit(main(sys.argv[1], '--strict' in sys.argv))
