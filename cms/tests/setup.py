from os import path
import sys
LOCAL_DIR = path.dirname(__file__)
UP_DIR = path.dirname(LOCAL_DIR)
PARENT_DIR = path.dirname(UP_DIR)

VENDOR_PATH = path.join(PARENT_DIR, "vendor")
sys.path.append(VENDOR_PATH)

