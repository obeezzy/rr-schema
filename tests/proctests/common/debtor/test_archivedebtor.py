#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase, DatabaseResult

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

    debtorTable = db.schema.get_table("debtor")
    debtorTable.insert("id",
                        "client_id",
                        "user_id") \
                .values(tuple(debtor.values())) \
                .execute()

def archive_debtor(db, debtorId, userId=1):
    db.call_procedure("ArchiveDebtor", (debtorId, 1))

def fetch_debtors(db, archived=False):
    debtorTable = db.schema.get_table("debtor")
    rowResult = debtorTable.select("id AS debtor_id",
                                    "client_id AS client_id",
                                    "user_id AS user_id") \
                            .where("archived = :archived") \
                            .bind("archived", archived) \
                            .execute()
    return DatabaseResult(rowResult).fetch_all()

if __name__ == '__main__':
    unittest.main()