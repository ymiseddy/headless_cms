import sys
from os import path

from cms.tools import PropertyBag

LOCAL_DIR = path.dirname(__file__)
UP_DIR = path.dirname(LOCAL_DIR)
PARENT_DIR = path.dirname(UP_DIR)

VENDOR_PATH = path.join(PARENT_DIR, "vendor")
sys.path.append(VENDOR_PATH)

sample_user = {
    "first_name": "Bob",
    "last_name": "Smith",
    "email": "test@example.com",
    "password": "Chavez21@",
}

