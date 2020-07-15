#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class FetchDebtTransaction(StoredProcedureTestCase):
    def test_fetch_debt_transaction(self):
        addedDebtTransaction = add_debt_transaction(self.db)
        fetchedDebtTransaction = fetch_debt_transaction(self.db)

        self.assertEqual(addedDebtTransaction["debt_transaction_id"], fetchedDebtTransaction["debt_transaction_id"], "Debt transaction ID mismatch.")
        self.assertEqual(addedDebtTransaction["debtor_id"], fetchedDebtTransaction["debtor_id"], "Debtor ID mismatch.")
        self.assertEqual(addedDebtTransaction["transaction_table"], fetchedDebtTransaction["transaction_table"], "Transaction table mismatch.")
        self.assertEqual(addedDebtTransaction["user_id"], fetchedDebtTransaction["user_id"], "User ID mismatch.")

def add_debt_transaction(db):
    debtTransaction = {
        "debtor_id": 1,
        "transaction_table": "debtor",
        "user_id": 1
    }

    db.execute("""INSERT INTO debt_transaction (debtor_id,
                                                transaction_table,
                                                user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS debt_transaction_id,
                    debtor_id,
                    transaction_table,
                    user_id""", tuple(debtTransaction.values()))
    result = {}
    for row in db:
        result = {
            "debt_transaction_id": row["debt_transaction_id"],
            "debtor_id": row["debtor_id"],
            "transaction_table": row["transaction_table"],
            "user_id": row["user_id"]
        }
    return result

def fetch_debt_transaction(db):
    db.execute("""SELECT id AS debt_transaction_id,
                            debtor_id,
                            transaction_table,
                            user_id
                FROM debt_transaction""")
    result = {}
    for row in db:
        result = {
            "debt_transaction_id": row["debt_transaction_id"],
            "debtor_id": row["debtor_id"],
            "transaction_table": row["transaction_table"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
