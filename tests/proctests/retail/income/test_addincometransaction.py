#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from decimal import Decimal

class AddIncomeTransaction(StoredProcedureTestCase):
    def test_add_income_transaction(self):
        addedIncomeTransaction = add_income_transaction(db=self.db,
                                                            name="Lois Lane",
                                                            purpose="Need saving from Superman",
                                                            amount=Decimal("460.00"),
                                                            paymentMethod="cash")
        fetchedIncomeTransaction = fetch_income_transaction(self.db)

        self.assertEqual(addedIncomeTransaction["income_transaction_id"], fetchedIncomeTransaction["income_transaction_id"], "Income transaction mismatch.")

def add_income_transaction(db, name, purpose, amount, paymentMethod):
    incomeTransaction = {
        "client_id": None,
        "client_name": name,
        "purpose": purpose,
        "amount": amount,
        "payment_method": paymentMethod,
        "currency": "NGN",
        "note_id": None,
        "user_id": 1
    }

    db.call_procedure("AddIncomeTransaction",
                        tuple(incomeTransaction.values()))
    result = {}
    for row in db:
        result = {
            "income_transaction_id": row[0]
        }
    result.update(incomeTransaction)
    return result

def fetch_income_transaction(db):
    db.execute("""SELECT id AS income_transaction_id,
                            client_id,
                            client_name,
                            purpose,
                            amount,
                            payment_method,
                            currency,
                            note_id,
                            user_id
                FROM income_transaction""")
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

if __name__ == '__main__':
    unittest.main()
