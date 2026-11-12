# Day_3/app_ingest.py
import json
import os
from Day_3.app_models import Record
from Day_2.sample_records import records as raw_data

def ingest():
    clean_data = []
    current_id = 1
    
    for row in raw_data:
        try:
            # Map fields safely and inject an ID
            record_obj = Record(
                id=current_id,
                activity_head=row["activity_head"],
                sub_activity=row["sub_activity"],
                suggested_credits=str(row.get("suggested_credits", "N/A")),
                suggested_weeks=str(row.get("suggested_weeks", "N/A")),
                evidence_document=row["evidence_document"],
                evaluated_by=row["evaluated_by"]
            )
            clean_data.append(record_obj.__dict__)
            current_id += 1
            
        except Exception as e:
            print(f"Skipped a bad row. Error: {e}")
            
    # Make sure the data folder exists
    os.makedirs("data", exist_ok=True)
    
    # Save the cleaned JSON
    with open("data/records.json", "w") as f:
        json.dump(clean_data, f, indent=4)
        
    print(f"All done! {len(clean_data)} records saved to data/records.json")

if __name__ == "__main__":
    ingest()