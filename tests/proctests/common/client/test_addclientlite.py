#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class AddClientLite(StoredProcedureTestCase):
    def test_add_client_lite(self):
        addedClient = add_client_lite(self.db)
        fetchedClient = fetch_client(self.db)

        self.assertEqual(addedClient, fetchedClient, "Record mismatch [client].")

def add_client_lite(db):
    client = {
        "preferred_name": "Preferred name",
        "phone_number": "123456789",
        "user_id": 1
    }

    db.call_procedure("AddClientLite",
                            tuple(client.values()))

    return client

def fetch_client(db):
    clientTable = db.schema.get_table("client")
    rowResult = clientTable.select("preferred_name",
                                    "phone_number",
                                    "user_id") \
                            .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()