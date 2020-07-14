#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase

class AddSalePayment(StoredProcedureTestCase):
    def test_add_sale_payment(self):
        addedSalePayment = add_sale_payment(self.db)
        fetchedSalePayment = fetch_sale_payment(self.db)

        self.assertEqual(addedSalePayment["sale_payment_id"],
                            fetchedSalePayment["sale_payment_id"],
                            "Sale payment ID mismatch.")
        self.assertEqual(addedSalePayment["sale_transaction_id"],
                            fetchedSalePayment["sale_transaction_id"],
                            "Sale transaction ID mismatch.")
        self.assertEqual(addedSalePayment["amount"],
                            fetchedSalePayment["amount"],
                            "Amount mismatch.")
        self.assertEqual(addedSalePayment["payment_method"],
                            fetchedSalePayment["payment_method"],
                            "Payment method mismatch.")
        self.assertEqual(addedSalePayment["currency"],
                            fetchedSalePayment["currency"],
                            "Currency mismatch.")
        self.assertEqual(addedSalePayment["note_id"],
                            fetchedSalePayment["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(addedSalePayment["user_id"],
                            fetchedSalePayment["user_id"],
                            "User ID mismatch.")

def add_sale_payment(db):
    salePayment = {
        "sale_transaction_id": 1,
        "amount": locale.currency(100.30),
        "payment_method": "cash",
        "currency": "NGN",
        "note_id": 1,
        "user_id": 1
    }

    db.call_procedure("AddSalePayment",
                        tuple(salePayment.values()))
    result = {}
    for row in db:
        result = {
            "sale_payment_id": row[0]
        }
    result.update(salePayment)
    return result

def fetch_sale_payment(db):
    db.execute("""SELECT id AS sale_payment_id,
                            sale_transaction_id,
                            amount,
                            payment_method,
                            currency,
                            note_id,
                            user_id
                FROM sale_payment""")
    result = {}
    for row in db:
        result = {
            "sale_payment_id": row["sale_payment_id"],
            "sale_transaction_id": row["sale_transaction_id"],
            "amount": row["amount"],
            "payment_method": row["payment_method"],
            "currency": row["currency"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
