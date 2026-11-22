# Existing consumer. It expects exact stdout bytes and catalog order.
import subprocess
import sys

def print_batch(catalog):
    return subprocess.check_output([sys.executable, "desk.py", "labels", catalog])
