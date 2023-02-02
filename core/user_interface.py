"""
User Interface

This module provides the implementation of rendering the CLI user interface on screen. It uses `argparse` library to
get command line arguments from the user. If no arguments was passed, a CLI interface will be displayed to the user.

Components:
    UserInterface class: create and display the user interface to the user.
"""

from utils.utilities import clear_screen


class UserInterface:
    """Create and display the user interface with options to the user."""

    def __init__(self):
        """Initialize the options to display to users."""
        self.options = [
            ('1', 'Add a new password entry.'),
            ('2', 'Generate a secure random password.'),
            ('3', 'Retrieve a saved password.'),
            ('4', 'Delete a password entry.'),
        ]
        self.message = self.display_choice()

    @staticmethod
    def welcome_msg():
        """Display the welcome message and brief description on application."""
        msg = [
            'Welcome to Password Manager by Sharvin!\n\n',
            'This is a secure and convenient tool to manage your password locally.\n',
            'It can generate a secure random password, add existing passwords and delete passwords from a local '
            'database.\n',
            "Let's get started.\n\n"
        ]
        print(''.join(msg))

    def display_choice(self):
        """Display the menu of options to the user and return their choice."""
        message = 'Please select an option from the list below:\n\n'
        message += '\n'.join(f'{num}. {text}' for num, text in self.options)
        return message

    def get_user_choice(self):
        """Get the user option choice."""
        while True:
            choice = input(f'{self.message}\n\nEnter your choice (e.g. 1): ')
            if choice in [num for num, _ in self.options]:
                return choice
            clear_screen()
            print(f'Error: "{choice}" is not a valid option. Please try again.\n\n')
