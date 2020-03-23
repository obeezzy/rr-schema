#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime, date, timedelta

class FilterExpenseReport(StoredProcedureTestCase):
    def test_filter_expense_report(self):
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

        today = date.today()
        tomorrow = today + timedelta(days=1)
        filteredExpenseReport = filter_expense_report(db=self.db,
                                                        filterColumn="purpose",
                                                        filterText=expenseTransaction1["purpose"][0:6],
                                                        sortColumn="purpose",
                                                        sortOrder="ascending",
                                                        fromDate=today,
                                                        toDate=tomorrow)
        fetchedExpenseTransactions = fetch_expense_transactions(self.db)

        self.assertEqual(len(fetchedExpenseTransactions), 3, "Expected 3 transactions.")
        self.assertEqual(len(filteredExpenseReport), 1, "Expected 1 transaction.")
        self.assertEqual(filteredExpenseReport[0]["expense_transaction_id"], expenseTransaction1["expense_transaction_id"], "Expense transaction ID mismatch")
        self.assertEqual(filteredExpenseReport[0]["purpose"], expenseTransaction1["purpose"], "Purpose mismatch")
        self.assertEqual(filteredExpenseReport[0]["amount"], expenseTransaction1["amount"], "Amount mismatch")

        filteredExpenseReport = filter_expense_report(db=self.db,
                                                        filterColumn="purpose",
                                                        filterText=expenseTransaction2["purpose"][0:6],
                                                        sortColumn="purpose",
                                                        sortOrder="ascending",
                                                        fromDate=today,
                                                        toDate=tomorrow)
        self.assertEqual(len(fetchedExpenseTransactions), 3, "Expected 3 transactions.")
        self.assertEqual(len(filteredExpenseReport), 1, "Expected 1 transaction.")
        self.assertEqual(filteredExpenseReport[0]["expense_transaction_id"], expenseTransaction2["expense_transaction_id"], "Expense transaction ID mismatch")
        self.assertEqual(filteredExpenseReport[0]["purpose"], expenseTransaction2["purpose"], "Purpose mismatch")
        self.assertEqual(filteredExpenseReport[0]["amount"], expenseTransaction2["amount"], "Amount mismatch")

        filteredExpenseReport = filter_expense_report(db=self.db,
                                                        filterColumn="purpose",
                                                        filterText=expenseTransaction3["purpose"][0:6],
                                                        sortColumn="purpose",
                                                        sortOrder="ascending",
                                                        fromDate=today,
                                                        toDate=tomorrow)
        self.assertEqual(len(fetchedExpenseTransactions), 3, "Expected 3 transactions.")
        self.assertEqual(len(filteredExpenseReport), 1, "Expected 1 transaction.")
        self.assertEqual(filteredExpenseReport[0]["expense_transaction_id"], expenseTransaction3["expense_transaction_id"], "Expense transaction ID mismatch")
        self.assertEqual(filteredExpenseReport[0]["purpose"], expenseTransaction3["purpose"], "Purpose mismatch")
        self.assertEqual(filteredExpenseReport[0]["amount"], expenseTransaction3["amount"], "Amount mismatch")

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

def filter_expense_report(db, filterColumn, filterText, sortColumn, sortOrder, fromDate, toDate):
    sqlResult = db.call_procedure("FilterExpenseReport", (
                                    filterColumn,
                                    filterText,
                                    sortColumn,
                                    sortOrder,
                                    fromDate,
                                    toDate))
    return DatabaseResult(sqlResult).fetch_all()

def fetch_expense_transactions(db):
    expenseTransactionTable = db.schema.get_table("expense_transaction")
    rowResult = expenseTransactionTable.select("id AS expense_transaction_id",
                                                "client_name AS client_name",
                                                "purpose AS purpose",
                                                "amount AS amount",
                                                "payment_method AS payment_method",
                                                "currency AS currency",
                                                "user_id AS user_id") \
                                        .where("archived = FALSE") \
                                        .execute()
    return DatabaseResult(rowResult).fetch_all()

if __name__ == '__main__':
    unittest.main()