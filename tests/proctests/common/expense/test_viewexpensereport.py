#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult
from datetime import datetime, timedelta

class ViewExpenseReport(StoredProcedureTestCase):
    def test_view_expense_report(self):
        expenseTransaction1 = add_expense_transaction(db=self.db,
                                                        clientName="Jack Dorsey",
                                                        purpose="Buy Twitter",
                                                        amount=40)
        expenseTransaction2 = add_expense_transaction(db=self.db,
                                                        clientName="Elon Musk",
                                                        purpose="Buy Tesla",
                                                        amount=90)
        expenseTransaction3 = add_expense_transaction(db=self.db,
                                                        clientName="Mark Zuckerberg",
                                                        purpose="Buy Facebook",
                                                        amount=190)

        today = datetime.date(datetime.now())
        tomorrow = today + timedelta(days=1)
        viewedExpenseReport = view_expense_report(db=self.db,
                                                    fromDate=today,
                                                    toDate=tomorrow)

        self.assertEqual(len(viewedExpenseReport), 3, "Expected 3 transactions.")
        self.assertEqual(viewedExpenseReport[0]["expense_transaction_id"], expenseTransaction1["expense_transaction_id"], "Expense transaction ID mismatch")
        self.assertEqual(viewedExpenseReport[0]["purpose"], expenseTransaction1["purpose"], "Purpose mismatch")
        self.assertEqual(viewedExpenseReport[0]["amount"], expenseTransaction1["amount"], "Amount mismatch")

        self.assertEqual(viewedExpenseReport[1]["expense_transaction_id"], expenseTransaction2["expense_transaction_id"], "Expense transaction ID mismatch")
        self.assertEqual(viewedExpenseReport[1]["purpose"], expenseTransaction2["purpose"], "Purpose mismatch")
        self.assertEqual(viewedExpenseReport[1]["amount"], expenseTransaction2["amount"], "Amount mismatch")

        self.assertEqual(viewedExpenseReport[2]["expense_transaction_id"], expenseTransaction3["expense_transaction_id"], "Expense transaction ID mismatch")
        self.assertEqual(viewedExpenseReport[2]["purpose"], expenseTransaction3["purpose"], "Purpose mismatch")
        self.assertEqual(viewedExpenseReport[2]["amount"], expenseTransaction3["amount"], "Amount mismatch")

def add_expense_transaction(db, clientName, purpose, amount):
    expenseTransaction = {
        "client_name": clientName,
        "purpose": purpose,
        "amount": amount,
        "payment_method": "cash",
        "currency": "NGN",
        "user_id": 1
    }

    expenseTransactionTable = db.schema.get_table("expense_transaction")
    result = expenseTransactionTable.insert("client_name",
                                            "purpose",
                                            "amount",
                                            "payment_method",
                                            "currency",
                                            "user_id") \
                                    .values(tuple(expenseTransaction.values())) \
                                    .execute()
    expenseTransaction.update(DatabaseResult(result).fetch_one("expense_transaction_id"))
    return expenseTransaction

def view_expense_report(db, fromDate, toDate):
    sqlResult = db.call_procedure("ViewExpenseReport", (
                                    fromDate,
                                    toDate))

    return DatabaseResult(sqlResult).fetch_all()

if __name__ == '__main__':
    unittest.main()