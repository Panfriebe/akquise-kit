"""Macht die gemeinsamen Helfer aus .claude/skripte importierbar."""
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(VAULT / ".claude" / "skripte"))
