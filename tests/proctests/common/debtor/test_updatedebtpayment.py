#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase
from datetime import datetime

class UpdateDebtPayment(StoredProcedureTestCase):
    def test_update_debt_payment(self):
        now = datetime.now()
        addedDebtPayment = add_debt_payment(self.db, dueDateTime=now)
        update_debt_payment(self.db, dueDateTime=now)
        updatedDebtPayment = fetch_debt_payment(self.db)

        self.assertEqual(addedDebtPayment["debt_payment_id"], updatedDebtPayment["debt_payment_id"], "Debt payment ID mismatch.")
        self.assertEqual(addedDebtPayment["debt_transaction_id"], updatedDebtPayment["debt_transaction_id"], "Debt transaction ID mismatch.")
        self.assertEqual(addedDebtPayment["total_debt"], updatedDebtPayment["total_debt"], "Total debt mismatch.")
        self.assertEqual(addedDebtPayment["amount_paid"], updatedDebtPayment["amount_paid"], "Amount paid mismatch.")
        self.assertEqual(addedDebtPayment["balance"], updatedDebtPayment["balance"], "Balance mismatch.")
        self.assertEqual(addedDebtPayment["currency"], updatedDebtPayment["currency"], "Currency mismatch.")
        self.assertEqual(addedDebtPayment["due_date_time"], updatedDebtPayment["due_date_time"], "Due date/time mismatch.")
        self.assertEqual(addedDebtPayment["note_id"], updatedDebtPayment["note_id"], "Note ID mismatch.")
        self.assertEqual(addedDebtPayment["user_id"], updatedDebtPayment["user_id"], "User ID mismatch.")

def add_debt_payment(db, dueDateTime):
    debtPayment = {
        "debt_transaction_id": 1,
        "total_debt": locale.currency(100),
        "amount_paid": locale.currency(20),
        "balance": locale.currency(80),
        "currency": "NGN",
        "due_date_time": dueDateTime,
        "note_id": 1,
        "user_id": 1
    }

    db.execute("""INSERT INTO debt_payment (debt_transaction_id,
                                            total_debt,
                                            amount_paid,
                                            balance,
                                            currency,
                                            due_date_time,
                                            note_id,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS debt_payment_id,
                    debt_transaction_id,
                    total_debt,
                    amount_paid,
                    balance,
                    currency,
                    due_date_time,
                    note_id,
                    user_id""", tuple(debtPayment.values()))
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
    result.update(debtPayment)
    return result

def update_debt_payment(db, dueDateTime):
    debtPayment = {
        "debt_payment_id": 1,
        "total_debt": locale.currency(100),
        "amount_paid": locale.currency(20),
        "balance": locale.currency(80),
        "currency": "NGN",
        "due_date_time": dueDateTime,
        "user_id": 1
    }

    db.call_procedure("UpdateDebtPayment",
                        tuple(debtPayment.values()))

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
