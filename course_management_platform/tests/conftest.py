"""
Minimal pytest configuration: ensure `backend` is on path and env loaded.
"""
import sys
import os

from pathlib import Path
from dotenv import load_dotenv

# Ensure backend package is importable (backend/app -> app)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load environment variables from project .env if present
load_dotenv(Path(__file__).parent.parent / '.env')
