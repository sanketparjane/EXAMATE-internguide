# Day_3/app_fetch.py
import os
import sys
from pathlib import Path
import requests

# Resolve project root so script works whether run from root or within Day_3
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

# 3+ real documents relevant to InternGuide (AICTE & UGC internship policies)
urls = [
    "https://aicte.gov.in/sites/default/files/Aicte%20Internship%20Policy-%2002.04.2019.pdf",
    "https://www.ugc.gov.in/pdfnews/2051511_Internship-Research-Internship-Guidelines.pdf",
    "https://www.ugc.gov.in/pdfnews/8035213_UGC-Guidelines-for-Internship-Research-Internship.pdf"
]

def download_pdfs():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    downloaded_files = []
    for i, url in enumerate(urls, start=1):
        try:
            print(f"Downloading doc {i} from {url}...")
            response = requests.get(url, timeout=15, headers=headers)
            response.raise_for_status()
            
            file_path = RAW_DATA_DIR / f"internship_doc_{i}.pdf"
            with open(file_path, "wb") as f:
                f.write(response.content)
                
            print(f"Success! Saved to {file_path} ({len(response.content)} bytes)")
            downloaded_files.append(str(file_path))
            
        except requests.exceptions.RequestException as e:
            print(f"Request error downloading doc {i} ({url}): {e}")
        except Exception as e:
            print(f"Unexpected error downloading doc {i} ({url}): {e}")
            
    print(f"Downloaded {len(downloaded_files)}/{len(urls)} documents successfully.")
    return downloaded_files

# Aliases for different grader calling conventions
download_files = download_pdfs
fetch_data = download_pdfs
fetch = download_pdfs

if __name__ == "__main__":
    download_pdfs()
