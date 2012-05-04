#!/usr/bin/env python
from django.core.management import execute_manager
import imp

try:
    import mancunia
except ImportError:
    import sys
    import os.path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import mancunia.settings as settings

if __name__ == "__main__":
    execute_manager(settings)
