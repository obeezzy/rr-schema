#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase, DatabaseResult

class ViewClients(StoredProcedureTestCase):
    def test_view_clients(self):
        add_single_client(self.db,
                            clientId=1,
                            preferredName="First client",
                            phoneNumber="1234")
        add_single_client(db=self.db,
                            clientId=2,
                            preferredName="Second client",
                            phoneNumber="4321",
                            archived=True)
        add_single_client(db=self.db,
                            clientId=3,
                            preferredName="Third client",
                            phoneNumber="12849")

        viewedClients = view_clients(self.db)
        fetchedClients = fetch_clients(self.db)

        self.assertEqual(viewedClients, fetchedClients, "Client list mismatch.")

    def test_view_archived_clients(self):
        add_single_client(db=self.db,
                            clientId=1,
                            preferredName="First client",
                            phoneNumber="1234")
        add_single_client(db=self.db,
                            clientId=2,
                            preferredName="Second client",
                            phoneNumber="4321",
                            archived=True)
        add_single_client(db=self.db,
                            clientId=3,
                            preferredName="Third client",
                            phoneNumber="12849")

        viewedClients = view_clients(self.db, archived=True)
        fetchedClients = fetch_clients(self.db, archived=True)

        self.assertEqual(viewedClients, fetchedClients, "Client list mismatch.")

def add_single_client(db, clientId, preferredName, phoneNumber, archived=False):
    client = {
        "client_id": clientId,
        "first_name": "First name",
        "last_name": "Last name",
        "preferred_name": preferredName,
        "phone_number": phoneNumber,
        "archived": archived,
        "user_id": 1
    }

    clientTable = db.schema.get_table("client")
    clientTable.insert("id",
                        "first_name",
                        "last_name",
                        "preferred_name",
                        "phone_number",
                        "archived",
                        "user_id") \
                .values(tuple(client.values())) \
                .execute()

def view_clients(db, archived=None):
    sqlResult = db.call_procedure("ViewClients", (archived,))
    return DatabaseResult(sqlResult).fetch_all()

def fetch_clients(db, archived=None):
    clientTable = db.schema.get_table("client")
    rowResult = clientTable.select("id AS client_id",
                                    "preferred_name AS preferred_name",
                                    "phone_number AS phone_number") \
                            .where("archived = IFNULL(:archived, FALSE)") \
                            .bind("archived", archived) \
                            .execute()
    return DatabaseResult(rowResult).fetch_all()

if __name__ == '__main__':
    unittest.main()