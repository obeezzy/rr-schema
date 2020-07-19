#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class ArchiveDebtor(StoredProcedureTestCase):
    def test_archive_debtor(self):
        addedClient = add_client(self.db)
        addedDebtor = add_debtor(db=self.db, clientId=addedClient["client_id"])
        archive_debtor(db=self.db, debtorId=addedDebtor["debtor_id"])
        archivedDebtors = fetch_debtors(self.db)
        debtorArchived = len([debtor for debtor in archivedDebtors if debtor["debtor_id"] == 1]) == 0

        self.assertEqual(debtorArchived, True, "Debtor not archived.")

def add_client(db):
    client = {
        "preferred_name": "Preferred name",
        "phone_number": "1234",
        "user_id": 1
    }

    db.execute("""INSERT INTO client (preferred_name,
                                        phone_number,
                                        user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS client_id""", tuple(client.values()))
    result = {}
    for row in db:
        result = {
            "client_id": row["client_id"]
        }
    result.update(client)
    return result

def add_debtor(db, clientId):
    debtor = {
        "client_id": clientId,
        "user_id": 1
    }

    db.execute("""INSERT INTO debtor (client_id,
                                        user_id)
                VALUES (%s, %s)
                RETURNING id AS debtor_id,
                    client_id,
                    user_id""", tuple(debtor.values()))
    db.commit()
    result = {}
    for row in db:
        result = {
            "debtor_id": row["debtor_id"],
            "client_id": row["client_id"],
            "user_id": row["user_id"]
        }
    return result

def archive_debtor(db, debtorId, userId=1):
    db.call_procedure("ArchiveDebtor", (True, debtorId, 1))

def fetch_debtors(db, archived=False):
    db.execute("""SELECT client_id,
                            user_id
                FROM debtor
                WHERE archived = %s""", [archived])
    results = []
    for row in db:
        result = {
            "debtor_id": row["debtor_id"],
            "client_id": row["client_id"],
            "user_id": row["user_id"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
