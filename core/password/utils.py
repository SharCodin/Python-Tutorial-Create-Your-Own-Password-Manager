"""
This module contains helper function to validate user inputs and passwords.

TODO: update the docstring.
"""
import re

from utils.constants import NON_EMAIL_ILLEGAL_PATTERN, EMAIL_PATTERN


def validate_user_input(user_input, is_email=False):
    if not user_input:
        return False

    if re.search(NON_EMAIL_ILLEGAL_PATTERN, user_input):
        return False

    if is_email:
        if not re.search(EMAIL_PATTERN, user_input):
            return False

    return True
