#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from datetime import datetime, date, timedelta
from decimal import Decimal

class ViewIncomeTransactions(StoredProcedureTestCase):
    def test_view_income_transactions(self):
        add_income_transaction(self.db,
                                clientName="Miles Morales",
                                purpose="Kick Kingpin's ass.",
                                amount=Decimal("420.00"),
                                paymentMethod="debit_card")
        add_income_transaction(db=self.db,
                                clientName="Ororo Monroe",
                                purpose="Fix climate change.",
                                amount=Decimal("620.00"),
                                paymentMethod="credit_card")
        add_income_transaction(db=self.db,
                                clientName="Jean Gray",
                                purpose="Read minds like their encyclopedias.",
                                amount=Decimal("777.00"),
                                paymentMethod="cash")

        today = date.today()
        tomorrow = today + timedelta(days=1)
        viewedIncomeTransactions = view_income_transactions(db=self.db,
                                                                fromDate=today,
                                                                toDate=tomorrow)

        fetchedIncomeTransactions = fetch_income_transactions(self.db)

        self.assertEqual(viewedIncomeTransactions[0]["income_transaction_id"], fetchedIncomeTransactions[0]["income_transaction_id"], "Income transaction ID mismatch.")
        self.assertEqual(viewedIncomeTransactions[0]["client_id"], fetchedIncomeTransactions[0]["client_id"], "Client ID mismatch.")
        self.assertEqual(viewedIncomeTransactions[0]["client_name"], fetchedIncomeTransactions[0]["client_name"], "Client name mismatch.")
        self.assertEqual(viewedIncomeTransactions[0]["purpose"], fetchedIncomeTransactions[0]["purpose"], "Purpose mismatch.")
        self.assertEqual(viewedIncomeTransactions[0]["amount"], fetchedIncomeTransactions[0]["amount"], "Amount mismatch.")
        self.assertEqual(viewedIncomeTransactions[0]["currency"], fetchedIncomeTransactions[0]["currency"], "Currency mismatch.")

def add_income_transaction(db, clientName, purpose, amount, paymentMethod):
    incomeTransaction = {
        "client_id": None,
        "client_name": clientName,
        "purpose": purpose,
        "amount": amount,
        "payment_method": paymentMethod,
        "currency": "NGN",
        "note_id": None,
        "user_id": 1
    }

    db.execute("""INSERT INTO income_transaction (client_id,
                                                    client_name,
                                                    purpose,
                                                    amount,
                                                    payment_method,
                                                    currency,
                                                    note_id,
                                                    user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS income_transaction_id,
                    client_id,
                    client_name,
                    purpose,
                    amount,
                    payment_method,
                    currency,
                    note_id,
                    user_id""", tuple(incomeTransaction.values()))
    result = {}
    for row in db:
        result = {
            "income_transaction_id": row["income_transaction_id"],
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

def view_income_transactions(db, fromDate, toDate, archived=False):
    db.call_procedure("ViewIncomeTransactions", [fromDate, toDate, archived])
    results = []
    for row in db:
        result = {
            "income_transaction_id": row["income_transaction_id"],
            "client_id": row["client_id"],
            "client_name": row["client_name"],
            "purpose": row["purpose"],
            "amount": row["amount"],
            "currency": row["currency"]
        }
        results.append(result)
    return results

def fetch_income_transactions(db, archived=False):
    db.execute("""SELECT id AS income_transaction_id,
                            client_id,
                            client_name,
                            purpose,
                            amount,
                            currency
                FROM income_transaction
                WHERE archived = %s""", [archived])
    results = []
    for row in db:
        result = {
            "income_transaction_id": row["income_transaction_id"],
            "client_id": row["client_id"],
            "client_name": row["client_name"],
            "purpose": row["purpose"],
            "amount": row["amount"],
            "currency": row["currency"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
