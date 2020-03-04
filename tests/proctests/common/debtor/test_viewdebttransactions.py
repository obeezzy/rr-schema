#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class ViewDebtTransactions(StoredProcedureTestCase):
    def test_view_debt_transactions(self):
        add_client(self.db,
                    clientId=1,
                    firstName="Miles",
                    lastName="Morales",
                    preferredName="Spider-Man",
                    phoneNumber="1234")
        add_client(db=self.db,
                    clientId=2,
                    firstName="Ororo",
                    lastName="Monroe",
                    preferredName="Storm",
                    phoneNumber="384958",
                    archived=True)
        add_client(db=self.db,
                    clientId=3,
                    firstName="Jean",
                    lastName="Gray",
                    preferredName="Phoenix",
                    phoneNumber="12849")

        add_debtor(db=self.db,
                    clientId=1)

        viewedClients = view_clients(self.db)
        fetchedClients = fetch_clients(self.db)

        self.assertEqual(viewedClients, fetchedClients, "Client list mismatch.")

def add_client(db, clientId, firstName, lastName, preferredName, phoneNumber, archived=False):
    client = {
        "client_id": clientId,
        "first_name": firstName,
        "last_name": lastName,
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

def add_debtor(db, clientId):
    debtor = {
        "client_id": clientId,
        "user_id": 1
    }


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