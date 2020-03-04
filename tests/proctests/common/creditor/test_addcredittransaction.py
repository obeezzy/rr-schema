#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult
from datetime import datetime

class AddCreditTransaction(StoredProcedureTestCase):
    def test_add_credit_transaction(self):
        addedCreditTransaction = add_credit_transaction(self.db)
        fetchedCreditTransaction = fetch_credit_transaction(self.db)

        self.assertEqual(addedCreditTransaction, fetchedCreditTransaction, "Credit transaction mismatch.")

def add_credit_transaction(db):
    creditTransaction = {
        "creditor_id": 1,
        "transaction_table": "sale",
        "transaction_id": 20,
        "note_id": 1,
        "user_id": 1
    }

    sqlResult = db.call_procedure("AddCreditTransaction",
                                        tuple(creditTransaction.values()))
    creditTransaction.update(DatabaseResult(sqlResult).fetch_one())
    return creditTransaction

def fetch_credit_transaction(db):
    creditTransactionTable = db.schema.get_table("credit_transaction")
    rowResult = creditTransactionTable.select("id AS credit_transaction_id",
                                                "creditor_id AS creditor_id",
                                                "transaction_table AS transaction_table",
                                                "transaction_id AS transaction_id",
                                                "note_id AS note_id",
                                                "user_id AS user_id") \
                                        .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()