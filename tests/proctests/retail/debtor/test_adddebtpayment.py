#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from datetime import datetime

class AddDebtPayment(StoredProcedureTestCase):
    def test_add_debt_payment(self):
        addedDebtPayment = add_debt_payment(self.db)
        fetchedDebtPayment = fetch_debt_payment(self.db)

        self.assertEqual(addedDebtPayment["debt_payment_id"], fetchedDebtPayment["debt_payment_id"], "Debt payment ID mismatch.")
        self.assertEqual(addedDebtPayment["debt_transaction_id"], fetchedDebtPayment["debt_transaction_id"], "Debt transaction ID mismatch.")
        self.assertEqual(addedDebtPayment["total_debt"], fetchedDebtPayment["total_debt"], "Total debt mismatch.")
        self.assertEqual(addedDebtPayment["amount_paid"], fetchedDebtPayment["amount_paid"], "Amount paid mismatch.")
        self.assertEqual(addedDebtPayment["balance"], fetchedDebtPayment["balance"], "Balance mismatch.")
        self.assertEqual(addedDebtPayment["currency"], fetchedDebtPayment["currency"], "Currency mismatch.")
        self.assertEqual(addedDebtPayment["due_date_time"], fetchedDebtPayment["due_date_time"], "Due/date time mismatch.")
        self.assertEqual(addedDebtPayment["note_id"], fetchedDebtPayment["note_id"], "Note ID mismatch.")
        self.assertEqual(addedDebtPayment["user_id"], fetchedDebtPayment["user_id"], "User ID mismatch.")

def add_debt_payment(db):
    debtPayment = {
        "debt_transaction_id": 1,
        "total_debt": 100,
        "amount_paid": 20,
        "balance": 80,
        "currency": "NGN",
        "due_date_time": datetime.now(),
        "note_id": 1,
        "user_id": 1
    }

    db.call_procedure("AddDebtPayment",
                        tuple(debtPayment.values()))
    result = {}
    for row in db:
        result = {
            "debt_payment_id": row[0]
        }
    result.update(debtPayment)
    return result

def fetch_debt_payment(db):
    db.execute("""SELECT id AS debt_payment_id,
                            debt_transaction_id,
                            total_debt,
                            amount_paid,
                            balance,
                            currency,
                            due_date_time,
                            note_id,
                            user_id
                FROM debt_payment""")
    result = {}
    for row in db:
        result = {
            "debt_payment_id": row["debt_payment_id"],
            "debt_transaction_id": row["debt_transaction_id"],
            "total_debt": row["total_debt"],
            "amount_paid": row["amount_paid"],
            "balance": row["balance"],
            "currency": row["currency"],
            "due_date_time": row["due_date_time"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
