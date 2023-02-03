"""
Utilities

This module provide small utility functions which does not fit in any other classes.

Components:
    clear_screen function: clear the user terminal screen.
"""

import os
import platform


def clear_screen() -> None:
    """
    Clear the user screen.

    It takes into consideration the platform the user is using.

    Returns:
        None
    """
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
