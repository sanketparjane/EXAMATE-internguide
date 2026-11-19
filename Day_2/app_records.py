# Day_2/app_records.py
from Day_2.sample_records import records

def load_records():
    # Loop through and add an ID to each record if it doesn't have one
    for index, record in enumerate(records):
        if 'id' not in record:
            record['id'] = index + 1
    return records

def search(keyword):
    data = load_records()
    results = []
    for r in data:
        # Check if the keyword exists anywhere in the record's values
        if keyword.lower() in str(r.values()).lower():
            results.append(r)
    return results

def count_by(category_key):
    data = load_records()
    counts = {}
    for r in data:
        val = r.get(category_key, "Unknown")
        if val in counts:
            counts[val] += 1
        else:
            counts[val] = 1
    return counts

def get_by_id(record_id):
    data = load_records()
    for r in data:
        if r.get('id') == record_id:
            return r
    return None
