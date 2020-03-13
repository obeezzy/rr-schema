#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime

class ViewDebtTransactions(StoredProcedureTestCase):
    def test_view_debt_transactions(self):
        client1 = add_client(db=self.db,
                                preferredName="Spider-Man",
                                phoneNumber="1234")
        debtor1 = add_debtor(db=self.db,
                                clientId=client1["client_id"])
        debtTransaction1 = add_debt_transaction(db=self.db,
                                                debtorId=debtor1["debtor_id"])
        debtPayment1 = add_debt_payment(db=self.db,
                                        debtTransactionId=debtTransaction1["debt_transaction_id"],
                                        totalDebt=500.48,
                                        amountPaid=302.12)
        debtPayment2 = add_debt_payment(db=self.db,
                                        debtTransactionId=debtTransaction1["debt_transaction_id"],
                                        totalDebt=2399.23,
                                        amountPaid=302.03)

        debtTransaction2 = add_debt_transaction(db=self.db,
                                                debtorId=debtor1["debtor_id"])
        debtPayment3 = add_debt_payment(db=self.db,
                                        debtTransactionId=debtTransaction2["debt_transaction_id"],
                                        totalDebt=4200.38,
                                        amountPaid=398.45)

        viewedDebtTransactions = view_debt_transactions(db=self.db,
                                                        debtorId=debtor1["debtor_id"])
        self.assertEqual(len(viewedDebtTransactions), 3, "Expected 3 transactions.")
        self.assertEqual(viewedDebtTransactions[0]["related_transaction_table"],
                            debtTransaction1["transaction_table"], 
                            "Related transaction table mismatch.")
        self.assertEqual(viewedDebtTransactions[0]["related_transaction_id"],
                            None,
                            "Related transaction ID mismatch.")
        self.assertEqual(viewedDebtTransactions[0]["debt_payment_id"],
                            debtPayment1["debt_payment_id"],
                            "Debt payment ID mismatch.")
        self.assertEqual(viewedDebtTransactions[0]["total_debt"],
                            debtPayment1["total_debt"],
                            "Total debt mismatch.")
        self.assertEqual(viewedDebtTransactions[0]["amount_paid"],
                            debtPayment1["amount_paid"],
                            "Amount paid mismatch.")
        self.assertEqual(viewedDebtTransactions[0]["balance"],
                            debtPayment1["balance"],
                            "Balance mismatch.")
        self.assertEqual(viewedDebtTransactions[0]["currency"],
                            debtPayment1["currency"],
                            "Currency mismatch.")
        self.assertEqual(viewedDebtTransactions[0]["due_date_time"],
                            debtPayment1["due_date_time"],
                            "Due date/time mismatch.")
        self.assertEqual(viewedDebtTransactions[0]["archived"],
                            False,
                            "Archived flag mismatch.")

        self.assertEqual(viewedDebtTransactions[1]["related_transaction_table"],
                            debtTransaction1["transaction_table"], 
                            "Related transaction table mismatch.")
        self.assertEqual(viewedDebtTransactions[1]["related_transaction_id"],
                            None,
                            "Related transaction ID mismatch.")
        self.assertEqual(viewedDebtTransactions[1]["debt_payment_id"],
                            debtPayment2["debt_payment_id"],
                            "Debt payment ID mismatch.")
        self.assertEqual(viewedDebtTransactions[1]["total_debt"],
                            debtPayment2["total_debt"],
                            "Total debt mismatch.")
        self.assertEqual(viewedDebtTransactions[1]["amount_paid"],
                            debtPayment2["amount_paid"],
                            "Amount paid mismatch.")
        self.assertEqual(viewedDebtTransactions[1]["balance"],
                            debtPayment2["balance"],
                            "Balance mismatch.")
        self.assertEqual(viewedDebtTransactions[1]["currency"],
                            debtPayment2["currency"],
                            "Currency mismatch.")
        self.assertEqual(viewedDebtTransactions[1]["due_date_time"],
                            debtPayment2["due_date_time"],
                            "Due date/time mismatch.")
        self.assertEqual(viewedDebtTransactions[1]["archived"],
                            False,
                            "Archived flag mismatch.")

        self.assertEqual(viewedDebtTransactions[2]["related_transaction_table"],
                            debtTransaction2["transaction_table"], 
                            "Related transaction table mismatch.")
        self.assertEqual(viewedDebtTransactions[2]["related_transaction_id"],
                            None,
                            "Related transaction ID mismatch.")
        self.assertEqual(viewedDebtTransactions[2]["debt_payment_id"],
                            debtPayment3["debt_payment_id"],
                            "Debt payment ID mismatch.")
        self.assertEqual(viewedDebtTransactions[2]["total_debt"],
                            debtPayment3["total_debt"],
                            "Total debt mismatch.")
        self.assertEqual(viewedDebtTransactions[2]["amount_paid"],
                            debtPayment3["amount_paid"],
                            "Amount paid mismatch.")
        self.assertEqual(viewedDebtTransactions[2]["balance"],
                            debtPayment3["balance"],
                            "Balance mismatch.")
        self.assertEqual(viewedDebtTransactions[2]["currency"],
                            debtPayment3["currency"],
                            "Currency mismatch.")
        self.assertEqual(viewedDebtTransactions[2]["due_date_time"],
                            debtPayment3["due_date_time"],
                            "Due date/time mismatch.")
        self.assertEqual(viewedDebtTransactions[2]["archived"],
                            False,
                            "Archived flag mismatch.")


def add_debtor_with_transactions(db, preferredName, phoneNumber):
    client = add_client(db=db, preferredName=preferredName, phoneNumber=phoneNumber)


def add_client(db, preferredName, phoneNumber, archived=False):
    client = {
        "preferred_name": preferredName,
        "phone_number": phoneNumber,
        "archived": archived,
        "user_id": 1
    }

    clientTable = db.schema.get_table("client")
    result = clientTable.insert("preferred_name",
                                "phone_number",
                                "archived",
                                "user_id") \
                        .values(tuple(client.values())) \
                        .execute()
    client.update(DatabaseResult(result).fetch_one("client_id"))
    return client

def add_debtor(db, clientId):
    debtor = {
        "client_id": clientId,
        "user_id": 1
    }

    debtorTable = db.schema.get_table("debtor")
    result = debtorTable.insert("client_id",
                                "user_id") \
                        .values(tuple(debtor.values())) \
                        .execute()
    debtor.update(DatabaseResult(result).fetch_one("debtor_id"))
    return debtor

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

def add_debt_payment(db, debtTransactionId, totalDebt, amountPaid):
    debtPayment = {
        "debt_transaction_id": debtTransactionId,
        "total_debt": totalDebt,
        "amount_paid": amountPaid,
        "balance": round(totalDebt - amountPaid, 2),
        "currency": "NGN",
        "due_date_time": DatabaseDateTime(datetime(2999, 3, 2)).iso_format,
        "user_id": 1
    }

    debtPaymentTable = db.schema.get_table("debt_payment")
    result = debtPaymentTable.insert("debt_transaction_id",
                                        "total_debt",
                                        "amount_paid",
                                        "balance",
                                        "currency",
                                        "due_date_time",
                                        "user_id") \
                                    .values(tuple(debtPayment.values())) \
                                    .execute()
    debtPayment.update(DatabaseResult(result).fetch_one("debt_payment_id"))
    return debtPayment

def view_debt_transactions(db, debtorId, archived=None):
    sqlResult = db.call_procedure("ViewDebtTransactions", (debtorId, archived))
    return DatabaseResult(sqlResult).fetch_all()

if __name__ == '__main__':
    unittest.main()