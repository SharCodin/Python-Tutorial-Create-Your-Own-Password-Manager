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

    def tearDown(self) -> None:
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
        for _ in range(5):
            initial_data = ("Google", "Jimmy", "Qwerty123")
            self.db.add_entry(initial_data)
        rows = []
        for row in self.db.get_all_entries():
            rows.append(row)
        self.assertEqual(5, len(rows), "Number of rows do not match.")

    def test_search_entry(self):
        for idx in range(5):
            initial_data = ("Google{}".format(idx), "Jimmy{}".format(idx), "Qwerty{}".format(idx))
            self.db.add_entry(initial_data)
        rows = []
        for row in self.db.search_entry('e2'):
            rows.append(row)
        self.assertEqual(1, len(rows), "Number of rows do not match.")
