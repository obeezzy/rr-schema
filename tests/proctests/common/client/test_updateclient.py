#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class UpdateClient(StoredProcedureTestCase):
    def test_update_client(self):
        addedClient = add_single_client(self.db)
        update_client(self.db)
        fetchedClient = fetch_client(self.db)

        self.assertEqual(addedClient["client_id"], fetchedClient["client_id"], "Client ID mismatch.")
        self.assertEqual(addedClient["first_name"], fetchedClient["first_name"], "First name mismatch.")
        self.assertEqual(addedClient["last_name"], fetchedClient["last_name"], "Last name mismatch.")
        self.assertEqual(addedClient["preferred_name"], fetchedClient["preferred_name"], "Preferred name mismatch.")
        self.assertEqual(addedClient["phone_number"], fetchedClient["phone_number"], "Phone number mismatch.")
        self.assertEqual(addedClient["user_id"], fetchedClient["user_id"], "User ID mismatch.")

def add_single_client(db):
    client = {
        "client_id": 1,
        "first_name": "First name",
        "last_name": "Last name",
        "preferred_name": "Preferred name",
        "phone_number": "1234567890",
        "user_id": 1
    }

    db.execute("""INSERT INTO client (id,
                                        first_name,
                                        last_name,
                                        preferred_name,
                                        phone_number,
                                        user_id)
                VALUES(%s, %s, %s, %s, %s, %s)
                RETURNING id AS client_id,
                    first_name,
                    last_name,
                    preferred_name,
                    phone_number,
                    user_id""", tuple(client.values()))
    db.commit()
    result = {}
    for row in db:
        result = {
            "client_id": row["client_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "preferred_name": row["preferred_name"],
            "phone_number": row["phone_number"],
            "user_id": row["user_id"]
        }
    return result

def update_client(db):
    client = {
        "client_id": 1,
        "first_name": "First name",
        "last_name": "Last name",
        "preferred_name": "Preferred name",
        "phone_number": "1234567890",
        "user_id": 1
    }

    db.call_procedure("UpdateClient",
                        tuple(client.values()))

def fetch_client(db):
    db.execute("""SELECT id AS client_id,
                            first_name,
                            last_name,
                            preferred_name,
                            phone_number,
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
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
