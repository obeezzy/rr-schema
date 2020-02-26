#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime

class ArchiveDebtPayment(StoredProcedureTestCase):
    def test_archive_debt_payment(self):
        add_single_debt_payment(db=self.db,
                                    debtPaymentId=1)
        add_single_debt_payment(db=self.db,
                                    debtPaymentId=2)
        add_single_debt_payment(db=self.db,
                                    debtPaymentId=3)

        archive_debt_payment(db=self.db,
                                debtPaymentId=1)

        fetchedDebtPayments = fetch_debt_payments(self.db)
        self.assertEqual(len(fetchedDebtPayments), 2, "Expected 2 debt payments to be returned.")

        debtPaymentArchived = len([debtPayment for debtPayment in fetchedDebtPayments \
                                if debtPayment["debt_transaction_id"] == 1]) == 0
        self.assertEqual(debtPaymentArchived, True, "Debt payment not archived.")

def add_single_debt_payment(db, debtPaymentId):
    debtPayment = {
        "debt_transaction_id": debtPaymentId,
        "total_debt": 100,
        "amount_paid": 80,
        "balance": 20,
        "currency": "NGN",
        "due_date_time": DatabaseDateTime(datetime.now()).iso_format,
        "note_id": 1,
        "user_id": 1
    }

    debtPaymentTable = db.schema.get_table("debt_payment")
    debtPaymentTable.insert("debt_transaction_id",
                            "total_debt",
                            "amount_paid",
                            "balance",
                            "currency",
                            "due_date_time",
                            "note_id ",
                            "user_id") \
                    .values(tuple(debtPayment.values())) \
                    .execute()

def archive_debt_payment(db, debtPaymentId):
    debtPayment = {
        "debt_payment_id": debtPaymentId,
        "user_id": 1
    }

    db.call_procedure("ArchiveDebtPayment",
                        tuple(debtPayment.values()))

def fetch_debt_payments(db, archived=False):
    debtPaymentTable = db.schema.get_table("debt_payment")
    rowResult = debtPaymentTable.select("id AS debt_transaction_id",
                                            "total_debt AS total_debt",
                                            "amount_paid AS amount_paid",
                                            "balance AS balance",
                                            "currency AS currency",
                                            "due_date_time AS due_date_time",
                                            "note_id AS note_id",
                                            "user_id AS user_id") \
                                    .where("archived = :archived") \
                                    .bind("archived", archived) \
                                    .execute()
    return DatabaseResult(rowResult).fetch_all()

if __name__ == '__main__':
    unittest.main()