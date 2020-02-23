#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase, DatabaseResult

class ViewClients(StoredProcedureTestCase):
    def test_view_clients(self):
        add_single_client(self, 1, "First client", "1234")
        add_single_client(self, 2, "Second client", "4321", archived=True)
        add_single_client(self, 3, "Third client", "12849")

        viewedClients = view_clients(self)
        fetchedClients = fetch_clients(self)

        self.assertEqual(viewedClients, fetchedClients, "Client list mismatch.")

    def test_view_archived_clients(self):
        add_single_client(self, 1, "First client", "1234")
        add_single_client(self, 2, "Second client", "4321", archived=True)
        add_single_client(self, 3, "Third client", "12849")

        viewedClients = view_clients(self, archived=True)
        fetchedClients = fetch_clients(self, archived=True)

        self.assertEqual(viewedClients, fetchedClients, "Client list mismatch.")

def add_single_client(self, clientId, preferredName, phoneNumber, *args, **kwargs):
    client = {
        "client_id": clientId,
        "first_name": "First name",
        "last_name": "Last name",
        "preferred_name": preferredName,
        "phone_number": phoneNumber,
        "archived": kwargs.get("archived", False),
        "user_id": 1
    }

    clientTable = self.db.schema.get_table("client")
    clientTable.insert("id",
                        "first_name",
                        "last_name",
                        "preferred_name",
                        "phone_number",
                        "archived",
                        "user_id") \
                .values(tuple(client.values())) \
                .execute()

def view_clients(self, *args, **kwargs):
    sqlResult = self.db.call_procedure("ViewClients", (kwargs.get("archived"),))
    return DatabaseResult(sqlResult).fetch_all()

def view_archived_clients(self):
    sqlResult = self.db.call_procedure("ViewClients", (True,))
    return DatabaseResult(sqlResult).fetch_all()

def fetch_clients(self, *args, **kwargs):
    clientTable = self.db.schema.get_table("client")
    rowResult = clientTable.select("id AS client_id",
                                    "preferred_name AS preferred_name",
                                    "phone_number AS phone_number") \
                            .where("archived = IFNULL(:archived, FALSE)") \
                            .bind("archived", kwargs.get("archived")) \
                            .execute()
    return DatabaseResult(rowResult).fetch_all()

if __name__ == '__main__':
    unittest.main()