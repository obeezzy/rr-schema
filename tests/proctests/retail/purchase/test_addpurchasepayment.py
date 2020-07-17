#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from decimal import Decimal

class AddPurchasePayment(StoredProcedureTestCase):
    def test_add_purchase_payment(self):
        addedPurchasePayment = add_purchase_payment(self.db)
        fetchedPurchasePayment = fetch_purchase_payment(self.db)

        self.assertEqual(addedPurchasePayment["purchase_payment_id"],
                            fetchedPurchasePayment["purchase_payment_id"],
                            "Purchase payment ID mismatch.")
        self.assertEqual(addedPurchasePayment["purchase_transaction_id"],
                            fetchedPurchasePayment["purchase_transaction_id"],
                            "Purchase transaction ID mismatch.")
        self.assertEqual(addedPurchasePayment["amount"],
                            fetchedPurchasePayment["amount"],
                            "Amount mismatch.")
        self.assertEqual(addedPurchasePayment["payment_method"],
                            fetchedPurchasePayment["payment_method"],
                            "Payment method mismatch.")
        self.assertEqual(addedPurchasePayment["currency"],
                            fetchedPurchasePayment["currency"],
                            "Currency mismatch.")
        self.assertEqual(addedPurchasePayment["note_id"],
                            fetchedPurchasePayment["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(addedPurchasePayment["user_id"],
                            fetchedPurchasePayment["user_id"],
                            "User ID mismatch.")

def add_purchase_payment(db):
    purchasePayment = {
        "purchase_transaction_id": 1,
        "amount": Decimal("100.30"),
        "payment_method": "cash",
        "currency": "NGN",
        "note_id": 1,
        "user_id": 1
    }

    db.call_procedure("AddPurchasePayment",
                        tuple(purchasePayment.values()))
    result = {}
    for row in db:
        result = {
            "purchase_payment_id": row[0]
        }
    result.update(purchasePayment)
    return result

def fetch_purchase_payment(db):
    db.execute("""SELECT id AS purchase_payment_id,
                            purchase_transaction_id,
                            amount,
                            payment_method,
                            currency,
                            note_id,
                            user_id
                FROM purchase_payment""")
    result = {}
    for row in db:
        result = {
            "purchase_payment_id": row["purchase_payment_id"],
            "purchase_transaction_id": row["purchase_transaction_id"],
            "amount": row["amount"],
            "payment_method": row["payment_method"],
            "currency": row["currency"],
            "note_id": row["note_id"],
            "user_id": row["note_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
