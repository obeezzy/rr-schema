#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime

class AddCreditPayment(StoredProcedureTestCase):
    def test_add_credit_payment(self):
        addedCreditPayment = add_credit_payment(self.db)
        fetchedCreditPayment = fetch_credit_payment(self.db)

        self.assertEqual(addedCreditPayment, fetchedCreditPayment, "Credit payment mismatch.")

def add_credit_payment(db):
    creditPayment = {
        "credit_transaction_id": 1,
        "total_credit": 100,
        "amount_paid": 20,
        "balance": 80,
        "currency": "NGN",
        "due_date_time": DatabaseDateTime(datetime.now()).iso_format,
        "note_id": 1,
        "user_id": 1
    }

    sqlResult = db.call_procedure("AddCreditPayment",
                                    tuple(creditPayment.values()))
    creditPayment.update(DatabaseResult(sqlResult).fetch_one())
    return creditPayment

def fetch_credit_payment(db):
    creditPaymentTable = db.schema.get_table("credit_payment")
    rowResult = creditPaymentTable.select("id AS credit_payment_id",
                                            "credit_transaction_id AS credit_transaction_id",
                                            "total_credit AS total_credit",
                                            "amount_paid AS amount_paid",
                                            "balance AS balance",
                                            "currency AS currency",
                                            "due_date_time AS due_date_time",
                                            "note_id AS note_id",
                                            "user_id AS user_id") \
                                    .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()