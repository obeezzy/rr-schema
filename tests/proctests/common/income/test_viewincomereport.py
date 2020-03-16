#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime, timedelta

class ViewIncomeReport(StoredProcedureTestCase):
    def test_view_income_report(self):
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

        today = datetime.date(datetime.now())
        tomorrow = today + timedelta(days=1)
        viewedIncomeReport = view_income_report(db=self.db,
                                                        fromDate=today,
                                                        toDate=tomorrow)

        self.assertEqual(len(viewedIncomeReport), 3, "Expected 3 transactions.")
        self.assertEqual(viewedIncomeReport[0]["income_transaction_id"], incomeTransaction1["income_transaction_id"], "Income transaction ID mismatch")
        self.assertEqual(viewedIncomeReport[0]["purpose"], incomeTransaction1["purpose"], "Purpose mismatch")
        self.assertEqual(viewedIncomeReport[0]["amount"], incomeTransaction1["amount"], "Amount mismatch")

        self.assertEqual(viewedIncomeReport[1]["income_transaction_id"], incomeTransaction2["income_transaction_id"], "Income transaction ID mismatch")
        self.assertEqual(viewedIncomeReport[1]["purpose"], incomeTransaction2["purpose"], "Purpose mismatch")
        self.assertEqual(viewedIncomeReport[1]["amount"], incomeTransaction2["amount"], "Amount mismatch")

        self.assertEqual(viewedIncomeReport[2]["income_transaction_id"], incomeTransaction3["income_transaction_id"], "Income transaction ID mismatch")
        self.assertEqual(viewedIncomeReport[2]["purpose"], incomeTransaction3["purpose"], "Purpose mismatch")
        self.assertEqual(viewedIncomeReport[2]["amount"], incomeTransaction3["amount"], "Amount mismatch")

def add_income_transaction(db, clientName, purpose, amount):
    incomeTransaction = {
        "client_name": clientName,
        "purpose": purpose,
        "amount": amount,
        "payment_method": "cash",
        "currency": "NGN",
        "user_id": 1
    }

    incomeTransactionTable = db.schema.get_table("income_transaction")
    result = incomeTransactionTable.insert("client_name",
                                            "purpose",
                                            "amount",
                                            "payment_method",
                                            "currency",
                                            "user_id") \
                                    .values(tuple(incomeTransaction.values())) \
                                    .execute()
    incomeTransaction.update(DatabaseResult(result).fetch_one("income_transaction_id"))
    return incomeTransaction

def view_income_report(db, fromDate, toDate):
    sqlResult = db.call_procedure("ViewIncomeReport", (
                                    fromDate,
                                    toDate))

    return DatabaseResult(sqlResult).fetch_all()

if __name__ == '__main__':
    unittest.main()