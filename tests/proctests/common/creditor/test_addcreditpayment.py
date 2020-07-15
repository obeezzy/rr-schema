#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase
from datetime import datetime

class AddCreditPayment(StoredProcedureTestCase):
    def test_add_credit_payment(self):
        addedCreditPayment = add_credit_payment(self.db)
        fetchedCreditPayment = fetch_credit_payment(self.db)

        self.assertEqual(addedCreditPayment["credit_payment_id"],
                            fetchedCreditPayment["credit_payment_id"],
                            "Credit payment ID mismatch.")
        self.assertEqual(addedCreditPayment["credit_transaction_id"],
                            fetchedCreditPayment["credit_transaction_id"],
                            "Credit transaction ID mismatch.")
        self.assertEqual(addedCreditPayment["total_credit"],
                            fetchedCreditPayment["total_credit"],
                            "Total credit mismatch.")
        self.assertEqual(addedCreditPayment["amount_paid"],
                            fetchedCreditPayment["amount_paid"],
                            "Amount paid mismatch.")
        self.assertEqual(addedCreditPayment["balance"],
                            fetchedCreditPayment["balance"],
                            "Balance mismatch.")
        self.assertEqual(addedCreditPayment["currency"],
                            fetchedCreditPayment["currency"],
                            "Currency mismatch.")
        self.assertEqual(addedCreditPayment["due_date_time"],
                            fetchedCreditPayment["due_date_time"],
                            "Due date/time mismatch.")
        self.assertEqual(addedCreditPayment["note_id"],
                            fetchedCreditPayment["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(addedCreditPayment["user_id"],
                            fetchedCreditPayment["user_id"],
                            "User ID mismatch.")

def add_credit_payment(db):
    creditPayment = {
        "credit_transaction_id": 1,
        "total_credit": str(100),
        "amount_paid": str(20),
        "balance": str(80),
        "currency": "NGN",
        "due_date_time": datetime.now(),
        "note_id": 1,
        "user_id": 1
    }

    db.call_procedure("AddCreditPayment", tuple(creditPayment.values()))
    result = {}
    for row in db:
        result = {
            "credit_payment_id": row[0]
        }
    result.update(creditPayment)
    return result

def fetch_credit_payment(db):
    db.execute("""SELECT id AS credit_payment_id,
                            credit_transaction_id,
                            total_credit,
                            amount_paid,
                            balance,
                            currency,
                            due_date_time,
                            note_id,
                            user_id
                FROM credit_payment""")
    result = {}
    for row in db:
        result = {
            "credit_payment_id": row["credit_payment_id"],
            "credit_transaction_id": row["credit_transaction_id"],
            "total_credit": row["total_credit"],
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
