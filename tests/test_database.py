"""
This module contains the tests for the PasswordManagerDB class of the core module.

The tests are built using the unittest library, and they check the following functionalities of the PasswordManagerDB
class:

    - create_table_if_required()
    - add_entry()
    - update_entry_all()
    - delete_entry()
    - get_entry()
    - get_all_entries()
    - search_entry_single_result()
    - search_entry_multiple_results()

Before each test, a temporary database is created and after each test it is deleted. The tests verify the correctness
of the database operations by checking the database content and comparing it to the expected results.
"""

import os
import sqlite3
from unittest import TestCase

from core import PasswordManagerDB


class TestPasswordManagerDB(TestCase):

    def setUp(self):
        self.test_db_name = "test_database.db"
        self.abs_path_to_db = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'core\\database',
                                           self.test_db_name)
        self.db = PasswordManagerDB(self.test_db_name)
        self.db.create_table_if_required()

    def tearDown(self):
        os.remove(self.abs_path_to_db)

    def test_create_table_if_required(self):
        con = sqlite3.connect(self.abs_path_to_db)
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' and name='services_password'")
        res = cur.fetchall()
        con.close()
        self.assertEqual(1, len(res), "Table was not created.")

    def test_add_entry(self):
        data = ("Google", "Jimmy", "Qwerty123")
        expected_row = (1, "Google", "Jimmy", "Qwerty123")
        self.db.add_entry(data)
        con = sqlite3.connect(self.abs_path_to_db)
        cur = con.cursor()
        rows = cur.execute("SELECT * FROM services_password").fetchall()
        con.close()
        self.assertEqual(1, len(rows), "Number of rows do not match.")
        self.assertEqual(expected_row, rows[0], "Item added does not match.")

    def test_update_entry_all(self):
        initial_data = ("Google", "Jimmy", "Qwerty123")
        self.db.add_entry(initial_data)
        data = {
            "id": "1",
            "service": "facebook",
            "username_email": "the_sea",
            "password": "Beach_123"
        }
        expected_row = (1, "facebook", "the_sea", "Beach_123")
        self.db.update_entry_all(data)
        con = sqlite3.connect(self.abs_path_to_db)
        cur = con.cursor()
        rows = cur.execute("SELECT * FROM services_password").fetchall()
        con.close()
        self.assertEqual(1, len(rows), "Number of rows do not match.")
        self.assertEqual(expected_row, rows[0], "Item added does not match.")

    def test_delete_entry(self):
        initial_data = ("Google", "Jimmy", "Qwerty123")
        self.db.add_entry(initial_data)
        self.db.delete_entry("1")
        con = sqlite3.connect(self.abs_path_to_db)
        cur = con.cursor()
        rows = cur.execute("SELECT * FROM services_password").fetchall()
        con.close()
        self.assertEqual(0, len(rows), "Number of rows do not match.")

    def test_get_entry(self):
        initial_data = ("Google", "Jimmy", "Qwerty123")
        self.db.add_entry(initial_data)
        row = self.db.get_entry("1")
        expected_row = (1, "Google", "Jimmy", "Qwerty123")
        self.assertEqual(expected_row, row, "Row does not match.")

    def test_get_all_entries(self):
        for idx in range(5):
            initial_data = (f"Google{idx}", f"Jimmy{idx}", f"Qwerty{idx}")
            self.db.add_entry(initial_data)
        rows = self.db.get_all_entries("2")
        self.assertEqual(3, len(rows), "Number of rows do not match.")
        self.assertNotEqual(rows[1], rows[2], "Row 1 and Row 2 has the same data.")

    def test_search_entry_single_result(self):
        for idx in range(5):
            initial_data = (f"Google{idx}", f"Jimmy{idx}", f"Qwerty{idx}")
            self.db.add_entry(initial_data)
        rows = self.db.search_entry('jim', "4")
        self.assertEqual(1, len(rows), "Number of rows do not match.")
        self.assertEqual("Jimmy4", rows[0][2], "Number of rows do not match.")

    def test_search_entry_multiple_results(self):
        for idx in range(5):
            initial_data = (f"Google{idx}", f"Jimmy{idx}", f"Qwerty{idx}")
            self.db.add_entry(initial_data)
        rows = self.db.search_entry('jim', "0")
        self.assertEqual(5, len(rows), "Number of rows do not match.")
        self.assertNotEqual(rows[1], rows[2], "Row 1 and Row 2 has the same data.")
