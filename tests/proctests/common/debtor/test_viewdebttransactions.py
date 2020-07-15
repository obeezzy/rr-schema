#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase
from datetime import datetime
from decimal import Decimal

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
                                        totalDebt=locale.currency(500.48),
                                        amountPaid=locale.currency(302.12))
        debtPayment2 = add_debt_payment(db=self.db,
                                        debtTransactionId=debtTransaction1["debt_transaction_id"],
                                        totalDebt=locale.currency(2399.23),
                                        amountPaid=locale.currency(302.03))

        debtTransaction2 = add_debt_transaction(db=self.db,
                                                debtorId=debtor1["debtor_id"])
        debtPayment3 = add_debt_payment(db=self.db,
                                        debtTransactionId=debtTransaction2["debt_transaction_id"],
                                        totalDebt=locale.currency(4200.38),
                                        amountPaid=locale.currency(398.45))

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
    add_client(db=db, preferredName=preferredName, phoneNumber=phoneNumber)


def add_client(db, preferredName, phoneNumber, archived=False):
    client = {
        "preferred_name": preferredName,
        "phone_number": phoneNumber,
        "archived": archived,
        "user_id": 1
    }

    db.execute("""INSERT INTO client (preferred_name,
                                        phone_number,
                                        archived,
                                        user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id AS client_id,
                    preferred_name,
                    phone_number,
                    archived,
                    user_id""", tuple(client.values()))
    result = {}
    for row in db:
        result = {
            "client_id": row["client_id"],
            "preferred_name": row["preferred_name"],
            "phone_number": row["phone_number"],
            "archived": row["archived"],
            "user_id": row["user_id"]
        }
    return result

def add_debtor(db, clientId):
    debtor = {
        "client_id": clientId,
        "user_id": 1
    }
    db.execute("""INSERT INTO debtor(client_id,
                                        user_id)
                VALUES (%s, %s)
                RETURNING id AS debtor_id,
                    client_id,
                    user_id""", tuple(debtor.values()))
    result = {}
    for row in db:
        result = {
            "debtor_id": row["debtor_id"],
            "client_id": row["client_id"],
            "user_id": row["user_id"]
        }
    return result

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
    return result

def add_debt_payment(db, debtTransactionId, totalDebt, amountPaid):
    debtPayment = {
        "debt_transaction_id": debtTransactionId,
        "total_debt": totalDebt,
        "amount_paid": amountPaid,
        "balance": locale.currency(Decimal(totalDebt.strip("$")) - Decimal(amountPaid.strip("$"))),
        "currency": "NGN",
        "due_date_time": datetime(2999, 3, 2),
        "user_id": 1
    }

    db.execute("""INSERT INTO debt_payment (debt_transaction_id,
                                            total_debt,
                                            amount_paid,
                                            balance,
                                            currency,
                                            due_date_time,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS debt_payment_id,
                    debt_transaction_id,
                    total_debt,
                    amount_paid,
                    balance,
                    currency,
                    due_date_time,
                    user_id""", tuple(debtPayment.values()))
    result = {}
    for row in db:
        result = {
            "debt_payment_id": row["debt_payment_id"],
            "debt_transaction_id": row["debt_transaction_id"],
            "total_debt": row["total_debt"],
            "amount_paid": row["amount_paid"],
            "balance": row["balance"],
            "currency": row["currency"],
            "due_date_time": row["due_date_time"],
            "user_id": row["user_id"]
        }
    return result

def view_debt_transactions(db, debtorId, archived=False):
    db.call_procedure("ViewDebtTransactions", [debtorId, archived])
    results = []
    for row in db:
        result = {
            "debt_transaction_id": row["debt_transaction_id"],
            "debtor_id": row["debtor_id"],
            "related_transaction_table": row["related_transaction_table"],
            "related_transaction_id": row["related_transaction_id"],
            "debt_payment_id": row["debt_payment_id"],
            "total_debt": row["total_debt"],
            "amount_paid": row["amount_paid"],
            "balance": row["balance"],
            "currency": row["currency"],
            "due_date_time": row["due_date_time"],
            "archived": row["archived"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
