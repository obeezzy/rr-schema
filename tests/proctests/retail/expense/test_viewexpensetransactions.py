#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase
from datetime import datetime, date, timedelta

class ViewExpenseTransactions(StoredProcedureTestCase):
    def test_view_expense_transactions(self):
        add_expense_transaction(self.db,
                                clientName="Miles Morales",
                                purpose="Kick Kingpin's ass.",
                                amount=locale.currency(420),
                                paymentMethod="debit_card")
        add_expense_transaction(db=self.db,
                                clientName="Ororo Monroe",
                                purpose="Fix climate change.",
                                amount=locale.currency(620),
                                paymentMethod="credit_card")
        add_expense_transaction(db=self.db,
                                clientName="Jean Gray",
                                purpose="Read minds like their encyclopedias.",
                                amount=locale.currency(777),
                                paymentMethod="cash")

        today = date.today()
        tomorrow = today + timedelta(days=1)
        viewedExpenseTransactions = view_expense_transactions(db=self.db,
                                                                fromDate=today,
                                                                toDate=tomorrow)

        fetchedExpenseTransactions = fetch_expense_transactions(self.db)

        self.assertEqual(viewedExpenseTransactions[0]["client_id"], fetchedExpenseTransactions[0]["client_id"], "Client ID mismatch.")

def add_expense_transaction(db, clientName, purpose, amount, paymentMethod):
    expenseTransaction = {
        "client_id": None,
        "client_name": clientName,
        "purpose": purpose,
        "amount": amount,
        "payment_method": paymentMethod,
        "currency": "NGN",
        "note_id": None,
        "user_id": 1
    }

    db.execute("""INSERT INTO expense_transaction (client_id,
                                                    client_name,
                                                    purpose,
                                                    amount,
                                                    payment_method,
                                                    currency,
                                                    note_id,
                                                    user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS expense_transaction_id,
                    client_id,
                    client_name,
                    purpose,
                    amount,
                    payment_method,
                    currency,
                    note_id,
                    user_id""", tuple(expenseTransaction.values()))
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

def view_expense_transactions(db, fromDate, toDate, archived=False):
    db.call_procedure("ViewExpenseTransactions", [fromDate,
                                                    toDate,
                                                    archived])
    results = []
    for row in db:
        result = {
                "expense_transaction_id": row["expense_transaction_id"],
                "client_id": row["client_id"],
                "client_name": row["client_name"],
                "amount": row["amount"]
        }
        results.append(result)
    return results

def fetch_expense_transactions(db, archived=False):
    db.execute("""SELECT id AS expense_transaction_id,
                            client_id,
                            client_name,
                            amount
                FROM expense_transaction
                WHERE archived = %s""", [archived])
    results = []
    for row in db:
        result = {
            "expense_transaction_id": row["expense_transaction_id"],
            "client_id": row["client_id"],
            "client_name": row["client_name"],
            "amount": row["amount"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
