#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase, DatabaseResult
from datetime import datetime

class UpdateClient(StoredProcedureTestCase):
    def test_update_client(self):
        addedClient = add_single_client(self)
        update_client(self)
        fetchedClient = fetch_client(self)

        self.assertEqual(addedClient["client_id"],
                            fetchedClient["client_id"],
                            "Client ID mismatch.")
        self.assertEqual(addedClient["first_name"],
                            fetchedClient["first_name"],
                            "First name mismatch.")
        self.assertEqual(addedClient["last_name"],
                            fetchedClient["last_name"],
                            "Last name mismatch.")
        self.assertEqual(addedClient["preferred_name"],
                            fetchedClient["preferred_name"],
                            "Preferred name mismatch.")
        self.assertEqual(addedClient["phone_number"],
                            fetchedClient["phone_number"],
                            "Phone number mismatch.")
        self.assertEqual(addedClient["created"],
                            DatabaseClient.to_iso_format(fetchedClient["created"]),
                            "Created date/time mismatch.")
        self.assertEqual(addedClient["last_edited"],    
                            DatabaseClient.to_iso_format(fetchedClient["last_edited"]),
                            "Last edited date/time mismatch.")
        self.assertEqual(addedClient["user_id"],
                            fetchedClient["user_id"],
                            "User ID mismatch.")

def add_single_client(self):
    client = {
        "client_id": 1,
        "first_name": "First name",
        "last_name": "Last name",
        "preferred_name": "Preferred name",
        "phone_number": "1234567890",
        "created": DatabaseClient.to_iso_format(datetime.now()),
        "last_edited": DatabaseClient.to_iso_format(datetime.now()),
        "user_id": 1
    }

    clientTable = self.db.schema.get_table("client")
    clientTable.insert("id",
                        "first_name",
                        "last_name",
                        "preferred_name",
                        "phone_number",
                        "created",
                        "last_edited",
                        "user_id") \
                .values(list(client.values())) \
                .execute()

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

    self.db.call_procedure("UpdateClient",
                            tuple(client.values()))

def fetch_client(self):
    clientTable = self.db.schema.get_table("client")
    rowResult = clientTable.select("id AS client_id",
                                    "first_name AS first_name",
                                    "last_name AS last_name",
                                    "preferred_name AS preferred_name",
                                    "phone_number AS phone_number",
                                    "created AS created",
                                    "last_edited AS last_edited",
                                    "user_id AS user_id") \
                            .execute()

    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()