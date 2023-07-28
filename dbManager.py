import sqlite3
import os
from dotenv import load_dotenv
from random import randint
import random


class DBManager():
    """
    This is a simple class that handles accessing the local SQLite database. 
    This Database is needed so that we can store each number's conversation ID
    """

    def __init__(self, table_name='ids'):
        # Connect to the database (creates a new database if it doesn't exist)
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.table_name = table_name

        # Create a databse
        query = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER,
            conversation_id INTEGER,
            outdated INTEGER
        )
        """

        self.cursor.execute(query)
        self.conn.commit()
        self.conn.close()

    def create_new_row(self, phone: str) -> int:
        """
        Creates a new row in the sqlite database with the given phone number and then returns the conversation id
        """
        # Reopen the SQLite Connection
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

        phone_number = self._parse_phone_number(phone)

        conversation_id = self._create_new_id()

        query = f"INSERT INTO {self.table_name} (id, conversation_id, outdated) VALUES (?, ?, ?)"
        self.cursor.execute(query, (phone_number, conversation_id, 0))

        self.conn.commit()
        self.conn.close()

        return conversation_id

    def get_conversation_id(self, phone_number: str) -> int:
        """
        Given a phone number, this will return that person's active conversation ID from the SQLite database. 
        If this cannot be found, this will simply return 1001, which is still usable, but might be shared. 

        This function also manages if the phone number does not exist by creating a new row and random
        unique ID.
        """

        # Reopen the SQLite Connection
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

        phone = self._parse_phone_number(phone_number)

        if(self._check_id_exists(phone)):
            print("DBMANAGER: Phone Number exists in databse, retrieving ID!")
            query = f"""
                SELECT (conversation_id)
                FROM {self.table_name}
                WHERE id = ? AND outdated = 0
            """

            self.cursor.execute(query, (phone,))
            conversation_id = self.cursor.fetchone()
            print("DBMANAGER: Successfully got Conversation ID") if conversation_id else print(
                "DBMANAGER: Failed to get Conversation ID, returning 1001!!")

            self.conn.close()
            if conversation_id:
                return conversation_id[0]
            else:
                return 1001
        else:
            # Create a new row for the number and store the conversation ID
            return self.create_new_row(phone_number)

    def remove_conversation_id(self, phone_number: str):
        """
        Given a phone number, it will set all of their conversations to be outdated(1) in the DATABSE.  
        """
        # Reopen the SQLite Connection
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

        phone = self._parse_phone_number(phone_number)
        query = f"""
            UPDATE {self.table_name}
            SET outdated = 1
            WHERE id = ? AND outdated = 0
        """

        self.cursor.execute(query, (phone,))
        self.conn.commit()

        self.conn.close()

    def _parse_phone_number(self, phone_num) -> int:
        """Converts for example, "whatsapp:+911234567890" to 911234567890"""
        return int(phone_num.split(':')[1].replace('+', ''))

    def _check_id_exists(self, id_to_check):
        """
        Checks if a given ID is in the database
        """
        select_query = f'SELECT 1 FROM {self.table_name} WHERE id = ?'
        self.cursor.execute(select_query, (id_to_check,))

        row = self.cursor.fetchone()
        return row is not None

    def _create_new_id(self) -> int:
        """
        Generates a conversation id (integer between 0 and 1000) that does not already exist/has been used
        """

        query = f"SELECT (conversation_id) FROM {self.table_name}"
        self.cursor.execute(query)

        existing_ids = {row[0] for row in self.cursor.fetchall()}
        all_possible_ids = set(range(1001))
        available_ids = [
            id for id in all_possible_ids if id not in existing_ids]

        if not available_ids:
            raise ValueError(
                "All Conversation IDs have been depleted! Please increase the limit!")

        return random.choice(available_ids)
