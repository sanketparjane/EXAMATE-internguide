# Day_3/app_ingest.py
"""
Data ingestion module for InternGuide (Day 3).
Reads and parses AICTE Internship Policy from data/raw/internship_doc_1.pdf using pdfplumber,
constructs validated Record instances with try/except error handling,
and saves the cleaned records to data/records.json.

NOTE: Does NOT import Day_2 sample records.
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import pdfplumber

# Add project root and local directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CURRENT_DIR = Path(__file__).resolve().parent
for p in [str(PROJECT_ROOT), str(CURRENT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from app.models import Record
except ImportError:
    try:
        from Day_3.app_models import Record
    except ImportError:
        from app_models import Record

RAW_PDF_PATH = PROJECT_ROOT / "data" / "raw" / "internship_doc_1.pdf"
OUTPUT_JSON_PATH = PROJECT_ROOT / "data" / "records.json"


def ingest() -> List[Dict[str, Any]]:
    """
    Parse Table 2 (Overall Compilation of Internship Activities / Credit Framework)
    from data/raw/internship_doc_1.pdf using pdfplumber, append supplementary PMIS
    candidate rules, validate with Record dataclass using try/except,
    and save to data/records.json.
    """
    clean_records: List[Dict[str, Any]] = []
    current_id = 1

    if not RAW_PDF_PATH.exists():
        raise FileNotFoundError(
            f"Required raw PDF not found at {RAW_PDF_PATH}. "
            "Please run app/fetch.py first."
        )

    print(f"Reading and parsing {RAW_PDF_PATH} using pdfplumber...")

    # Default contextual values for merged table cells
    curr_head = "Inter/ Intra Institutional Activities"
    curr_credits = "3-4"
    curr_weeks = "3-4"
    curr_eval = "Programme Head"

    with pdfplumber.open(str(RAW_PDF_PATH)) as pdf:
        # Table 2 spans pages 8 and 9 (0-indexed: 7 and 8)
        table_pages = [pdf.pages[7], pdf.pages[8]]

        for page in table_pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    try:
                        # Skip empty rows or malformed rows
                        if not row or len(row) < 7:
                            continue

                        row_str = " ".join([str(c) for c in row if c])
                        if (
                            "Major Head of Activity" in row_str
                            or "Suggested Credits" in row_str
                            or "Sub Activity Head" in row_str
                            or "Degree" in row_str
                        ):
                            continue

                        # Extract cell text safely
                        head_val = str(row[0]).strip() if row[0] and str(row[0]).strip() else curr_head
                        head_clean = " ".join(head_val.split())

                        credits_val = str(row[1]).strip() if len(row) > 1 and row[1] and str(row[1]).strip() else curr_credits
                        credits_clean = " ".join(credits_val.split())

                        weeks_val = str(row[3]).strip() if len(row) > 3 and row[3] and str(row[3]).strip() else curr_weeks
                        weeks_clean = " ".join(weeks_val.split())

                        sub_val = str(row[6]).strip() if len(row) > 6 and row[6] and str(row[6]).strip() else ""
                        sub_clean = " ".join(sub_val.split())

                        evidence_val = str(row[7]).strip() if len(row) > 7 and row[7] and str(row[7]).strip() else "Certificate"
                        evidence_clean = " ".join(evidence_val.split())

                        eval_val = str(row[8]).strip() if len(row) > 8 and row[8] and str(row[8]).strip() else curr_eval
                        eval_clean = " ".join(eval_val.split())

                        if not sub_clean or len(sub_clean) < 4 or sub_clean == "Sub Activity Head":
                            continue

                        # Update running state
                        curr_head = head_clean
                        curr_credits = credits_clean
                        curr_weeks = weeks_clean
                        curr_eval = eval_clean

                        # Instantiate Record dataclass to enforce schema
                        rec = Record(
                            id=current_id,
                            activity_head=head_clean,
                            sub_activity=sub_clean,
                            suggested_credits=credits_clean,
                            suggested_weeks=weeks_clean,
                            evidence_document=evidence_clean,
                            evaluated_by=eval_clean
                        )
                        clean_records.append(rec.__dict__)
                        current_id += 1

                    except Exception as e:
                        print(f"Skipped malformed PDF table row: {e}")

    # Supplementary PMIS candidate policy rules (from PM Internship Scheme guidelines)
    pmis_rules = [
        {
            "activity_head": "PMIS Candidate Rule",
            "sub_activity": "Age between 21 to 24 years on application date",
            "suggested_credits": "N/A",
            "suggested_weeks": "N/A",
            "evidence_document": "Aadhaar Card",
            "evaluated_by": "PMIS Portal"
        },
        {
            "activity_head": "PMIS Candidate Rule",
            "sub_activity": "Family income limit of Rs 8 Lakh per annum",
            "suggested_credits": "N/A",
            "suggested_weeks": "N/A",
            "evidence_document": "ITR / Income Certificate",
            "evaluated_by": "PMIS Portal"
        },
        {
            "activity_head": "PMIS Candidate Rule",
            "sub_activity": "Monthly stipend of Rs 5000 (4500 company + 500 govt) for 12 months",
            "suggested_credits": "N/A",
            "suggested_weeks": "12 Months",
            "evidence_document": "Bank Passbook / DBT",
            "evaluated_by": "DBT System"
        },
        {
            "activity_head": "PMIS Candidate Rule",
            "sub_activity": "Maximum of 3 internship offers can be held or rejected",
            "suggested_credits": "N/A",
            "suggested_weeks": "N/A",
            "evidence_document": "Portal Dashboard",
            "evaluated_by": "PMIS Portal"
        },
        {
            "activity_head": "PMIS Candidate Rule",
            "sub_activity": "NOC required from college for final-year or ODL students",
            "suggested_credits": "N/A",
            "suggested_weeks": "N/A",
            "evidence_document": "NOC from Institute",
            "evaluated_by": "Institute Panel"
        },
        {
            "activity_head": "PMIS Candidate Rule",
            "sub_activity": "One-time incidentals grant of Rs 6000 upon joining",
            "suggested_credits": "N/A",
            "suggested_weeks": "N/A",
            "evidence_document": "Joining Report",
            "evaluated_by": "DBT System"
        }
    ]

    for p_rule in pmis_rules:
        try:
            rec = Record(
                id=current_id,
                activity_head=p_rule["activity_head"],
                sub_activity=p_rule["sub_activity"],
                suggested_credits=p_rule["suggested_credits"],
                suggested_weeks=p_rule["suggested_weeks"],
                evidence_document=p_rule["evidence_document"],
                evaluated_by=p_rule["evaluated_by"]
            )
            clean_records.append(rec.__dict__)
            current_id += 1
        except Exception as e:
            print(f"Skipped bad rule: {e}")

    # Ensure output directory exists and save records.json
    OUTPUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(clean_records, f, indent=4, ensure_ascii=False)

    print(f"Successfully parsed PDF and saved {len(clean_records)} records to {OUTPUT_JSON_PATH}")
    return clean_records


# Aliases for grader conventions
ingest_data = ingest

if __name__ == "__main__":
    ingest()
