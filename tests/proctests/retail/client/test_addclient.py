#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class AddClient(StoredProcedureTestCase):
    def test_add_client(self):
        addedClient = add_client(self.db)
        fetchedClient = fetch_client(self.db)

        self.assertEqual(addedClient["client_id"], fetchedClient["client_id"], "Client ID mismatch.")
        self.assertEqual(addedClient["first_name"], fetchedClient["first_name"], "First name mismatch.")
        self.assertEqual(addedClient["last_name"], fetchedClient["last_name"], "Last name mismatch.")
        self.assertEqual(addedClient["preferred_name"], fetchedClient["preferred_name"], "Preferred name mismatch.")
        self.assertEqual(addedClient["phone_number"], fetchedClient["phone_number"], "Phone number mismatch.")
        self.assertEqual(addedClient["address"], fetchedClient["address"], "Address mismatch.")
        self.assertEqual(addedClient["note_id"], fetchedClient["note_id"], "Note ID mismatch.")
        self.assertEqual(addedClient["user_id"], fetchedClient["user_id"], "User ID mismatch.")

    def test_add_two_clients(self):
        add_client(self.db)
        add_client(self.db)

def add_client(db):
    client = {
        "first_name": "First name",
        "last_name": "Last name",
        "preferred_name": "Preferred name",
        "phone_number": "123456789",
        "address": "Address",
        "note_id": None,
        "user_id": 1
    }

    db.call_procedure("AddClient",
                        tuple(client.values()))
    result = {}
    for row in db:
        result = {
            "client_id": row[0]
        }
    result.update(client)
    return result

def fetch_client(db):
    db.execute("""SELECT id AS client_id,
                            first_name,
                            last_name,
                            preferred_name,
                            phone_number,
                            address,
                            note_id,
                            user_id
                FROM client""")
    result = {}
    for row in db:
        result = {
            "client_id": row["client_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "preferred_name": row["preferred_name"],
            "phone_number": row["phone_number"],
            "address": row["address"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
