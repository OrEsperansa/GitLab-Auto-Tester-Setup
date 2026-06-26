import sys
from pathlib import Path


PRIVATE_TESTER_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PRIVATE_TESTER_ROOT))
