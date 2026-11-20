import os
import sys

# Make the project root importable so tests can `from app import app`
# regardless of the directory pytest is invoked from.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
