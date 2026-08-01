#!/usr/bin/env python3
"""Convert Phase-5-Capstone.md to EPUB."""
import markdown
from ebooklib import epub
import re
import os

capstone_path = "/home/littleseneca/Projects/Personal/OSKG-IBD/notes/synthesis/Phase-5-Capstone.md"
with open(capstone_path) as f:
    md_content = f.read()

# Strip YAML frontmatter
md_body = re.sub(r'^---\n.*?\n---\n', '', md_content, flags=re.DOTALL)

html_body = markdown.markdown(md_body, extensions=['tables', 'fenced_code'])

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>OSKG-IBD Capstone</title>
<style>
body {{ font-family: Georgia, serif; line-height: 1.7; max-width: 40em; margin: 0 auto; padding: 1em; color: #1a1a1a; }}
h1 {{ font-size: 1.8em; border-bottom: 2px solid #2a6f4c; padding-bottom: 0.3em; }}
h2 {{ font-size: 1.3em; margin-top: 1.5em; color: #2a6f4c; }}
h3 {{ font-size: 1.1em; }}
blockquote {{ border-left: 3px solid #2a6f4c; padding-left: 1em; color: #555; margin-left: 0; }}
table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
th, td {{ border: 1px solid #ccc; padding: 0.5em; text-align: left; }}
th {{ background: #f0f0f0; }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

book = epub.EpubBook()
book.set_identifier('oskg-ibd-capstone-2026')
book.set_title('OSKG-IBD Capstone: What the IBD-SIBO Knowledge Graph Shows')
book.set_language('en')
book.add_author('OSKG-IBD Project')
book.add_metadata('DC', 'description', 'Evidence-grounded synthesis of the IBD-SIBO knowledge graph. 476 claims, 174 edges across 20+ sources.')

c1 = epub.EpubHtml(title='Capstone', file_name='capstone.xhtml', lang='en')
c1.content = full_html
book.add_item(c1)

book.toc = [epub.Link('capstone.xhtml', 'Capstone', 'capstone')]
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
book.spine = ['nav', c1]

output_path = "/home/littleseneca/Projects/Personal/OSKG-IBD/OSKG-IBD-Capstone.epub"
epub.write_epub(output_path, book)
print(f"EPUB written: {output_path}")
print(f"Size: {os.path.getsize(output_path):,} bytes")
