# Day_7/app_vectorstore.py
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.vectorstore import *

if __name__ == "__main__":
    index_chunks()
