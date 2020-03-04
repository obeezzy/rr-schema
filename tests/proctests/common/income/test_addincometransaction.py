#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult
from datetime import datetime
from decimal import Decimal

class AddIncomeTransaction(StoredProcedureTestCase):
    def test_add_income_transaction(self):
        addedIncomeTransaction = add_income_transaction(db=self.db,
                                                            name="Lois Lane",
                                                            purpose="Need saving from Superman",
                                                            amount=460.00,
                                                            paymentMethod="cash")
        fetchedIncomeTransaction = fetch_income_transaction(self.db)

        self.assertEqual(addedIncomeTransaction, fetchedIncomeTransaction, "Income transaction mismatch.")

def add_income_transaction(db, name, purpose, amount, paymentMethod):
    incomeTransaction = {
        "client_id": None,
        "client_name": name,
        "purpose": purpose,
        "amount": Decimal(format(amount, '.2f')),
        "payment_method": paymentMethod,
        "currency": "NGN",
        "note_id": None,
        "user_id": 1
    }

    sqlResult = db.call_procedure("AddIncomeTransaction",
                                    tuple(incomeTransaction.values()))
    incomeTransaction.update(DatabaseResult(sqlResult).fetch_one())
    return incomeTransaction

def fetch_income_transaction(db):
    incomeTransactionTable = db.schema.get_table("income_transaction")
    rowResult = incomeTransactionTable.select("id AS income_transaction_id",
                                                "client_id AS client_id",
                                                "client_name AS client_name",
                                                "purpose AS purpose",
                                                "amount AS amount",
                                                "payment_method AS payment_method",
                                                "currency AS currency",
                                                "note_id AS note_id",
                                                "user_id AS user_id") \
                                        .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()