#!/usr/bin/env python3
"""read_script.py <file> — universal script reader. Never chokes on format again.
Handles: .txt/.md, .docx, the 'fake PDF' zip bundle (images + N.txt inside),
and real text-layer PDFs. Prints the extracted script text to stdout.

The recurring failure was a file named .pdf that is actually a ZIP bundle of
page images plus per-page .txt files. Standard PDF tools die on it. This reads
the embedded text directly."""
import sys, zipfile, re, os

def clean(t):
    t = re.sub(r'\d{1,2}/\d{1,2}/\d{2,4}, .*?about:blank', '', t)
    t = re.sub(r'about:blank \d/\d', '', t)
    return re.sub(r'\n{3,}', '\n\n', t.replace('\r', '')).strip()

def read(path):
    ext = os.path.splitext(path)[1].lower()
    # plain text
    if ext in ('.txt', '.md'):
        return open(path, encoding='utf-8', errors='ignore').read()
    # anything zip-based (docx, or the fake-pdf bundle, or a real .pdf that's actually zip)
    if zipfile.is_zipfile(path):
        z = zipfile.ZipFile(path)
        names = z.namelist()
        # docx
        if 'word/document.xml' in names:
            xml = z.read('word/document.xml').decode('utf-8', 'ignore')
            xml = re.sub(r'</w:p>', '\n', xml)
            return re.sub(r'<[^>]+>', '', xml)
        # fake-pdf bundle: per-page N.txt files
        txts = sorted(n for n in names if re.fullmatch(r'\d+\.txt', n))
        if txts:
            return "\n".join(z.read(n).decode('utf-8', 'ignore') for n in txts)
        # fallback: any .txt inside
        anytxt = [n for n in names if n.endswith('.txt')]
        if anytxt:
            return "\n".join(z.read(n).decode('utf-8', 'ignore') for n in anytxt)
    # real PDF with a text layer
    if ext == '.pdf':
        try:
            from pdfminer.high_level import extract_text
            return extract_text(path)
        except Exception as e:
            return f"[could not extract PDF text: {e}. If this is a scanned/image PDF, hand it to the chat assistant to read by eye.]"
    return open(path, encoding='utf-8', errors='ignore').read()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python read_script.py <file>")
    print(clean(read(sys.argv[1])))
