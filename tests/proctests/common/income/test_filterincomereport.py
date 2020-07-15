#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from datetime import datetime, date, timedelta

class FilterIncomeReport(StoredProcedureTestCase):
    def test_filter_income_report(self):
        incomeTransaction1 = add_income_transaction(db=self.db,
                                                        clientName="Jack Dorsey",
                                                        purpose="Buy Twitter",
                                                        amount=40)
        incomeTransaction2 = add_income_transaction(db=self.db,
                                                        clientName="Elon Musk",
                                                        purpose="Buy Tesla",
                                                        amount=90)
        incomeTransaction3 = add_income_transaction(db=self.db,
                                                        clientName="Mark Zuckerberg",
                                                        purpose="Buy Facebook",
                                                        amount=190)

        today = date.today()
        tomorrow = today + timedelta(days=1)
        filteredIncomeReport = filter_income_report(db=self.db,
                                                        filterColumn="purpose",
                                                        filterText=incomeTransaction1["purpose"][0:6],
                                                        sortColumn="purpose",
                                                        sortOrder="ascending",
                                                        fromDate=today,
                                                        toDate=tomorrow)
        fetchedIncomeTransactions = fetch_income_transactions(self.db)

        self.assertEqual(len(fetchedIncomeTransactions), 3, "Expected 3 transactions.")
        self.assertEqual(len(filteredIncomeReport), 1, "Expected 1 transaction.")
        self.assertEqual(filteredIncomeReport[0]["income_transaction_id"], incomeTransaction1["income_transaction_id"], "Income transaction ID mismatch")
        self.assertEqual(filteredIncomeReport[0]["purpose"], incomeTransaction1["purpose"], "Purpose mismatch")
        self.assertEqual(filteredIncomeReport[0]["amount"], incomeTransaction1["amount"], "Amount mismatch")

        filteredIncomeReport = filter_income_report(db=self.db,
                                                        filterColumn="purpose",
                                                        filterText=incomeTransaction2["purpose"][0:6],
                                                        sortColumn="purpose",
                                                        sortOrder="ascending",
                                                        fromDate=today,
                                                        toDate=tomorrow)
        self.assertEqual(len(fetchedIncomeTransactions), 3, "Expected 3 transactions.")
        self.assertEqual(len(filteredIncomeReport), 1, "Expected 1 transaction.")
        self.assertEqual(filteredIncomeReport[0]["income_transaction_id"], incomeTransaction2["income_transaction_id"], "Income transaction ID mismatch")
        self.assertEqual(filteredIncomeReport[0]["purpose"], incomeTransaction2["purpose"], "Purpose mismatch")
        self.assertEqual(filteredIncomeReport[0]["amount"], incomeTransaction2["amount"], "Amount mismatch")

        filteredIncomeReport = filter_income_report(db=self.db,
                                                        filterColumn="purpose",
                                                        filterText=incomeTransaction3["purpose"][0:6],
                                                        sortColumn="purpose",
                                                        sortOrder="ascending",
                                                        fromDate=today,
                                                        toDate=tomorrow)
        self.assertEqual(len(fetchedIncomeTransactions), 3, "Expected 3 transactions.")
        self.assertEqual(len(filteredIncomeReport), 1, "Expected 1 transaction.")
        self.assertEqual(filteredIncomeReport[0]["income_transaction_id"], incomeTransaction3["income_transaction_id"], "Income transaction ID mismatch")
        self.assertEqual(filteredIncomeReport[0]["purpose"], incomeTransaction3["purpose"], "Purpose mismatch")
        self.assertEqual(filteredIncomeReport[0]["amount"], incomeTransaction3["amount"], "Amount mismatch")

def add_income_transaction(db, clientName, purpose, amount):
    incomeTransaction = {
        "client_name": clientName,
        "purpose": purpose,
        "amount": amount,
        "payment_method": "cash",
        "currency": "NGN",
        "user_id": 1
    }

    db.execute("""INSERT INTO income_transaction (client_name,
                                                    purpose,
                                                    amount,
                                                    payment_method,
                                                    currency,
                                                    user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id AS income_transaction_id,
                    client_name,
                    purpose,
                    amount,
                    payment_method,
                    currency,
                    user_id""", tuple(incomeTransaction.values()))
    result = {}
    for row in db:
        result = {
            "income_transaction_id": row["income_transaction_id"],
            "client_name": row["client_name"],
            "purpose": row["purpose"],
            "amount": row["amount"],
            "payment_method": row["payment_method"],
            "currency": row["currency"],
            "user_id": row["user_id"]
        }
    return result

def filter_income_report(db, filterColumn, filterText, sortColumn, sortOrder, fromDate, toDate):
    db.call_procedure("FilterIncomeReport", [filterColumn,
                                                filterText,
                                                sortColumn,
                                                sortOrder,
                                                fromDate,
                                                toDate])
    results = []
    for row in db:
        result = {
            "income_transaction_id": row["income_transaction_id"],
            "purpose": row["purpose"],
            "amount": row["amount"],
        }
        results.append(result)
    return results

def fetch_income_transactions(db):
    db.execute("""SELECT id AS income_transaction_id,
                            client_name,
                            purpose,
                            amount,
                            payment_method,
                            currency,
                            user_id
                FROM income_transaction
                WHERE archived = FALSE""")
    results = []
    for row in db:
        result = {
            "income_transaction_id": row["income_transaction_id"],
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
