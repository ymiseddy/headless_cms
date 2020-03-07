"""
Headless CMS main application startup.
"""
import sys
from os import path
import cms

# Do some path munging
EXEC_DIR = path.abspath(path.dirname(__file__))
VENDOR_LIB = path.join(EXEC_DIR, "vendor")
sys.path.append(VENDOR_LIB)

if __name__ == "__main__":
    pass
    # cms.run(sys.argv)
