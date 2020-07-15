#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class AddDebtor(StoredProcedureTestCase):
    def test_add_debtor(self):
        addedDebtor = add_debtor(self.db)
        fetchedDebtor = fetch_debtor(self.db)

        self.assertEqual(addedDebtor["debtor_id"], fetchedDebtor["debtor_id"], "Debtor ID mismatch.")
        self.assertEqual(addedDebtor["client_id"], fetchedDebtor["client_id"], "Client ID mismatch.")
        self.assertEqual(addedDebtor["note_id"], fetchedDebtor["note_id"], "Note ID mismatch.")
        self.assertEqual(addedDebtor["user_id"], fetchedDebtor["user_id"], "User ID mismatch.")

def add_debtor(db):
    debtor = {
        "client_id": 1,
        "note_id": 1,
        "user_id": 1
    }

    db.call_procedure("AddDebtor",
                        tuple(debtor.values()))
    result = {}
    for row in db:
        result = {
            "debtor_id": row[0]
        }
    result.update(debtor)
    return result

def fetch_debtor(db):
    db.execute("""SELECT id AS debtor_id,
                            client_id,
                            note_id,
                            user_id
                FROM debtor""")
    result = {}
    for row in db:
        result = {
            "debtor_id": row["debtor_id"],
            "client_id": row["client_id"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
