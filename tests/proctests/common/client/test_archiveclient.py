#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class ArchiveClient(StoredProcedureTestCase):
    def test_archive_client(self):
        add_single_client(db=self.db,
                            clientId=1,
                            preferredName="First client",
                            phoneNumber="1234")
        add_single_client(db=self.db,
                            clientId=2,
                            preferredName="Second client",
                            phoneNumber="4321")
        add_single_client(db=self.db,
                            clientId=3,
                            preferredName="Third client",
                            phoneNumber="12849")

        archive_client(db=self.db, clientId=1, userId=1)
        fetchedClients = fetch_clients(self.db)
        clientArchived = len([client for client in fetchedClients if client["client_id"] == 1]) == 0

        self.assertEqual(clientArchived, True, "Client not archived.")

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

def archive_client(db, clientId, userId):
    sqlResult = db.call_procedure("ArchiveClient", (clientId, userId))

def view_archived_clients(db):
    sqlResult = db.call_procedure("ViewClients", (True,))
    return DatabaseResult(sqlResult).fetch_all()

def fetch_clients(db, archived=False):
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