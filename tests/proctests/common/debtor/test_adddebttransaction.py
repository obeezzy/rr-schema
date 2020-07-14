#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class AddDebtTransaction(StoredProcedureTestCase):
    def test_add_debt_transaction(self):
        addedDebtTransaction = add_debt_transaction(self.db)
        fetchedDebtTransaction = fetch_debt_transaction(self.db)

        self.assertEqual(addedDebtTransaction["debt_transaction_id"], fetchedDebtTransaction["debt_transaction_id"], "Debt transaction ID mismatch.")
        self.assertEqual(addedDebtTransaction["debtor_id"], fetchedDebtTransaction["debtor_id"], "Debtor ID mismatch.")
        self.assertEqual(addedDebtTransaction["transaction_table"], fetchedDebtTransaction["transaction_table"], "Transaction table mismatch.")
        self.assertEqual(addedDebtTransaction["transaction_id"], fetchedDebtTransaction["transaction_id"], "Transaction ID mismatch.")
        self.assertEqual(addedDebtTransaction["note_id"], fetchedDebtTransaction["note_id"], "Note ID mismatch.")
        self.assertEqual(addedDebtTransaction["user_id"], fetchedDebtTransaction["user_id"], "User ID mismatch.")

def add_debt_transaction(db):
    debtTransaction = {
        "debtor_id": 1,
        "transaction_table": "sale",
        "transaction_id": 20,
        "note_id": 1,
        "user_id": 1
    }

    db.call_procedure("AddDebtTransaction",
                        tuple(debtTransaction.values()))
    result = {}
    for row in db:
        result = {
            "debt_transaction_id": row[0]
        }
    result.update(debtTransaction)
    return result

def fetch_debt_transaction(db):
    db.execute("""SELECT id AS debt_transaction_id,
                        debtor_id,
                        transaction_table,
                        transaction_id,
                        note_id,
                        user_id
                FROM debt_transaction""")
    result = {}
    for row in db:
        result = {
            "debt_transaction_id": row["debt_transaction_id"],
            "debtor_id": row["debtor_id"],
            "transaction_table": row["transaction_table"],
            "transaction_id": row["transaction_id"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
