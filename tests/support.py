"""Resolve app and fixture locations independently of the invoking directory."""
from pathlib import Path
import sys

REPOSITORY = Path(__file__).resolve().parents[1]
APP = REPOSITORY / "app"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(APP))
