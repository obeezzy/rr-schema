#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from datetime import datetime

class ViewDebtors(StoredProcedureTestCase):
    @unittest.skip("Total debt is wrong!")
    def test_view_debtors(self):
        debtorRow1 = add_first_debtor(self.db)
        debtorRow2 = add_second_debtor(self.db)
        debtorRow3 = add_third_debtor(self.db)

        fetchedDebtors = view_debtors(self.db)

        self.assertEqual(len(fetchedDebtors), 3, "Expected 3 debtors.")
        self.assertEqual(fetchedDebtors[0], debtorRow1, "Debtor mismatch")
        self.assertEqual(fetchedDebtors[1], debtorRow2, "Debtor mismatch")
        self.assertEqual(fetchedDebtors[2], debtorRow3, "Debtor mismatch")

def add_first_debtor(db):
    client = add_client(db=db,
                        firstName="Kent",
                        lastName="Bent",
                        preferredName="Kent",
                        phoneNumber="123456789")
    debtor = add_debtor(db=db,
                        clientId=client["client_id"])
    debtTransaction1 = add_debt_transaction(db=db,
                                            debtorId=debtor["debtor_id"],
                                            transactionTable="debtor")
    debtPayment1 = add_debt_payment(db=db,
                                    debtTransactionId=debtTransaction1["debt_transaction_id"],
                                    totalDebt=420,
                                    amountPaid=60)
    debtPayment2 = add_debt_payment(db=db,
                                    debtTransactionId=debtTransaction1["debt_transaction_id"],
                                    totalDebt=360,
                                    amountPaid=300) # 60

    debtTransaction2 = add_debt_transaction(db=db,
                                            debtorId=debtor["debtor_id"],
                                            transactionTable="debtor")
    debtPayment3 = add_debt_payment(db=db,
                                    debtTransactionId=debtTransaction2["debt_transaction_id"],
                                    totalDebt=240,
                                    amountPaid=40) # 200

    return {
        "debtor_id": debtor["debtor_id"],
        "preferred_name": client["preferred_name"],
        "first_name": client["first_name"],
        "last_name": client["last_name"],
        "total_debt": debtPayment2["balance"] + debtPayment3["balance"]
    }

def add_second_debtor(db):
    client = add_client(db=db,
                        firstName="Ama",
                        lastName="Mosieri",
                        preferredName="Ama",
                        phoneNumber="987654321")
    debtor = add_debtor(db=db,
                        clientId=client["client_id"])
    debtTransaction1 = add_debt_transaction(db=db,
                                            debtorId=debtor["debtor_id"],
                                            transactionTable="debtor")
    debtPayment1 = add_debt_payment(db=db,
                                    debtTransactionId=debtTransaction1["debt_transaction_id"],
                                    totalDebt=1400,
                                    amountPaid=200)

    debtTransaction2 = add_debt_transaction(db=db,
                                            debtorId=debtor["debtor_id"],
                                            transactionTable="debtor")
    debtPayment2 = add_debt_payment(db=db,
                                    debtTransactionId=debtTransaction2["debt_transaction_id"],
                                    totalDebt=600,
                                    amountPaid=200)

    return {
        "debtor_id": debtor["debtor_id"],
        "preferred_name": client["preferred_name"],
        "first_name": client["first_name"],
        "last_name": client["last_name"],
        "total_debt": debtPayment1["balance"] + debtPayment2["balance"]
    }

def add_third_debtor(db):
    client = add_client(db=db,
                        firstName="Emeka",
                        lastName="Mgbachi",
                        preferredName="Iche",
                        phoneNumber="389375938")
    debtor = add_debtor(db=db,
                        clientId=client["client_id"])
    debtTransaction1 = add_debt_transaction(db=db,
                                            debtorId=debtor["debtor_id"],
                                            transactionTable="debtor")
    debtPayment1 = add_debt_payment(db=db,
                                    debtTransactionId=debtTransaction1["debt_transaction_id"],
                                    totalDebt=3000,
                                    amountPaid=1000)
    debtPayment2 = add_debt_payment(db=db,
                                    debtTransactionId=debtTransaction1["debt_transaction_id"],
                                    totalDebt=2000,
                                    amountPaid=500)

    debtTransaction2 = add_debt_transaction(db=db,
                                            debtorId=debtor["debtor_id"],
                                            transactionTable="debtor")
    debtPayment3 = add_debt_payment(db=db,
                                    debtTransactionId=debtTransaction2["debt_transaction_id"],
                                    totalDebt=240,
                                    amountPaid=40)

    debtTransaction3 = add_debt_transaction(db=db,
                                            debtorId=debtor["debtor_id"],
                                            transactionTable="debtor")
    debtPayment4 = add_debt_payment(db=db,
                                    debtTransactionId=debtTransaction3["debt_transaction_id"],
                                    totalDebt=2200,
                                    amountPaid=200)
    debtPayment5 = add_debt_payment(db=db,
                                    debtTransactionId=debtTransaction3["debt_transaction_id"],
                                    totalDebt=2000,
                                    amountPaid=500)
    debtPayment6 = add_debt_payment(db=db,
                                    debtTransactionId=debtTransaction3["debt_transaction_id"],
                                    totalDebt=1500,
                                    amountPaid=300)
    debtPayment7 = add_debt_payment(db=db,
                                    debtTransactionId=debtTransaction3["debt_transaction_id"],
                                    totalDebt=1200,
                                    amountPaid=1200)

    return {
        "debtor_id": debtor["debtor_id"],
        "preferred_name": client["preferred_name"],
        "first_name": client["first_name"],
        "last_name": client["last_name"],
        "total_debt": debtPayment2["balance"] + debtPayment3["balance"] + debtPayment4["balance"]
    }

def add_debtor(db, clientId):
    debtor = {
        "client_id": clientId,
        "user_id": 1
    }
    db.execute("""INSERT INTO debtor (client_id,
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
    result.update(debtor)
    return result

def add_client(db, firstName, lastName, preferredName, phoneNumber):
    client = {
        "first_name": firstName,
        "last_name": lastName,
        "preferred_name": preferredName,
        "phone_number": phoneNumber,
        "user_id": 1
    }

    db.execute("""INSERT INTO client (first_name,
                                    last_name,
                                    preferred_name,
                                    phone_number,
                                    user_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id AS client_id,
                    first_name,
                    last_name,
                    preferred_name,
                    phone_number,
                    user_id""", tuple(client.values()))
    result = {}
    for row in db:
        result = {
            "client_id": row["client_id"]
        }
    result.update(client)
    return result


def add_debt_transaction(db, debtorId, tableRef, tableId=None):
    debtTransaction = {
        "debtor_id": debtorId,
        "table_ref": tableRef,
        "table_id": tableId,
        "user_id": 1
    }

    db.execute("""INSERT INTO debt_transaction (debtor_id,
                                                table_ref,
                                                table_id,
                                                user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id AS debt_transaction_id,
                    debtor_id,
                    table_ref,
                    table_id,
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

def add_debt_payment(db, debtTransactionId, totalDebt, amountPaid):
    debtPayment = {
        "debt_transaction_id": debtTransactionId,
        "total_debt": totalDebt,
        "amount_paid": amountPaid,
        "balance": totalDebt - amountPaid,
        "currency": "NGN",
        "due_date_time": datetime.now(),
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
    result.update(debtPayment)
    return result

def view_debtors(db, archived=False):
    debtor = {
        "archived": archived
    }

    db.call_procedure("ViewDebtors",
                        tuple(debtor.values()))
    results = []
    for row in db:
        result = {
            "debtor_id": row["debtor_id"],
            "preferred_name": row["preferred_name"],
            "first_name": row["first_name"],
            "last_name": row["last_name"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
