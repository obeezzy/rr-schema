#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class FetchDebtTransaction(StoredProcedureTestCase):
    def test_fetch_debt_transaction(self):
        addedDebtTransaction = add_debt_transaction(self.db)
        fetchedDebtTransaction = fetch_debt_transaction(self.db)

        self.assertEqual(addedDebtTransaction, fetchedDebtTransaction, "Debt transaction mismatch.")

def add_debt_transaction(db):
    debtTransaction = {
        "debtor_id": 1,
        "transaction_table": "debtor",
        "user_id": 1
    }

    debtTransactionTable = db.schema.get_table("debt_transaction")
    result = debtTransactionTable.insert("debtor_id",
                                            "transaction_table",
                                            "user_id") \
                                    .values(tuple(debtTransaction.values())) \
                                    .execute()
    debtTransaction.update(DatabaseResult(result).fetch_one("debt_transaction_id"))
    return debtTransaction

def fetch_debt_transaction(db):
    debtTransactionTable = db.schema.get_table("debt_transaction")
    rowResult = debtTransactionTable.select("id AS debt_transaction_id",
                                            "debtor_id AS debtor_id",
                                            "transaction_table",
                                            "user_id") \
                                    .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()