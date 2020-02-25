#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase, DatabaseResult
from datetime import datetime
import time

class TouchDebtTransaction(StoredProcedureTestCase):
    def test_touch_debt_transaction(self):
        add_debt_transaction(self.db)
        addedDebtTransaction = fetch_debt_transaction(self.db)
        time.sleep(1)
        touch_debt_transaction(self.db)
        fetchedDebtTransaction = fetch_debt_transaction(self.db)

        originalDateTime = DatabaseClient.from_iso_format(addedDebtTransaction["last_edited"])
        newDateTime = DatabaseClient.from_iso_format(fetchedDebtTransaction["last_edited"])

        self.assertLess(originalDateTime, newDateTime, "Debt transaction mismatch.")

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

def touch_debt_transaction(db):
    debtTransaction = {
        "debt_transaction_id": 1,
        "user_id": 1
    }

    db.call_procedure("TouchDebtTransaction",
                        tuple(debtTransaction.values()))

def fetch_debt_transaction(db):
    debtTransactionTable = db.schema.get_table("debt_transaction")
    rowResult = debtTransactionTable.select("id AS debt_transaction_id",
                                                "debtor_id AS debtor_id",
                                                "transaction_table AS transaction_table",
                                                "transaction_id AS transaction_id",
                                                "note_id AS note_id",
                                                "last_edited AS last_edited",
                                                "user_id AS user_id") \
                                        .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()