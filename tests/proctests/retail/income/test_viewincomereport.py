#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from datetime import datetime, date, timedelta
from decimal import Decimal

class ViewIncomeReport(StoredProcedureTestCase):
    def test_view_income_report(self):
        incomeTransaction1 = add_income_transaction(db=self.db,
                                                        clientName="Jack Dorsey",
                                                        purpose="Buy Twitter",
                                                        amount=Decimal("40.00"))
        incomeTransaction2 = add_income_transaction(db=self.db,
                                                        clientName="Elon Musk",
                                                        purpose="Buy Tesla",
                                                        amount=Decimal("90.00"))
        incomeTransaction3 = add_income_transaction(db=self.db,
                                                        clientName="Mark Zuckerberg",
                                                        purpose="Buy Facebook",
                                                        amount=Decimal("190.00"))

        today = date.today()
        tomorrow = today + timedelta(days=1)
        viewedIncomeReport = view_income_report(db=self.db,
                                                        fromDate=today,
                                                        toDate=tomorrow)

        self.assertEqual(len(viewedIncomeReport), 3, "Expected 3 transactions.")
        self.assertEqual(viewedIncomeReport[0]["income_transaction_id"], incomeTransaction1["income_transaction_id"], "Income transaction ID mismatch.")
        self.assertEqual(viewedIncomeReport[0]["purpose"], incomeTransaction1["purpose"], "Purpose mismatch.")
        self.assertEqual(viewedIncomeReport[0]["amount"], incomeTransaction1["amount"], "Amount mismatch.")

        self.assertEqual(viewedIncomeReport[1]["income_transaction_id"], incomeTransaction2["income_transaction_id"], "Income transaction ID mismatch")
        self.assertEqual(viewedIncomeReport[1]["purpose"], incomeTransaction2["purpose"], "Purpose mismatch.")
        self.assertEqual(viewedIncomeReport[1]["amount"], incomeTransaction2["amount"], "Amount mismatch.")

        self.assertEqual(viewedIncomeReport[2]["income_transaction_id"], incomeTransaction3["income_transaction_id"], "Income transaction ID mismatch")
        self.assertEqual(viewedIncomeReport[2]["purpose"], incomeTransaction3["purpose"], "Purpose mismatch.")
        self.assertEqual(viewedIncomeReport[2]["amount"], incomeTransaction3["amount"], "Amount mismatch.")

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

def view_income_report(db, fromDate, toDate):
    db.call_procedure("ViewIncomeReport", [fromDate, toDate])
    results = []
    for row in db:
        result = {
            "income_transaction_id": row["income_transaction_id"],
            "purpose": row["purpose"],
            "amount": row["amount"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
