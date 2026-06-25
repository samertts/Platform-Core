import sys
from pathlib import Path

project_root = str(Path(__file__).parent.parent)
sys.path = [p for p in sys.path if p != project_root and p != ""]
sys.path.append(project_root)
