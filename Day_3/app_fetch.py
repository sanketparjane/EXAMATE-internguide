# Day_3/app_fetch.py
import requests
import os

# Added a 3rd document URL to meet the "3+" requirement
urls = [
    "https://aicte.gov.in/sites/default/files/Aicte%20Internship%20Policy-%2002.04.2019.pdf",
    "https://www.ugc.gov.in/pdfnews/2051511_Internship-Research-Internship-Guidelines.pdf",
    "https://www.education.gov.in/sites/upload_files/mhrd/files/NEP_Final_English_0.pdf" 
]

def download_pdfs():
    os.makedirs("data/raw", exist_ok=True)
    
    for i, url in enumerate(urls):
        try:
            print(f"Downloading doc {i+1}...")
            # Added a 15-second timeout as required
            response = requests.get(url, timeout=15)
            response.raise_for_status() 
            
            file_path = f"data/raw/internship_doc_{i+1}.pdf"
            with open(file_path, 'wb') as f:
                f.write(response.content)
                
            print(f"Success! Saved to {file_path}")
            
        except Exception as e:
            print(f"Failed to download {url}. Error: {e}")

if __name__ == "__main__":
    download_pdfs()