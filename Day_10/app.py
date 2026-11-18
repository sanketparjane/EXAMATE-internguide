# Day_10/app.py
"""
Day 10 Streamlit UI entry point for InternGuide.
Runs the complete Streamlit UI from ui/app.py.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Run ui/app.py
ui_app_path = PROJECT_ROOT / "ui" / "app.py"
with open(ui_app_path, "r", encoding="utf-8") as f:
    code = f.read()

exec(code, globals())
