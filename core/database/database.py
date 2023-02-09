"""
Password Manager Database implemented in SQLite3

This module provides a class to manage all database related operations for the Password Manager application using
SQLite3 as the underlying database management system.

Components:
    PasswordManagerDB class: manages all database related operations.
        - Create table
        - Add a new entry
        - Update an entry
        - Delete an entry
        - Retrieve a single entry
        - Retrieve all entries
        - Search database
"""
import os
import sqlite3
from typing import Any


class PasswordManagerDB:
    """
    A class to manage all database related operations.
    """

    def __init__(self, db_name: str) -> None:
        """
            Initialize db_file with the correct path

        Args:
            db_name (str): database file name.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_file = os.path.join(base_dir, db_name)

    def create_table_if_required(self) -> None:
        """Create a table if the table does not exist."""
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS services_password (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                username_email TEXT NOT NULL,
                password TEXT NOT NULL
            )""")
        con.commit()
        con.close()

    def add_entry(self, data: tuple[str, str, str]) -> None:
        """
        Add new entry to the database.

        Args:
            data (tuple[str, str, str]): a tuple of service, username_email, password.
                Example
                data = ("Google", "Username", "Password")
        """
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()
        cur.execute("""INSERT INTO services_password(service, username_email, password) VALUES (?,?,?)""", data)
        con.commit()
        con.close()

    def update_entry_all(self, data: dict[str, str]) -> None:
        """
        Update all fields for one entry.

        Args:
            data (dict[str, str]): a dictionary with the key as the name of the field to update and the value os the
                updated string. You must include the ID of the row you want to update.
                Example
                data = {"id": "7", "service": "facebook", "username_email": "user_email", "password": "new_password"}
        """
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()
        cur.execute("""UPDATE services_password SET service=:service, username_email=:username_email, 
                    password=:password WHERE id=:id""", data)
        con.commit()
        con.close()

    def delete_entry(self, id_to_delete: str) -> None:
        """
        Delete an entry using its id. This operation is irreversible.

        Args:
            id_to_delete (str): The pk / id of the row to delete from the database.
        """
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()
        cur.execute("DELETE FROM services_password where id=?", id_to_delete)
        con.commit()
        con.close()

    def get_entry(self, id_to_select: str) -> str:
        """
        Retrieve one entry matching by id from the database.

        Args:
            id_to_select (str): The pk / id to search for in the database.

        Returns:
            tuple: Example - (2, 'ser', '152', '212')
        """
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()
        row = cur.execute("SELECT * FROM services_password where id=?", id_to_select)
        res = row.fetchone()
        con.close()
        return res


    def get_all_entries(self, offset: str) -> Any:
        """
        Retrieve all entries from the database.

        Args:
            offset (str): The last row number which was retrieve. If you want to fetch row 10 to row 20 including row
                          number 10, offset = 9 (start at 10).
        Returns:
            Yields tuple[int, str, str, str]
                Examples - (2, 'ser', '152', '212')
        """
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()

        rows = cur.execute("SELECT * FROM services_password LIMIT 10 OFFSET ?", offset).fetchall()
        con.close()
        return rows

    def search_entry(self, search_term: str, offset: str) -> Any:
        """
            Search the database by service, username_email or password. Can do fuzzy search to some extent.

        Args:
            offset (str): The last row number which was retrieve. If you want to fetch row 10 to row 20 including row
                          number 10, offset = 9 (start at 10).
            search_term (str): The full term or partial term to search for.

        Returns:
            tuple[int, str, str, str]: Example - (2, 'ser', '152', '212')
        """
        con = sqlite3.connect(self.db_file)
        cur = con.cursor()
        query = """SELECT * FROM services_password WHERE service LIKE ? OR username_email LIKE ? OR password LIKE ? 
                LIMIT 10 OFFSET ?"""
        search_query = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", offset)
        cur.execute(query, search_query)
        rows = cur.execute("SELECT * FROM services_password LIMIT 10 OFFSET ?", offset).fetchall()
        con.close()
        return rows
