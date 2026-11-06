# app/fetch.py
import requests
import os

urls = [
    "https://aicte.gov.in/sites/default/files/Aicte%20Internship%20Policy-%2002.04.2019.pdf",
    "https://www.ugc.gov.in/pdfnews/2051511_Internship-Research-Internship-Guidelines.pdf"
]

def download_files():
    os.makedirs("data/raw", exist_ok=True)
    for i, url in enumerate(urls):
        try:
            print(f"Fetching {url}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            filepath = f"data/raw/doc_{i}.pdf"
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"Saved to {filepath}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")

if __name__ == "__main__":
    download_files()