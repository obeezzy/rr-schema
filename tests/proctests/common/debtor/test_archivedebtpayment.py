#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
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
                                if debtPayment["debt_payment_id"] == 1]) == 0
        self.assertEqual(debtPaymentArchived, True, "Debt payment not archived.")

def add_single_debt_payment(db, debtPaymentId):
    debtPayment = {
        "debt_transaction_id": debtPaymentId,
        "total_debt": 100,
        "amount_paid": 80,
        "balance": 20,
        "currency": "NGN",
        "due_date_time": str(datetime.now()),
        "note_id": 1,
        "user_id": 1
    }

    db.execute("""INSERT INTO debt_payment (debt_transaction_id,
                                            total_debt,
                                            amount_paid,
                                            balance,
                                            currency,
                                            due_date_time,
                                            note_id,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", tuple(debtPayment.values()))
    db.commit()

def archive_debt_payment(db, debtPaymentId):
    debtPayment = {
        "archived": True,
        "debt_payment_id": debtPaymentId,
        "user_id": 1
    }

    db.call_procedure("ArchiveDebtPayment",
                        tuple(debtPayment.values()))

def fetch_debt_payments(db, archived=False):
    db.execute("""SELECT id AS debt_payment_id,
                            debt_transaction_id,
                            total_debt,
                            amount_paid,
                            balance,
                            currency,
                            due_date_time,
                            note_id,
                            user_id
                FROM debt_payment
                WHERE archived = %s""", [archived])
    results = []
    for row in db:
        result = {
            "debt_payment_id": row["debt_payment_id"],
            "debt_transaction_id": row["debt_transaction_id"],
            "total_debt": row["total_debt"],
            "amount_paid": row["amount_paid"],
            "balance": row["balance"],
            "currency": row["currency"],
            "due_date_time": row["due_date_time"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
