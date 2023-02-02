"""
Utilities

This module provide small utility function which does not fit in any other classes.
"""

import os
import platform


def clear_screen() -> None:
    """Clear user screen based on platform.
    :rtype: None
    """
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
