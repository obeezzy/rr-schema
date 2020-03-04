#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime

class AddDebtPayment(StoredProcedureTestCase):
    def test_add_debt_payment(self):
        addedDebtPayment = add_debt_payment(self.db)
        fetchedDebtPayment = fetch_debt_payment(self.db)

        self.assertEqual(addedDebtPayment, fetchedDebtPayment, "Debt payment mismatch.")

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

    sqlResult = db.call_procedure("AddDebtPayment",
                                        tuple(debtPayment.values()))
    debtPayment.update(DatabaseResult(sqlResult).fetch_one())
    return debtPayment

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