#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase

class AddClient(StoredProcedureTestCase):
    def test_add_client(self):
        try:
            addedClient = add_client(self)
            fetchedClient = fetch_client(self)

            self.assertEqual(addedClient, fetchedClient, "Fetched record mismatch.")
        except:
            raise
        finally:
            self.db.cleanup()

    def test_add_two_clients(self):
        try:
            add_client(self)
            add_client(self)
        except:
            raise
        finally:
            self.db.cleanup()

def add_client(self):
    client = {
        "first_name": "First name",
        "last_name": "Last name",
        "preferred_name": "Preferred name",
        "phone_number": "123456789",
        "address": "Address",
        "note_id": None,
        "user_id": 1
    }

    self.db.call_procedure("AddClient",
                            list(client.values())
    )

    return client

def fetch_client(self):
    return self.db.execute("SELECT first_name, \
                                last_name, \
                                preferred_name, \
                                phone_number, \
                                address, \
                                note_id, \
                                user_id \
                                FROM client")

if __name__ == '__main__':
    unittest.main()