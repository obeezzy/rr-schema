#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime

class ViewDebtPayments(StoredProcedureTestCase):
    def test_view_debt_payments(self):
        addedNote1 = add_note(db=self.db, note="First note")
        addedNote2 = add_note(db=self.db, note="Second note")
        addedNote3 = add_note(db=self.db, note="Third note")

        addedDebtTransaction = add_debt_transaction(db=self.db,
                                                    debtorId=1)

        addedDebtPayment1 = add_debt_payment(self.db,
                                                debtTransactionId=addedDebtTransaction["debt_transaction_id"],
                                                totalDebt=750,
                                                amountPaid=250,
                                                noteId=addedNote1["note_id"])
        addedDebtPayment2 = add_debt_payment(self.db,
                                                debtTransactionId=addedDebtTransaction["debt_transaction_id"],
                                                totalDebt=800,
                                                amountPaid=300,
                                                noteId=addedNote2["note_id"])
        addedDebtPayment3 = add_debt_payment(self.db,
                                                debtTransactionId=addedDebtTransaction["debt_transaction_id"],
                                                totalDebt=2100,
                                                amountPaid=200,
                                                noteId=addedNote3["note_id"])

        viewedDebtPayments = view_debt_payments(db=self.db, debtTransactionId=1)

        self.assertEqual(addedDebtPayment1["debt_payment_id"], viewedDebtPayments[0]["debt_payment_id"], "Debt payment ID mismatch")
        self.assertEqual(addedDebtPayment1["debt_transaction_id"], viewedDebtPayments[0]["debt_transaction_id"], "Debt transaction ID mismatch")
        self.assertEqual(addedDebtPayment1["total_debt"], viewedDebtPayments[0]["total_debt"], "Total debt mismatch")
        self.assertEqual(addedDebtPayment1["amount_paid"], viewedDebtPayments[0]["amount_paid"], "Amount paid mismatch")
        self.assertEqual(addedDebtPayment1["balance"], viewedDebtPayments[0]["balance"], "Balance mismatch")
        self.assertEqual(addedDebtPayment1["due_date_time"], viewedDebtPayments[0]["due_date_time"], "Due date/time mismatch")
        self.assertEqual(addedDebtPayment1["note_id"], viewedDebtPayments[0]["note_id"], "Note ID mismatch")
        self.assertEqual(addedNote1["note"], viewedDebtPayments[0]["note"], "Note mismatch")
        self.assertEqual(addedDebtPayment1["currency"], viewedDebtPayments[0]["currency"], "Currency mismatch")

        self.assertEqual(addedDebtPayment2["debt_payment_id"], viewedDebtPayments[1]["debt_payment_id"], "Debt payment ID mismatch")
        self.assertEqual(addedDebtPayment2["debt_transaction_id"], viewedDebtPayments[1]["debt_transaction_id"], "Debt transaction ID mismatch")
        self.assertEqual(addedDebtPayment2["total_debt"], viewedDebtPayments[1]["total_debt"], "Total debt mismatch")
        self.assertEqual(addedDebtPayment2["amount_paid"], viewedDebtPayments[1]["amount_paid"], "Amount paid mismatch")
        self.assertEqual(addedDebtPayment2["balance"], viewedDebtPayments[1]["balance"], "Balance mismatch")
        self.assertEqual(addedDebtPayment2["due_date_time"], viewedDebtPayments[1]["due_date_time"], "Due date/time mismatch")
        self.assertEqual(addedDebtPayment2["note_id"], viewedDebtPayments[1]["note_id"], "Note ID mismatch")
        self.assertEqual(addedNote2["note"], viewedDebtPayments[1]["note"], "Note mismatch")
        self.assertEqual(addedDebtPayment2["currency"], viewedDebtPayments[1]["currency"], "Currency mismatch")

        self.assertEqual(addedDebtPayment3["debt_payment_id"], viewedDebtPayments[2]["debt_payment_id"], "Debt payment ID mismatch")
        self.assertEqual(addedDebtPayment3["debt_transaction_id"], viewedDebtPayments[2]["debt_transaction_id"], "Debt transaction ID mismatch")
        self.assertEqual(addedDebtPayment3["total_debt"], viewedDebtPayments[2]["total_debt"], "Total debt mismatch")
        self.assertEqual(addedDebtPayment3["amount_paid"], viewedDebtPayments[2]["amount_paid"], "Amount paid mismatch")
        self.assertEqual(addedDebtPayment3["balance"], viewedDebtPayments[2]["balance"], "Balance mismatch")
        self.assertEqual(addedDebtPayment3["due_date_time"], viewedDebtPayments[2]["due_date_time"], "Due date/time mismatch")
        self.assertEqual(addedDebtPayment3["note_id"], viewedDebtPayments[2]["note_id"], "Note ID mismatch")
        self.assertEqual(addedNote3["note"], viewedDebtPayments[2]["note"], "Note mismatch")
        self.assertEqual(addedDebtPayment3["currency"], viewedDebtPayments[2]["currency"], "Currency mismatch")

def add_debt_transaction(db, debtorId):
    debtTransaction = {
        "debtor_id": debtorId,
        "transaction_table": "debtor",
        "user_id": 1
    }

    debtTransactionTable = db.schema.get_table("debt_transaction")
    result = debtTransactionTable.insert("debtor_id",
                                            "transaction_table",
                                            "user_id") \
                                    .values(tuple(debtTransaction.values())) \
                                    .execute()
    debtTransaction.update(DatabaseResult(result).fetch_one("debt_transaction_id"))
    return debtTransaction

def add_debt_payment(db, debtTransactionId, totalDebt, amountPaid, noteId):
    debtPayment = {
        "debt_transaction_id": debtTransactionId,
        "total_debt": totalDebt,
        "amount_paid": amountPaid,
        "balance": totalDebt - amountPaid,
        "due_date_time": DatabaseDateTime(datetime.now()).iso_format,
        "note_id": noteId,
        "currency": "NGN",
        "user_id": 1
    }

    debtPaymentTable = db.schema.get_table("debt_payment")
    result = debtPaymentTable.insert("debt_transaction_id",
                                        "total_debt",
                                        "amount_paid",
                                        "balance",
                                        "due_date_time",
                                        "note_id",
                                        "currency",
                                        "user_id") \
                            .values(tuple(debtPayment.values())) \
                            .execute()
    debtPayment.update(DatabaseResult(result).fetch_one("debt_payment_id"))
    return debtPayment

def view_debt_payments(db, debtTransactionId, archived=None):
    sqlResult = db.call_procedure("ViewDebtPayments", (debtTransactionId, archived))
    return DatabaseResult(sqlResult).fetch_all()

def add_note(db, note):
    note = {
        "note": note,
        "table_name": "debtor",
        "user_id": 1
    }
    noteTable = db.schema.get_table("note")
    result = noteTable.insert("note",
                                    "table_name",
                                    "user_id") \
                            .values(tuple(note.values())) \
                            .execute()
    note.update(DatabaseResult(result).fetch_one("note_id"))
    return note

if __name__ == '__main__':
    unittest.main()