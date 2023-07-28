from dbManager import DBManager
import os
import sys
import sqlite3
import random
from termcolor import colored


def run_test(test_name, test_function):
    try:
        test_function()
        print(colored(f"{test_name}: Passed", "green"))
    except Exception as e:
        print(colored(f"{test_name}: Failed", "red"))
        print(colored(f"Error: {str(e)}", "red"))
        import traceback
        traceback.print_exc(file=sys.stdout)


def test_create_new_row():
    db = DBManager()
    phone_number = "whatsapp:+911234567890"
    conversation_id = db.create_new_row(phone_number)
    assert conversation_id >= 0 and conversation_id <= 1000


def test_get_conversation_id():
    db = DBManager()
    phone_number = "whatsapp:+911234567890"
    conversation_id = db.get_conversation_id(phone_number)
    assert conversation_id >= 0 and conversation_id <= 1000


def test_remove_conversation_id():
    db = DBManager()
    phone_number = "whatsapp:+911234567890"
    db.remove_conversation_id(phone_number)
    conversation_id = db.get_conversation_id(phone_number)
    assert conversation_id == 1001


if __name__ == "__main__":
    os.environ["DB_ENV"] = "testing"
    if os.path.exists("database.db"):
        os.remove("database.db")

    run_test("Test Create New Row", test_create_new_row)
    run_test("Test Get Conversation ID", test_get_conversation_id)
    run_test("Test Remove Conversation ID", test_remove_conversation_id)

    print("All tests completed.")
