#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult
from datetime import datetime, date, timedelta

class ViewExpenseTransactions(StoredProcedureTestCase):
    def test_view_expense_transactions(self):
        add_expense_transaction(self.db,
                                clientName="Miles Morales",
                                purpose="Kick Kingpin's ass.",
                                amount=420,
                                paymentMethod="debit-card")
        add_expense_transaction(db=self.db,
                                clientName="Ororo Monroe",
                                purpose="Fix climate change.",
                                amount=620,
                                paymentMethod="credit-card")
        add_expense_transaction(db=self.db,
                                clientName="Jean Gray",
                                purpose="Read minds like their encyclopedias.",
                                amount=777,
                                paymentMethod="cash")

        today = date.today()
        tomorrow = today + timedelta(days=1)
        viewedExpenseTransactions = view_expense_transactions(db=self.db,
                                                                fromDate=today,
                                                                toDate=tomorrow)

        fetchedExpenseTransactions = fetch_expense_transactions(self.db)

        self.assertEqual(viewedExpenseTransactions, fetchedExpenseTransactions, "Expense transaction mismatch.")

def add_expense_transaction(db, clientName, purpose, amount, paymentMethod):
    expenseTransaction = {
        "client_id": None,
        "client_name": clientName,
        "purpose": purpose,
        "amount": amount,
        #"payment_method": paymentMethod,
        "currency": "NGN",
        "note_id": None,
        "user_id": 1
    }

    expenseTransactionTable = db.schema.get_table("expense_transaction")
    expenseTransactionTable.insert("client_id",
                                    "client_name",
                                    "purpose",
                                    "amount",
                                    #"payment_method",
                                    "currency",
                                    "note_id",
                                    "user_id") \
                            .values(tuple(expenseTransaction.values())) \
                            .execute()

def view_expense_transactions(db, fromDate, toDate, archived=None):
    sqlResult = db.call_procedure("ViewExpenseTransactions", (
                                    fromDate,
                                    toDate,
                                    archived))
    return DatabaseResult(sqlResult).fetch_all()

def fetch_expense_transactions(db, archived=False):
    expenseTransactionTable = db.schema.get_table("expense_transaction")
    rowResult = expenseTransactionTable.select("id AS expense_transaction_id",
                                                "client_id AS client_id",
                                                "client_name AS client_name",
                                                "amount AS amount") \
                            .where("archived = :archived") \
                            .bind("archived", archived) \
                            .execute()
    return DatabaseResult(rowResult).fetch_all()

if __name__ == '__main__':
    unittest.main()