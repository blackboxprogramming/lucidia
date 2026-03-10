import sys
import os

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def pytest_configure(config):
    if _root not in sys.path:
        sys.path.insert(0, _root)
