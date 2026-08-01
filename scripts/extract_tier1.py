#!/usr/bin/env python3
"""Extract Tier 1 books to plain text. PDFs via pdftotext, EPUBs via ebooklib."""

import subprocess
import os
import sys
from pathlib import Path

FULLTEXT = Path("/home/littleseneca/Projects/Personal/OSKG-IBD/sources/books/_fulltext")
OUTDIR = Path("/home/littleseneca/Projects/Personal/OSKG-IBD/sources/books")

# Map: (source filename pattern) -> (output name, format)
BOOKS = [
    # 1. Sleisenger (review companion only - 11E main text failed CDN)
    ("Sleisenger_and_Fordtrans_Gastrointestinal_and_Liver_Disease_Review_and_Assessmen.pdf",
     "Sleisenger-Fordtran-Review-Companion-2020.txt", "pdf"),

    # 2. Yamada
    ("Yamadas_Textbook_of_Gastroenterology_3_Volume_Set_7th_Edition_BOOKMARKED__INDEXE.pdf",
     "Yamada-Textbook-Gastroenterology-7E-2022.txt", "pdf"),

    # 3. The Microbiome Connection
    ("The_Microbiome_Connection_Your_Guide_to_IBS_SIBO_and_Low-Fermentation_Eating.epub",
     "Microbiome-Connection-Pimentel-2022.txt", "epub"),

    # 4. A New IBS Solution
    ("A_New_IBS_Solution_Bacteria-The_Missing_Link_in_Treating_Irritable_Bowel_Syndrom.pdf",
     "New-IBS-Solution-Pimentel-2006.txt", "pdf"),

    # 5. Crohn's and Colitis
    ("Crohns__colitis__understanding__managing_IBD.epub",
     "Crohns-Colitis-Steinhart-2018.txt", "epub"),
]


def pdf_to_text(pdf_path, out_path):
    """Extract PDF to text using pdftotext -layout."""
    cmd = ["pdftotext", "-layout", str(pdf_path), str(out_path)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        print(f"  ERROR: pdftotext failed: {result.stderr[:200]}")
        return False
    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"  OK: {size_mb:.1f} MB text")
    return True


def epub_to_text(epub_path, out_path):
    """Extract EPUB to text using ebooklib."""
    from ebooklib import epub
    from bs4 import BeautifulSoup

    book = epub.read_epub(str(epub_path))
    chapters = []
    for item in book.get_items():
        if item.get_type() == 9:  # ITEM_DOCUMENT
            soup = BeautifulSoup(item.get_content(), "html.parser")
            text = soup.get_text("\n", strip=True)
            if text.strip():
                chapters.append(text)

    full_text = "\n\n".join(chapters)
    out_path.write_text(full_text, encoding="utf-8")
    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"  OK: {size_mb:.1f} MB text ({len(chapters)} chapters)")
    return True


def main():
    for pattern, out_name, fmt in BOOKS:
        print(f"\n--- {out_name} ---")
        matches = list(FULLTEXT.glob(pattern))
        if not matches:
            # Try partial match
            matches = [f for f in FULLTEXT.iterdir() if pattern[:30] in f.name]
        if not matches:
            print(f"  SKIP: source not found matching '{pattern[:50]}...'")
            continue

        src = matches[0]
        print(f"  Source: {src.name} ({src.stat().st_size / (1024*1024):.1f} MB)")
        out_path = OUTDIR / out_name

        if fmt == "pdf":
            pdf_to_text(src, out_path)
        elif fmt == "epub":
            epub_to_text(src, out_path)

    print("\nDone.")


if __name__ == "__main__":
    main()
