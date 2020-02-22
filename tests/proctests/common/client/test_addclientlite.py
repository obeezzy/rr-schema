#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase

class AddClientLite(StoredProcedureTestCase):
    def test_add_client_lite(self):
        try:
            addedClient = add_client_lite(self)
            fetchedClient = fetch_client(self)

            self.assertEqual(addedClient, fetchedClient, "Record mismatch.")
        except:
            raise
        finally:
            self.db.cleanup()

def add_client_lite(self):
    client = {
        "preferred_name": "Preferred name",
        "phone_number": "123456789",
        "user_id": 1
    }

    self.db.call_procedure("AddClientLite",
                            list(client.values())
    )

    return client

def fetch_client(self):
    return self.db.execute("SELECT preferred_name, \
                            phone_number, \
                            user_id \
                            FROM client")

if __name__ == '__main__':
    unittest.main()