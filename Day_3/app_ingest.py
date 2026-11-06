# app/ingest.py
import json
import os
from app_models import Record
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Day_2.sample_records import records as raw_data
def ingest_data():
    clean_records = []
    
    for row in raw_data:
        try:
            # Try mapping to the dataclass to ensure fields exist
            clean_rec = Record(
                activity_head=row["activity_head"],
                sub_activity=row["sub_activity"],
                suggested_credits=str(row["suggested_credits"]),
                suggested_weeks=str(row["suggested_weeks"]),
                evidence_document=row["evidence_document"],
                evaluated_by=row["evaluated_by"]
            )
            clean_records.append(clean_rec.__dict__)
        except KeyError as e:
            print(f"Bad row skipped. Missing field: {e}")
            
    os.makedirs("data", exist_ok=True)
    with open("data/records.json", "w") as f:
        json.dump(clean_records, f, indent=4)
    print(f"Successfully ingested {len(clean_records)} records into records.json")

if __name__ == "__main__":
    ingest_data()