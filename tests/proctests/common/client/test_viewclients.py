#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class ViewClients(StoredProcedureTestCase):
    def test_view_clients(self):
        client1 = add_client(self.db,
                                preferredName="First client",
                                phoneNumber="1234")
        client2 = add_client(db=self.db,
                                preferredName="Second client",
                                phoneNumber="4321",
                                archived=True)
        client3 = add_client(db=self.db,
                                preferredName="Third client",
                                phoneNumber="12849")

        viewedClients = view_clients(self.db)

        self.assertEqual(viewedClients[0]["client_id"],
                            client1["client_id"],
                            "Client ID mismatch.")
        self.assertEqual(viewedClients[0]["preferred_name"],
                            client1["preferred_name"],
                            "Preferred name mismatch.")
        self.assertEqual(viewedClients[0]["phone_number"],
                            client1["phone_number"],
                            "Phone number mismatch.")

        self.assertEqual(viewedClients[1]["client_id"],
                            client3["client_id"],
                            "Client ID mismatch.")
        self.assertEqual(viewedClients[1]["preferred_name"],
                            client3["preferred_name"],
                            "Preferred name mismatch.")
        self.assertEqual(viewedClients[1]["phone_number"],
                            client3["phone_number"],
                            "Phone number mismatch.")

    def test_view_archived_clients(self):
        client1 = add_client(self.db,
                                preferredName="First client",
                                phoneNumber="1234")
        client2 = add_client(db=self.db,
                                preferredName="Second client",
                                phoneNumber="4321",
                                archived=True)
        client3 = add_client(db=self.db,
                                preferredName="Third client",
                                phoneNumber="12849",
                                archived=True)

        viewedClients = view_clients(self.db, archived=True)

        self.assertEqual(viewedClients[0]["client_id"],
                            client2["client_id"],
                            "Client ID mismatch.")
        self.assertEqual(viewedClients[0]["preferred_name"],
                            client2["preferred_name"],
                            "Preferred name mismatch.")
        self.assertEqual(viewedClients[0]["phone_number"],
                            client2["phone_number"],
                            "Phone number mismatch.")

        self.assertEqual(viewedClients[1]["client_id"],
                            client3["client_id"],
                            "Client ID mismatch.")
        self.assertEqual(viewedClients[1]["preferred_name"],
                            client3["preferred_name"],
                            "Preferred name mismatch.")
        self.assertEqual(viewedClients[1]["phone_number"],
                            client3["phone_number"],
                            "Phone number mismatch.")

def add_client(db, preferredName, phoneNumber, archived=False):
    client = {
        "preferred_name": preferredName,
        "phone_number": phoneNumber,
        "archived": archived,
        "user_id": 1
    }

    db.execute("""INSERT INTO client (preferred_name,
                                        phone_number,
                                        archived,
                                        user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id AS client_id,
                    preferred_name,
                    phone_number,
                    archived,
                    user_id""", tuple(client.values()))
    db.commit()
    result = {}
    for row in db:
        result = {
            "client_id": row["client_id"],
            "preferred_name": row["preferred_name"],
            "phone_number": row["phone_number"],
            "archived": row["archived"],
            "user_id": row["user_id"]
        }
    return result

def view_clients(db, archived=False):
    db.call_procedure("ViewClients", [archived])
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
