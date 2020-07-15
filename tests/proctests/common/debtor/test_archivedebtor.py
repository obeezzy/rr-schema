#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class ArchiveDebtor(StoredProcedureTestCase):
    def test_archive_debtor(self):
        add_debtor(db=self.db, debtorId=1, clientId=1)
        archive_debtor(db=self.db, debtorId=1)
        archivedDebtors = fetch_debtors(self.db)
        debtorArchived = len([debtor for debtor in archivedDebtors if debtor["debtor_id"] == 1]) == 0

        self.assertEqual(debtorArchived, True, "Debtor not archived.")

def add_debtor(db, debtorId, clientId):
    debtor = {
        "debtor_id": debtorId,
        "client_id": clientId,
        "user_id": 1
    }

    db.execute("""INSERT INTO debtor (id,
                                        client_id,
                                        user_id)
                VALUES (%s, %s, %s)
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
