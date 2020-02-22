#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase

class UpdateClient(StoredProcedureTestCase):
    def test_update_client(self):
        try:
            addedClient = add_single_client(self)
            update_client(self)
            fetchedClient = fetch_client(self)

            self.assertLess(addedClient["last_edited"],
                            fetchedClient["last_edited"],
                            "Last edited date/time invalid.")
            # Remove "last_edited" since they don't match
            del addedClient["last_edited"]; del fetchedClient["last_edited"]
            self.assertEqual(addedClient,
                                fetchedClient,
                                "Record mismatch.")
        except:
            raise
        finally:
            self.db.cleanup()

def add_single_client(self):
    client = {
        "client_id": 1,
        "first_name": "First name",
        "last_name": "Last name",
        "preferred_name": "Preferred name",
        "phone_number": "1234567890",
        "created": self.now,
        "last_edited": self.now,
        "user_id": 1
    }

    self.db.execute("INSERT INTO client (\
                            id, \
                            first_name, \
                            last_name, \
                            preferred_name, \
                            phone_number, \
                            created, \
                            last_edited, \
                            user_id) \
                            VALUES (\
                            %s, \
                            %s, \
                            %s, \
                            %s, \
                            %s, \
                            %s, \
                            %s, \
                            %s)", 
                            tuple(client.values()))

    return client

def update_client(self):
    client = {
        "client_id": 1,
        "first_name": "First name",
        "last_name": "Last name",
        "preferred_name": "Preferred name",
        "phone_number": "1234567890",
        "user_id": 1
    }

    return self.db.call_procedure("UpdateClient",
                                    list(client.values())
    )

def fetch_client(self):
    return self.db.execute("SELECT id AS client_id, \
                            first_name, \
                            last_name, \
                            preferred_name, \
                            phone_number, \
                            created, \
                            last_edited, \
                            user_id \
                            FROM client")

if __name__ == '__main__':
    unittest.main()