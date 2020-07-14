#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

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

    db.execute("""INSERT INTO client (id,
                                        first_name,
                                        last_name,
                                        preferred_name,
                                        phone_number,
                                        archived,
                                        user_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)""", tuple(client.values()))
    db.commit()

def archive_client(db, clientId, userId):
    db.call_procedure("ArchiveClient", [clientId, userId])

def view_archived_clients(db):
    db.call_procedure("ViewClients", [True])
    results = [] 
    for row in db:
        result = {
            "client_id": row["client_id"],
            "preferred_name": row["preferred_name"],
            "phone_number": row["phone_number"]
        }
        results.append(result)
    return results

def fetch_clients(db, archived=False):
    db.execute("""SELECT id AS client_id,
                            preferred_name,
                            phone_number
                    FROM client
                    WHERE archived = %s""", [archived])
    results = [] 
    for row in db:
        result = {
            "client_id": row["client_id"],
            "preferred_name": row["preferred_name"],
            "phone_number": row["phone_number"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
