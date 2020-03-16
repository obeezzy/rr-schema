#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

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
        "amount": 100.30,
        "payment_method": "cash",
        "currency": "NGN",
        "note_id": 1,
        "user_id": 1
    }

    sqlResult = db.call_procedure("AddPurchasePayment",
                                        tuple(purchasePayment.values()))
    purchasePayment.update(DatabaseResult(sqlResult).fetch_one())
    return purchasePayment

def fetch_purchase_payment(db):
    purchasePaymentTable = db.schema.get_table("purchase_payment")
    rowResult = purchasePaymentTable.select("id AS purchase_payment_id",
                                            "purchase_transaction_id AS purchase_transaction_id",
                                            "amount AS amount",
                                            "payment_method AS payment_method",
                                            "currency AS currency",
                                            "note_id AS note_id",
                                            "user_id AS user_id") \
                                    .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()