#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

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
        self.assertEqual(filteredClients[0]["client_id"], fetchedClients[0]["client_id"], "Client ID mismatch.")
        self.assertEqual(filteredClients[0]["preferred_name"], fetchedClients[0]["preferred_name"], "Preferred name mismatch.")
        self.assertEqual(filteredClients[0]["phone_number"], fetchedClients[0]["phone_number"], "Phone number mismatch.")

def add_single_client(db, clientId, preferredName, phoneNumber):
    client = {
        "client_id": clientId,
        "first_name": "First name",
        "last_name": "Last name",
        "preferred_name": preferredName,
        "phone_number": phoneNumber,
        "user_id": 1
    }

    db.execute("""INSERT INTO client (id,
                                        first_name,
                                        last_name,
                                        preferred_name,
                                        phone_number,
                                        user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id AS client_id,
                    first_name,
                    last_name,
                    preferred_name,
                    phone_number,
                    user_id""", tuple(client.values()))
    db.commit()
    result = {}
    for row in db:
        result = {
            "client_id": row["client_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "preferred_name": row["preferred_name"],
            "phone_number": row["phone_number"],
            "user_id": row["user_id"]
        }
    return result

def filter_clients(db, filterColumn, filterText, archived):
    db.call_procedure("FilterClients", [filterColumn,
                                        filterText,
                                        archived])
    results = []
    for row in db:
        result = {
            "client_id": row["client_id"],
            "preferred_name": row["preferred_name"],
            "phone_number": row["phone_number"]
        }
        results.append(result)
    return results

def fetch_clients(db):
    db.execute("""SELECT id AS client_id,
                    preferred_name,
                    phone_number
                    FROM client""")
    results = []
    for row in db:
        result = {
            "client_id": row["client_id"],
            "preferred_name": row["preferred_name"],
            "phone_number": row["phone_number"]
        }
        results.append(result)
    return results
    return db.fetchall()

if __name__ == '__main__':
    unittest.main()
