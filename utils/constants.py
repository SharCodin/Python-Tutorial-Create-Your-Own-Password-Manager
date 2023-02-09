"""
This file contains constant values use in the application.
"""

import string

LEGAL_CHARACTERS = string.digits + string.ascii_letters + "!@#$%^&*_.-?"
NON_EMAIL_ILLEGAL_PATTERN = f"^{LEGAL_CHARACTERS}"
EMAIL_PATTERN = r"^([a-zA-Z0-9]+[\._%+-]?)*[a-zA-Z0-9]+@[a-zA-Z0-9]+[\.]{1}[a-zA-Z]{2,}([\.]{1}[a-zA-Z]{2,})?$"
