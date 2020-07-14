#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class AddClientLite(StoredProcedureTestCase):
    def test_add_client_lite(self):
        addedClient = add_client_lite(self.db)
        fetchedClient = fetch_client(self.db)

        self.assertEqual(addedClient["client_id"], fetchedClient["client_id"], "Client ID mismatch.")
        self.assertEqual(addedClient["preferred_name"], fetchedClient["preferred_name"], "Preferred name mismatch.")
        self.assertEqual(addedClient["phone_number"], fetchedClient["phone_number"], "Phone number mismatch.")
        self.assertEqual(addedClient["user_id"], fetchedClient["user_id"], "User ID mismatch.")

def add_client_lite(db):
    client = {
        "preferred_name": "Preferred name",
        "phone_number": "123456789",
        "user_id": 1
    }

    db.call_procedure("AddClientLite",
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
                            preferred_name,
                            phone_number,
                            user_id
                    FROM client""")
    result = {}
    for row in db:
        result = {
            "client_id": row["client_id"],
            "preferred_name": row["preferred_name"],
            "phone_number": row["phone_number"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
