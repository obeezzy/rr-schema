#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase, DatabaseResult
from datetime import datetime
from decimal import Decimal

class AddExpenseTransaction(StoredProcedureTestCase):
    def test_add_expense_transaction(self):
        addedExpenseTransaction = add_expense_transaction(db=self.db,
                                                            name="Lois Lane",
                                                            purpose="Need saving from Superman",
                                                            amount=460.00,
                                                            paymentMethod="cash")
        fetchedExpenseTransaction = fetch_expense_transaction(self.db)

        self.assertEqual(addedExpenseTransaction, fetchedExpenseTransaction, "Expense transaction mismatch.")

def add_expense_transaction(db, name, purpose, amount, paymentMethod):
    expenseTransaction = {
        "client_id": None,
        "name": name,
        "purpose": purpose,
        "amount": Decimal(format(amount, '.2f')),
        "payment_method": paymentMethod,
        "currency": "NGN",
        "note_id": None,
        "user_id": 1
    }

    sqlResult = db.call_procedure("AddExpenseTransaction",
                                    tuple(expenseTransaction.values()))
    expenseTransaction.update(DatabaseResult(sqlResult).fetch_one())
    return expenseTransaction

def fetch_expense_transaction(db):
    expenseTransactionTable = db.schema.get_table("expense_transaction")
    rowResult = expenseTransactionTable.select("id AS expense_transaction_id",
                                                "client_id AS client_id",
                                                "name AS name",
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