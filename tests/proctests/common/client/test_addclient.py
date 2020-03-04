#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class AddClient(StoredProcedureTestCase):
    def test_add_client(self):
        addedClient = add_client(self.db)
        fetchedClient = fetch_client(self.db)

        self.assertEqual(addedClient, fetchedClient, "Fetched record mismatch.")

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

    return client

def fetch_client(db):
    clientTable = db.schema.get_table("client")
    rowResult = clientTable.select("first_name",
                                    "last_name",
                                    "preferred_name",
                                    "phone_number",
                                    "address",
                                    "note_id",
                                    "user_id") \
                            .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()