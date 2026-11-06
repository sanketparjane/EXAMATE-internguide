# app/records.py
from data.sample_records import records

def load_records():
    return records

def search(keyword):
    return [r for r in records if keyword.lower() in str(r.values()).lower()]

def count_by(category_key):
    counts = {}
    for r in records:
        val = r.get(category_key, "Unknown")
        counts[val] = counts.get(val, 0) + 1
    return counts

def get_by_id(record_id):
    for r in records:
        if r.get("id") == record_id:
            return r
    return None