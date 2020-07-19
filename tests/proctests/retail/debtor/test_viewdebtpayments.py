#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from datetime import datetime
from decimal import Decimal

class ViewDebtPayments(StoredProcedureTestCase):
    def test_view_debt_payments(self):
        addedClient = add_client(self.db)
        addedDebtor = add_debtor(self.db,
                                    clientId=addedClient["client_id"])
        addedDebtTransaction = add_debt_transaction(self.db,
                                                    debtorId=addedDebtor["debtor_id"])
        addedNote1 = add_note(db=self.db, note="First note")
        addedNote2 = add_note(db=self.db, note="Second note")
        addedNote3 = add_note(db=self.db, note="Third note")

        addedDebtTransaction = add_debt_transaction(db=self.db,
                                                    debtorId=addedDebtor["debtor_id"])

        addedDebtPayment1 = add_debt_payment(self.db,
                                                debtTransactionId=addedDebtTransaction["debt_transaction_id"],
                                                totalDebt=Decimal("750"),
                                                amountPaid=Decimal("250"),
                                                noteId=addedNote1["note_id"])
        addedDebtPayment2 = add_debt_payment(self.db,
                                                debtTransactionId=addedDebtTransaction["debt_transaction_id"],
                                                totalDebt=Decimal("800"),
                                                amountPaid=Decimal("300"),
                                                noteId=addedNote2["note_id"])
        addedDebtPayment3 = add_debt_payment(self.db,
                                                debtTransactionId=addedDebtTransaction["debt_transaction_id"],
                                                totalDebt=Decimal("2100"),
                                                amountPaid=Decimal("200"),
                                                noteId=addedNote3["note_id"])

        viewedDebtPayments = view_debt_payments(db=self.db, debtTransactionId=addedDebtTransaction["debt_transaction_id"])

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

def add_client(db):
    client = {
        "preferred_name": "Preferred name",
        "phone_number": "1234",
        "user_id": 1
    }

    db.execute("""INSERT INTO client (preferred_name,
                                        phone_number,
                                        user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS client_id""", tuple(client.values()))
    result = {}
    for row in db:
        result = {
            "client_id": row["client_id"]
        }
    result.update(client)
    return result

def add_debtor(db, clientId):
    debtor = {
        "client_id": clientId,
        "user_id": 1
    }

    db.execute("""INSERT INTO debtor (client_id,
                                        user_id)
                VALUES (%s, %s)
                RETURNING id AS debtor_id""", tuple(debtor.values()))
    result = {}
    for row in db:
        result = {
            "debtor_id": row["debtor_id"]
        }
    result.update(debtor)
    return result

def add_debt_transaction(db, debtorId):
    debtTransaction = {
        "debtor_id": debtorId,
        "table_ref": "debtor",
        "user_id": 1
    }

    db.execute("""INSERT INTO debt_transaction (debtor_id,
                                                table_ref,
                                                user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS debt_transaction_id,
                    debtor_id,
                    table_ref,
                    user_id""", tuple(debtTransaction.values()))
    result = {}
    for row in db:
        result = {
            "debt_transaction_id": row["debt_transaction_id"],
            "debtor_id": row["debtor_id"],
            "table_ref": row["table_ref"],
            "user_id": row["user_id"]
        }
    result.update(debtTransaction)
    return result

def add_debt_payment(db, debtTransactionId, totalDebt, amountPaid, noteId):
    debtPayment = {
        "debt_transaction_id": debtTransactionId,
        "total_debt": totalDebt,
        "amount_paid": amountPaid,
        "balance": totalDebt - amountPaid,
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
            "total_debt": row["total_debt"],
            "amount_paid": row["amount_paid"],
            "balance": row["balance"],
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
        "user_id": 1
    }

    db.execute("""INSERT INTO note (note,
                                    user_id)
                VALUES (%s, %s)
                RETURNING id AS note_id,
                    note,
                    user_id""", tuple(note.values()))
    result = {}
    for row in db:
        result = {
            "note_id": row["note_id"],
            "note": row["note"],
            "user_id": row["user_id"]
        }
    result.update(note)
    return result

if __name__ == '__main__':
    unittest.main()
