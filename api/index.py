"""Entrypoint da Vercel."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "backend", "src"))
sys.path.insert(0, ROOT)

from backend.api import app  # noqa: E402,F401
