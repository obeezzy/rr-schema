#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime
import time

class UpdateDebtPayment(StoredProcedureTestCase):
    def test_update_debt_payment(self):
        addedDebtPayment = add_debt_payment(self.db)
        update_debt_payment(self.db)
        updatedDebtPayment = fetch_debt_payment(self.db)

        self.assertEqual(addedDebtPayment, updatedDebtPayment, "Date/time not updated.")

def add_debt_payment(db):
    debtPayment = {
        "debt_transaction_id": 1,
        "total_debt": 100,
        "amount_paid": 20,
        "balance": 80,
        "currency": "NGN",
        "due_date_time": DatabaseDateTime(datetime.now()).iso_format,
        "note_id": 1,
        "user_id": 1
    }

    debtPaymentTable = db.schema.get_table("debt_payment")
    result = debtPaymentTable.insert("debt_transaction_id",
                                        "total_debt",
                                        "amount_paid",
                                        "balance",
                                        "currency",
                                        "due_date_time",
                                        "note_id",
                                        "user_id") \
                    .values(tuple(debtPayment.values())) \
                    .execute()
    debtPayment.update(DatabaseResult(result).fetch_one(columnLabel="debt_payment_id"))
    return debtPayment

def update_debt_payment(db):
    debtPayment = {
        "debt_payment_id": 1,
        "total_debt": 100,
        "amount_paid": 20,
        "balance": 80,
        "currency": "NGN",
        "due_date_time": DatabaseDateTime(datetime.now()).iso_format,
        "user_id": 1
    }

    db.call_procedure("UpdateDebtPayment",
                        tuple(debtPayment.values()))

def fetch_debt_payment(db):
    debtPaymentTable = db.schema.get_table("debt_payment")
    rowResult = debtPaymentTable.select("id AS debt_payment_id",
                                            "debt_transaction_id AS debt_transaction_id",
                                            "total_debt AS total_debt",
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