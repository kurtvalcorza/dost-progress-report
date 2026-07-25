#!/usr/bin/env python3
"""
patch-reference-docx.py — apply the DOST house format to the DOCX reference doc.

Typography and page breaks come from the reference doc, NOT from the Markdown
source. Pandoc's default reference.docx uses the theme font at 12 pt and has no
page break on Heading1, so chapters run on and the font fails the DOST general
instruction ("Use Arial font, 11 font size").

Two patches, both inside word/styles.xml:

  1. Arial 11 as the document default (w:docDefaults), plus every style that
     pins a font or size of its own — otherwise headings and the ToC keep the
     theme font while body text changes, which is worse than not patching.
  2. <w:pageBreakBefore/> on Heading1 and TOCHeading so each chapter starts on
     a new page.

    python patch-reference-docx.py [reference.docx]

The element order inside <w:pPr> is fixed by the OOXML schema — pStyle, keepNext,
keepLines, pageBreakBefore, ... — and a wrong position silently breaks the style
rather than raising an error. This script inserts after keepLines/keepNext/pStyle
(whichever is last present) rather than at a hardcoded index.

Sizes are in half-points: 11 pt = w:sz 22.

Idempotent: re-running on an already-patched file changes nothing.
"""
import io
import re
import shutil
import sys
import zipfile

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
TARGET_STYLES = ('Heading1', 'TOCHeading')
# Schema order inside <w:pPr>; pageBreakBefore goes after the last of these.
PRECEDING = ('pStyle', 'keepNext', 'keepLines')

FONT = 'Arial'
SIZE_HALF_POINTS = '22'          # 11 pt
RFONTS = ('<w:rFonts w:ascii="%s" w:hAnsi="%s" w:eastAsia="%s" w:cs="%s"/>'
          % (FONT, FONT, FONT, FONT))


def set_font(xml):
    """Force Arial 11 everywhere a font or size is declared.

    Headings keep their own w:sz so they stay larger than body text; only the
    typeface is rewritten there. The document default carries the 11 pt size.
    """
    # 1. Replace every rFonts declaration (docDefaults and per-style alike).
    xml, n_fonts = re.subn(r'<w:rFonts\b[^>]*/>', RFONTS, xml)

    # 2. Document default size -> 11 pt. Only inside docDefaults, so heading
    #    sizes are left alone.
    def fix_defaults(m):
        block = m.group(0)
        block = re.sub(r'<w:sz w:val="\d+"\s*/>',
                       '<w:sz w:val="%s"/>' % SIZE_HALF_POINTS, block)
        block = re.sub(r'<w:szCs w:val="\d+"\s*/>',
                       '<w:szCs w:val="%s"/>' % SIZE_HALF_POINTS, block)
        return block

    xml, n_def = re.subn(r'<w:docDefaults\b.*?</w:docDefaults>', fix_defaults,
                         xml, flags=re.S)
    return xml, n_fonts, n_def


def patch_ppr(ppr):
    """Insert <w:pageBreakBefore/> into one <w:pPr> block at the schema position."""
    if 'w:pageBreakBefore' in ppr:
        return ppr, False
    pos = ppr.index('>') + 1          # just after the opening <w:pPr ...>
    for tag in PRECEDING:
        for m in re.finditer(r'<w:%s\b[^>]*?(?:/>|>.*?</w:%s>)' % (tag, tag), ppr, re.S):
            pos = max(pos, m.end())
    return ppr[:pos] + '<w:pageBreakBefore/>' + ppr[pos:], True


def patch_styles(xml):
    patched = []

    def repl(m):
        block = m.group(0)
        sid = re.search(r'w:styleId="([^"]+)"', block)
        if not sid or sid.group(1) not in TARGET_STYLES:
            return block
        pm = re.search(r'<w:pPr\b.*?</w:pPr>', block, re.S)
        if pm:
            new, changed = patch_ppr(pm.group(0))
            if not changed:
                return block
            block = block[:pm.start()] + new + block[pm.end():]
        else:
            # No <w:pPr> at all — insert one after <w:name .../> if present.
            nm = re.search(r'<w:name\b[^>]*/>', block)
            at = nm.end() if nm else block.index('>') + 1
            block = (block[:at] + '<w:pPr><w:pageBreakBefore/></w:pPr>'
                     + block[at:])
        patched.append(sid.group(1))
        return block

    xml = re.sub(r'<w:style\b.*?</w:style>', repl, xml, flags=re.S)
    return xml, patched


def main(path='reference.docx'):
    shutil.copyfile(path, path + '.bak')
    with zipfile.ZipFile(path) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]

    out, patched, fontinfo = [], [], None
    for info, data in items:
        if info.filename == 'word/styles.xml':
            xml = data.decode('utf-8')
            xml, n_fonts, n_def = set_font(xml)
            fontinfo = (n_fonts, n_def)
            xml, patched = patch_styles(xml)
            data = xml.encode('utf-8')
        out.append((info, data))

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        for info, data in out:
            z.writestr(info, data)
    open(path, 'wb').write(buf.getvalue())

    if fontinfo:
        print('font: %s %s pt -> %d rFonts declaration(s), %d docDefaults block(s)'
              % (FONT, int(SIZE_HALF_POINTS) // 2, fontinfo[0], fontinfo[1]))
    if patched:
        print('patched pageBreakBefore into: %s' % ', '.join(patched))
    else:
        print('pageBreakBefore: no change (already patched, or styles not found)')
    missing = [s for s in TARGET_STYLES if s not in patched]
    if missing and patched:
        print('NOTE: not patched this run: %s' % ', '.join(missing))
    print('backup: %s.bak' % path)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'reference.docx')
