#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from datetime import datetime
from decimal import Decimal

class AddExpenseTransaction(StoredProcedureTestCase):
    def test_add_expense_transaction(self):
        addedExpenseTransaction = add_expense_transaction(db=self.db,
                                                            name="Lois Lane",
                                                            purpose="Need saving from Superman",
                                                            amount=Decimal("460.00"),
                                                            paymentMethod="cash")
        fetchedExpenseTransaction = fetch_expense_transaction(self.db)

        self.assertEqual(addedExpenseTransaction["client_id"], fetchedExpenseTransaction["client_id"], "Client ID mismatch.")

def add_expense_transaction(db, name, purpose, amount, paymentMethod):
    expenseTransaction = {
        "client_id": None,
        "name": name,
        "purpose": purpose,
        "amount": amount,
        "payment_method": paymentMethod,
        "currency": "NGN",
        "note_id": None,
        "user_id": 1
    }

    db.call_procedure("AddExpenseTransaction",
                        tuple(expenseTransaction.values()))
    result = {}
    for row in db:
        result = {
            "expense_transaction_id": row[0]
        }
    result.update(expenseTransaction)
    return result

def fetch_expense_transaction(db):
    db.execute("""SELECT id AS expense_transaction_id,
                            client_id,
                            client_name,
                            purpose,
                            amount,
                            payment_method,
                            currency,
                            note_id,
                            user_id
                FROM expense_transaction""")
    result = {}
    for row in db:
        result = {
            "expense_transaction_id": row["expense_transaction_id"],
            "client_id": row["client_id"],
            "client_name": row["client_name"],
            "purpose": row["purpose"],
            "amount": row["amount"],
            "payment_method": row["payment_method"],
            "currency": row["currency"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
