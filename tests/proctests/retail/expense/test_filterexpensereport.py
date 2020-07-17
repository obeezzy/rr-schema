#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from datetime import datetime, date, timedelta
from decimal import Decimal

class FilterExpenseReport(StoredProcedureTestCase):
    def test_filter_expense_report(self):
        expenseTransaction1 = add_expense_transaction(db=self.db,
                                                        clientName="Jack Dorsey",
                                                        purpose="Buy Twitter",
                                                        amount=Decimal("40.00"))
        expenseTransaction2 = add_expense_transaction(db=self.db,
                                                        clientName="Elon Musk",
                                                        purpose="Buy Tesla",
                                                        amount=Decimal("90.00"))
        expenseTransaction3 = add_expense_transaction(db=self.db,
                                                        clientName="Mark Zuckerberg",
                                                        purpose="Buy Facebook",
                                                        amount=Decimal("190.00"))

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

    db.execute("""INSERT INTO expense_transaction (client_name,
                                                    purpose,
                                                    amount,
                                                    payment_method,
                                                    currency,
                                                    user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id AS expense_transaction_id,
                    client_name,
                    purpose,
                    amount,
                    payment_method,
                    currency,
                    user_id""", tuple(expenseTransaction.values()))
    result = {}
    for row in db:
        result = {
            "expense_transaction_id": row["expense_transaction_id"],
            "client_name": row["client_name"],
            "purpose": row["purpose"],
            "amount": row["amount"],
            "payment_method": row["payment_method"],
            "currency": row["currency"],
            "user_id": row["user_id"]
        }
    return result

def filter_expense_report(db, filterColumn, filterText, sortColumn, sortOrder, fromDate, toDate):
    db.call_procedure("FilterExpenseReport", [filterColumn,
                                                filterText,
                                                sortColumn,
                                                sortOrder,
                                                fromDate,
                                                toDate])
    results = []
    for row in db:
        result = {
            "expense_transaction_id": row["expense_transaction_id"],
            "purpose": row["purpose"],
            "amount": row["amount"]
        }
        results.append(result)
    return results

def fetch_expense_transactions(db):
    db.execute("""SELECT id AS expense_transaction_id,
                            client_name,
                            purpose,
                            amount,
                            payment_method,
                            currency,
                            user_id
                FROM expense_transaction
                WHERE archived = FALSE""")
    results = []
    for row in db:
        result = {
            "expense_transaction_id": row["expense_transaction_id"],
            "client_name": row["client_name"],
            "purpose": row["purpose"],
            "amount": row["amount"],
            "payment_method": row["payment_method"],
            "currency": row["currency"],
            "user_id": row["user_id"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
