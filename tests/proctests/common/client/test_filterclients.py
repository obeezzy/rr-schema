#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime

class FilterClients(StoredProcedureTestCase):
    def test_filter_clients(self):
        add_single_client(db=self.db,
                            clientId=1,
                            preferredName="First client",
                            phoneNumber="123456789")
        add_single_client(db=self.db,
                            clientId=2,
                            preferredName="Second client",
                            phoneNumber="987654321")
        filteredClients = filter_clients(db=self.db,
                                        filterColumn="preferred_name",
                                        filterText="Fir",
                                        archived=False)
        fetchedClients = fetch_clients(self.db)

        self.assertEqual(len(fetchedClients), 2, "Expected 2 clients returned.")
        self.assertEqual(len(filteredClients), 1, "Expected 1 filtered client.")
        self.assertEqual(filteredClients[0], fetchedClients[0], "Client mismatch")

def add_single_client(db, clientId, preferredName, phoneNumber):
    client = {
        "client_id": clientId,
        "first_name": "First name",
        "last_name": "Last name",
        "preferred_name": preferredName,
        "phone_number": phoneNumber,
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
                .values(tuple(client.values())) \
                .execute()
    return client

def filter_clients(db, filterColumn, filterText, archived):
    sqlResult = db.call_procedure("FilterClients", (
                                        filterColumn,
                                        filterText,
                                        archived))

    return DatabaseResult(sqlResult).fetch_all()

def fetch_clients(db):
    clientTable = db.schema.get_table("client")
    rowResult = clientTable.select("id AS client_id",
                                    "preferred_name AS preferred_name",
                                    "phone_number AS phone_number") \
                            .execute()
    return DatabaseResult(rowResult).fetch_all()

if __name__ == '__main__':
    unittest.main()