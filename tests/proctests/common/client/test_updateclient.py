#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime

class UpdateClient(StoredProcedureTestCase):
    def test_update_client(self):
        addedClient = add_single_client(self.db)
        update_client(self.db)
        fetchedClient = fetch_client(self.db)

        self.assertEqual(addedClient, fetchedClient, "Client mismatch.")

def add_single_client(db):
    client = {
        "client_id": 1,
        "first_name": "First name",
        "last_name": "Last name",
        "preferred_name": "Preferred name",
        "phone_number": "1234567890",
        "created": DatabaseDateTime(datetime.now()).iso_format,
        "last_edited": DatabaseDateTime(datetime.now()).iso_format,
        "user_id": 1
    }

    clientTable = db.schema.get_table("client")
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
    clientTable = db.schema.get_table("client")
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