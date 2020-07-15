#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase
from datetime import datetime
from decimal import Decimal

class ViewDebtPayments(StoredProcedureTestCase):
    def test_view_debt_payments(self):
        addedNote1 = add_note(db=self.db, note="First note")
        addedNote2 = add_note(db=self.db, note="Second note")
        addedNote3 = add_note(db=self.db, note="Third note")

        addedDebtTransaction = add_debt_transaction(db=self.db,
                                                    debtorId=1)

        addedDebtPayment1 = add_debt_payment(self.db,
                                                debtTransactionId=addedDebtTransaction["debt_transaction_id"],
                                                totalDebt=locale.currency(750),
                                                amountPaid=locale.currency(250),
                                                noteId=addedNote1["note_id"])
        addedDebtPayment2 = add_debt_payment(self.db,
                                                debtTransactionId=addedDebtTransaction["debt_transaction_id"],
                                                totalDebt=locale.currency(800),
                                                amountPaid=locale.currency(300),
                                                noteId=addedNote2["note_id"])
        addedDebtPayment3 = add_debt_payment(self.db,
                                                debtTransactionId=addedDebtTransaction["debt_transaction_id"],
                                                totalDebt=locale.currency(2100),
                                                amountPaid=locale.currency(200),
                                                noteId=addedNote3["note_id"])

        viewedDebtPayments = view_debt_payments(db=self.db, debtTransactionId=1)

        self.assertEqual(addedDebtPayment1["debt_payment_id"], viewedDebtPayments[0]["debt_payment_id"], "Debt payment ID mismatch.")
        self.assertEqual(addedDebtPayment1["debt_transaction_id"], viewedDebtPayments[0]["debt_transaction_id"], "Debt transaction ID mismatch.")
        self.assertEqual(addedDebtPayment1["total_debt"], viewedDebtPayments[0]["total_debt"], "Total debt mismatch.")
        self.assertEqual(addedDebtPayment1["amount_paid"], viewedDebtPayments[0]["amount_paid"], "Amount paid mismatch.")
        self.assertEqual(addedDebtPayment1["balance"], viewedDebtPayments[0]["balance"], "Balance mismatch.")
        self.assertEqual(addedDebtPayment1["due_date_time"], viewedDebtPayments[0]["due_date_time"], "Due date/time mismatch.")
        self.assertEqual(addedDebtPayment1["note_id"], viewedDebtPayments[0]["note_id"], "Note ID mismatch.")
        self.assertEqual(addedNote1["note"], viewedDebtPayments[0]["note"], "Note mismatch.")
        self.assertEqual(addedDebtPayment1["currency"], viewedDebtPayments[0]["currency"], "Currency mismatch.")

        self.assertEqual(addedDebtPayment2["debt_payment_id"], viewedDebtPayments[1]["debt_payment_id"], "Debt payment ID mismatch.")
        self.assertEqual(addedDebtPayment2["debt_transaction_id"], viewedDebtPayments[1]["debt_transaction_id"], "Debt transaction ID mismatch.")
        self.assertEqual(addedDebtPayment2["total_debt"], viewedDebtPayments[1]["total_debt"], "Total debt mismatch.")
        self.assertEqual(addedDebtPayment2["amount_paid"], viewedDebtPayments[1]["amount_paid"], "Amount paid mismatch.")
        self.assertEqual(addedDebtPayment2["balance"], viewedDebtPayments[1]["balance"], "Balance mismatch.")
        self.assertEqual(addedDebtPayment2["due_date_time"], viewedDebtPayments[1]["due_date_time"], "Due date/time mismatch.")
        self.assertEqual(addedDebtPayment2["note_id"], viewedDebtPayments[1]["note_id"], "Note ID mismatch.")
        self.assertEqual(addedNote2["note"], viewedDebtPayments[1]["note"], "Note mismatch.")
        self.assertEqual(addedDebtPayment2["currency"], viewedDebtPayments[1]["currency"], "Currency mismatch.")

        self.assertEqual(addedDebtPayment3["debt_payment_id"], viewedDebtPayments[2]["debt_payment_id"], "Debt payment ID mismatch.")
        self.assertEqual(addedDebtPayment3["debt_transaction_id"], viewedDebtPayments[2]["debt_transaction_id"], "Debt transaction ID mismatch.")
        self.assertEqual(addedDebtPayment3["total_debt"], viewedDebtPayments[2]["total_debt"], "Total debt mismatch.")
        self.assertEqual(addedDebtPayment3["amount_paid"], viewedDebtPayments[2]["amount_paid"], "Amount paid mismatch.")
        self.assertEqual(addedDebtPayment3["balance"], viewedDebtPayments[2]["balance"], "Balance mismatch.")
        self.assertEqual(addedDebtPayment3["due_date_time"], viewedDebtPayments[2]["due_date_time"], "Due date/time mismatch.")
        self.assertEqual(addedDebtPayment3["note_id"], viewedDebtPayments[2]["note_id"], "Note ID mismatch.")
        self.assertEqual(addedNote3["note"], viewedDebtPayments[2]["note"], "Note mismatch.")
        self.assertEqual(addedDebtPayment3["currency"], viewedDebtPayments[2]["currency"], "Currency mismatch.")

def add_debt_transaction(db, debtorId):
    debtTransaction = {
        "debtor_id": debtorId,
        "transaction_table": "debtor",
        "user_id": 1
    }

    db.execute("""INSERT INTO debt_transaction (debtor_id,
                                                transaction_table,
                                                user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS debt_transaction_id,
                    debtor_id,
                    transaction_table,
                    user_id""", tuple(debtTransaction.values()))
    result = {}
    for row in db:
        result = {
            "debt_transaction_id": row["debt_transaction_id"],
            "debtor_id": row["debtor_id"],
            "transaction_table": row["transaction_table"],
            "user_id": row["user_id"]
        }
    result.update(debtTransaction)
    return result

def add_debt_payment(db, debtTransactionId, totalDebt, amountPaid, noteId):
    debtPayment = {
        "debt_transaction_id": debtTransactionId,
        "total_debt": totalDebt,
        "amount_paid": amountPaid,
        "balance": locale.currency(Decimal(totalDebt.strip("$")) - Decimal(amountPaid.strip("$"))),
        "due_date_time": datetime.now(),
        "note_id": noteId,
        "currency": "NGN",
        "user_id": 1
    }

    db.execute("""INSERT INTO debt_payment (debt_transaction_id,
                                            total_debt,
                                            amount_paid,
                                            balance,
                                            due_date_time,
                                            note_id,
                                            currency,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS debt_payment_id,
                    debt_transaction_id,
                    total_debt,
                    amount_paid,
                    balance,
                    due_date_time,
                    note_id,
                    currency,
                    user_id""", tuple(debtPayment.values()))
    result = {}
    for row in db:
        result = {
            "debt_payment_id": row["debt_payment_id"],
            "debt_transaction_id": row["debt_transaction_id"],
            "total_debt": row["total_debt"],
            "amount_paid": row["amount_paid"],
            "balance": row["balance"],
            "due_date_time": row["due_date_time"],
            "note_id": row["note_id"],
            "currency": row["currency"],
            "user_id": row["user_id"]
        }
    result.update(debtPayment)
    return result

def view_debt_payments(db, debtTransactionId, archived=False):
    db.call_procedure("ViewDebtPayments", [debtTransactionId, archived])
    results = []
    for row in db:
        result = {
            "debt_payment_id": row["debt_payment_id"],
            "debt_transaction_id": row["debt_transaction_id"],
            "total_debt": row["total_debt"].replace(",", ""),
            "amount_paid": row["amount_paid"].replace(",", ""),
            "balance": row["balance"].replace(",", ""),
            "due_date_time": row["due_date_time"],
            "note_id": row["note_id"],
            "note": row["note"],
            "currency": row["currency"]
        }
        results.append(result)
    return results

def add_note(db, note):
    note = {
        "note": note,
        "table_name": "debtor",
        "user_id": 1
    }

    db.execute("""INSERT INTO note (note,
                                    table_name,
                                    user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS note_id,
                    note,
                    table_name,
                    user_id""", tuple(note.values()))
    result = {}
    for row in db:
        result = {
            "note_id": row["note_id"],
            "note": row["note"],
            "table_name": row["table_name"],
            "user_id": row["user_id"]
        }
    result.update(note)
    return result

if __name__ == '__main__':
    unittest.main()
