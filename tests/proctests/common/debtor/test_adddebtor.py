#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase, DatabaseResult

class AddDebtor(StoredProcedureTestCase):
    def test_add_debtor(self):
        addedDebtor = add_debtor(self)
        fetchedDebtor = fetch_debtor(self)

        self.assertEqual(addedDebtor, fetchedDebtor, "Debtor mismatch.")

def add_debtor(self):
    debtor = {
        "client_id": 1,
        "note_id": 1,
        "user_id": 1
    }

    sqlResult = self.db.call_procedure("AddDebtor",
                                        tuple(debtor.values()))
    debtor.update(DatabaseResult(sqlResult).fetch_one())
    return debtor

def fetch_debtor(self):
    debtorTable = self.db.schema.get_table("debtor")
    rowResult = debtorTable.select("id AS debtor_id",
                                    "client_id",
                                    "note_id",
                                    "user_id") \
                            .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()