#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class AddDebtTransaction(StoredProcedureTestCase):
    def test_add_debt_transaction(self):
        addedDebtTransaction = add_debt_transaction(self.db)
        fetchedDebtTransaction = fetch_debt_transaction(self.db)

        self.assertEqual(addedDebtTransaction, fetchedDebtTransaction, "Debt transaction mismatch.")

def add_debt_transaction(db):
    debtTransaction = {
        "debtor_id": 1,
        "transaction_table": "sale",
        "transaction_id": 20,
        "note_id": 1,
        "user_id": 1
    }

    sqlResult = db.call_procedure("AddDebtTransaction",
                                        tuple(debtTransaction.values()))
    debtTransaction.update(DatabaseResult(sqlResult).fetch_one())
    return debtTransaction

def fetch_debt_transaction(db):
    debtTransactionTable = db.schema.get_table("debt_transaction")
    rowResult = debtTransactionTable.select("id AS debt_transaction_id",
                                                "debtor_id AS debtor_id",
                                                "transaction_table AS transaction_table",
                                                "transaction_id AS transaction_id",
                                                "note_id AS note_id",
                                                "user_id AS user_id") \
                                        .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()