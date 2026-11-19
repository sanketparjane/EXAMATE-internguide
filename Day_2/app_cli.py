# Day_2/app_cli.py
from Day_2.app_records import load_records, search, count_by, get_by_id

def main():
    print("--- Testing Records App ---")

    # 1. Test load
    all_records = load_records()
    print(f"Total records loaded: {len(all_records)}")

    # 2. Test search
    print("\nSearching for 'NSS':")
    nss_results = search('NSS')
    for r in nss_results:
        print(f" - {r['activity_head']} -> {r['sub_activity']}")

    # 3. Test count
    print("\nCount by Activity Head:")
    counts = count_by('activity_head')
    for key, val in counts.items():
        print(f" {key}: {val}")

    # 4. Test get_by_id
    print("\nGetting record with ID 5:")
    rec = get_by_id(5)
    print(rec)

if __name__ == "__main__":
    main()
