import sys
from pathlib import Path

# Get the project root directory
root_dir = Path(__file__).parent.parent

# Add the project root directory to sys.path
sys.path.insert(0, str(root_dir))
