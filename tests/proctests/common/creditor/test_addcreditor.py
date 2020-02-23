#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase, DatabaseResult

class AddCreditor(StoredProcedureTestCase):
    def test_add_creditor(self):
        addedCreditor = add_creditor(self)
        fetchedCreditor = fetch_creditor(self)

        self.assertEqual(addedCreditor, fetchedCreditor, "Creditor ID mismatch.")

def add_creditor(self):
    creditor = {
        "client_id": 1,
        "note_id": 1,
        "user_id": 1
    }

    sqlResult = self.db.call_procedure("AddCreditor",
                                        tuple(creditor.values()))
    creditor.update(DatabaseResult(sqlResult).fetch_one())
    return creditor

def fetch_creditor(self):
    creditorTable = self.db.schema.get_table("creditor")
    rowResult = creditorTable.select("id AS creditor_id",
                        "client_id",
                        "note_id",
                        "user_id") \
                .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()