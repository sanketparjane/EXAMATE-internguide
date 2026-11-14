# app/chunking.py
"""
Document chunking module for InternGuide.
Reads raw PDF documents and records.json, chunks them into semantic passages,
and preserves metadata: source, page, and title.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any
import pypdf

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"

# Document title mapping
DOC_TITLES = {
    "internship_doc_1.pdf": "AICTE Internship Policy: Guidelines & Procedures (2019)",
    "internship_doc_2.pdf": "UGC Guidelines for Internship/Research Internship for UG Students",
    "internship_doc_3.pdf": "AICTE Internship Evaluation Proformas, Annexures & Formats",
    "records.json": "InternGuide Curated AICTE & PMIS Rules Database"
}


def clean_text(text: str) -> str:
    """Normalize whitespace and strip spurious control characters."""
    if not text:
        return ""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = 600, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping character chunks while respecting sentence/paragraph boundaries.
    """
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if len(current_chunk) + len(para) <= chunk_size:
            current_chunk = f"{current_chunk}\n\n{para}".strip()
        else:
            if current_chunk:
                chunks.append(current_chunk)
            # If paragraph itself exceeds chunk_size, slice it with overlap
            if len(para) > chunk_size:
                start = 0
                while start < len(para):
                    end = start + chunk_size
                    chunks.append(para[start:end].strip())
                    start += (chunk_size - overlap)
                current_chunk = ""
            else:
                current_chunk = para

    if current_chunk:
        chunks.append(current_chunk)

    return [c for c in chunks if len(c.strip()) > 30]


def chunk_pdf(pdf_path: Path, doc_title: str) -> List[Dict[str, Any]]:
    """
    Extract and chunk text from a PDF, preserving source, page, and title metadata.
    """
    chunks = []
    try:
        reader = pypdf.PdfReader(str(pdf_path))
        filename = pdf_path.name

        for page_idx, page in enumerate(reader.pages, start=1):
            raw_text = page.extract_text() or ""
            text = clean_text(raw_text)
            if not text:
                continue

            page_chunks = chunk_text(text, chunk_size=600, overlap=100)
            for c_idx, chunk_content in enumerate(page_chunks, start=1):
                chunk_id = f"{pdf_path.stem}_p{page_idx}_c{c_idx}"
                chunks.append({
                    "id": chunk_id,
                    "text": chunk_content,
                    "metadata": {
                        "source": filename,
                        "page": page_idx,
                        "title": doc_title,
                        "chunk_index": c_idx
                    }
                })
    except Exception as e:
        print(f"Error chunking {pdf_path}: {e}")

    return chunks


def chunk_records_json(json_path: Path) -> List[Dict[str, Any]]:
    """
    Convert structured records from records.json into semantic chunks with metadata.
    """
    chunks = []
    if not json_path.exists():
        return chunks

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            records = json.load(f)

        for rec in records:
            rec_id = rec.get("id", len(chunks) + 1)
            act_head = rec.get("activity_head", "AICTE Internship Rule")
            sub_act = rec.get("sub_activity", "")
            credits = rec.get("suggested_credits", "N/A")
            weeks = rec.get("suggested_weeks", "N/A")
            evidence = rec.get("evidence_document", "Certificate")
            eval_by = rec.get("evaluated_by", "Faculty / Panel")

            text = (
                f"Activity Head: {act_head}\n"
                f"Sub-Activity: {sub_act}\n"
                f"Suggested Credits: {credits} credits\n"
                f"Suggested Duration: {weeks} weeks (30 hours per credit per AICTE)\n"
                f"Required Evidence: {evidence}\n"
                f"Evaluated By: {eval_by}"
            )

            chunks.append({
                "id": f"record_{rec_id}",
                "text": text,
                "metadata": {
                    "source": "data/records.json",
                    "page": 1,
                    "title": f"InternGuide Rule: {act_head}",
                    "chunk_index": rec_id
                }
            })
    except Exception as e:
        print(f"Error chunking {json_path}: {e}")

    return chunks


def chunk_all_documents() -> List[Dict[str, Any]]:
    """
    Chunk all InternGuide documents in data/raw/ and data/records.json.
    Returns a unified list of chunk dictionaries with metadata: source, page, title.
    """
    all_chunks = []

    # 1. Chunk all PDFs in data/raw/
    if RAW_DIR.exists():
        for pdf_file in sorted(RAW_DIR.glob("*.pdf")):
            title = DOC_TITLES.get(pdf_file.name, f"InternGuide Document: {pdf_file.stem}")
            print(f"Chunking {pdf_file.name}...")
            pdf_chunks = chunk_pdf(pdf_file, title)
            all_chunks.extend(pdf_chunks)
            print(f"  -> Generated {len(pdf_chunks)} chunks from {pdf_file.name}")

    # 2. Chunk data/records.json
    records_file = DATA_DIR / "records.json"
    if records_file.exists():
        rec_chunks = chunk_records_json(records_file)
        all_chunks.extend(rec_chunks)
        print(f"  -> Generated {len(rec_chunks)} chunks from {records_file.name}")

    print(f"Total chunks created across all documents: {len(all_chunks)}")
    return all_chunks


if __name__ == "__main__":
    chunks = chunk_all_documents()
    if chunks:
        sample = chunks[0]
        print("\nSample Chunk:")
        print(f"ID: {sample['id']}")
        print(f"Metadata: {sample['metadata']}")
        print(f"Text Snippet: {sample['text'][:150]}...")
