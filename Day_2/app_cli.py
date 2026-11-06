# app/cli.py
from app_records import load_records, search, count_by

def main():
    print("Loaded records:", len(load_records()))
    
    print("\nSearch for 'NSS':")
    results = search('NSS')
    for r in results:
        print(f"- {r['activity_head']}: {r['sub_activity']}")
        
    print("\nCount by Activity Head:")
    print(count_by('activity_head'))

if __name__ == "__main__":
    main()