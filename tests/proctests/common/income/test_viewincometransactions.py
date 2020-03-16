#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime, timedelta

class ViewIncomeTransactions(StoredProcedureTestCase):
    def test_view_income_transactions(self):
        add_income_transaction(self.db,
                                clientName="Miles Morales",
                                purpose="Kick Kingpin's ass.",
                                amount=420,
                                paymentMethod="debit-card")
        add_income_transaction(db=self.db,
                                clientName="Ororo Monroe",
                                purpose="Fix climate change.",
                                amount=620,
                                paymentMethod="credit-card")
        add_income_transaction(db=self.db,
                                clientName="Jean Gray",
                                purpose="Read minds like their encyclopedias.",
                                amount=777,
                                paymentMethod="cash")

        today = datetime.date(datetime.now())
        tomorrow = today + timedelta(days=1)
        viewedIncomeTransactions = view_income_transactions(db=self.db,
                                                                fromDate=today,
                                                                toDate=tomorrow)

        fetchedIncomeTransactions = fetch_income_transactions(self.db)

        self.assertEqual(viewedIncomeTransactions, fetchedIncomeTransactions, "Income transaction mismatch.")

def add_income_transaction(db, clientName, purpose, amount, paymentMethod):
    incomeTransaction = {
        "client_id": None,
        "client_name": clientName,
        "purpose": purpose,
        "amount": amount,
        #"payment_method": paymentMethod,
        "currency": "NGN",
        "note_id": None,
        "user_id": 1
    }

    incomeTransactionTable = db.schema.get_table("income_transaction")
    incomeTransactionTable.insert("client_id",
                                    "client_name",
                                    "purpose",
                                    "amount",
                                    #"payment_method",
                                    "currency",
                                    "note_id",
                                    "user_id") \
                            .values(tuple(incomeTransaction.values())) \
                            .execute()

def view_income_transactions(db, fromDate, toDate, archived=None):
    sqlResult = db.call_procedure("ViewIncomeTransactions", (
                                    fromDate,
                                    toDate,
                                    archived))
    return DatabaseResult(sqlResult).fetch_all()

def fetch_income_transactions(db, archived=False):
    incomeTransactionTable = db.schema.get_table("income_transaction")
    rowResult = incomeTransactionTable.select("id AS income_transaction_id",
                                                "client_id AS client_id",
                                                "client_name AS client_name",
                                                "amount AS amount") \
                            .where("archived = :archived") \
                            .bind("archived", archived) \
                            .execute()
    return DatabaseResult(rowResult).fetch_all()

if __name__ == '__main__':
    unittest.main()