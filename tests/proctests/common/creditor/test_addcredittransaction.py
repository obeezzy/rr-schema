#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class AddCreditTransaction(StoredProcedureTestCase):
    def test_add_credit_transaction(self):
        addedCreditTransaction = add_credit_transaction(self.db)
        fetchedCreditTransaction = fetch_credit_transaction(self.db)

        self.assertEqual(addedCreditTransaction["credit_transaction_id"],
                            fetchedCreditTransaction["credit_transaction_id"],
                            "Credit transaction ID mismatch.")
        self.assertEqual(addedCreditTransaction["transaction_table"],
                            fetchedCreditTransaction["transaction_table"],
                            "Transaction table mismatch.")
        self.assertEqual(addedCreditTransaction["transaction_id"],
                            fetchedCreditTransaction["transaction_id"],
                            "Transaction ID mismatch.")
        self.assertEqual(addedCreditTransaction["note_id"],
                            fetchedCreditTransaction["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(addedCreditTransaction["user_id"],
                            fetchedCreditTransaction["user_id"],
                            "User ID mismatch.")

def add_credit_transaction(db):
    creditTransaction = {
        "creditor_id": 1,
        "transaction_table": "sale",
        "transaction_id": 20,
        "note_id": 1,
        "user_id": 1
    }

    db.call_procedure("AddCreditTransaction",
                        tuple(creditTransaction.values()))
    result = {}
    for row in db:
        result = {
            "credit_transaction_id": row[0]
        }
    result.update(creditTransaction)
    return result

def fetch_credit_transaction(db):
    db.execute("""SELECT id AS credit_transaction_id,
                            creditor_id,
                            transaction_table,
                            transaction_id,
                            note_id,
                            user_id
                FROM credit_transaction""")
    result = {}
    for row in db:
        result = {
            "credit_transaction_id": row["credit_transaction_id"],
            "creditor_id": row["creditor_id"],
            "transaction_table": row["transaction_table"],
            "transaction_id": row["transaction_id"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
