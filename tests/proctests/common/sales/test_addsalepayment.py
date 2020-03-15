#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

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
        "amount": 100.30,
        "payment_method": "cash",
        "currency": "NGN",
        "note_id": 1,
        "user_id": 1
    }

    sqlResult = db.call_procedure("AddSalePayment",
                                        tuple(salePayment.values()))
    salePayment.update(DatabaseResult(sqlResult).fetch_one())
    return salePayment

def fetch_sale_payment(db):
    salePaymentTable = db.schema.get_table("sale_payment")
    rowResult = salePaymentTable.select("id AS sale_payment_id",
                                            "sale_transaction_id AS sale_transaction_id",
                                            "amount AS amount",
                                            "payment_method AS payment_method",
                                            "currency AS currency",
                                            "note_id AS note_id",
                                            "user_id AS user_id") \
                                    .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()