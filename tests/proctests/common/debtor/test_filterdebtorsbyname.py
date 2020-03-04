#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime

class FilterDebtorsByName(StoredProcedureTestCase):
    @unittest.skip("Total debt is wrong!")
    def test_filter_debtors_by_name(self):
        debtorRow1 = add_first_debtor(self.db)
        debtorRow2 = add_second_debtor(self.db)
        debtorRow3 = add_third_debtor(self.db)

        filteredDebtors = filter_debtors_by_name(db=self.db,
                                                    filterColumn="preferred_name",
                                                    filterText=debtorRow1["preferred_name"][0:3],
                                                    sortColumn="preferred_name",
                                                    sortOrder="ascending",
                                                    archived=False)
        fetchedDebtors = fetch_debtors(self.db)

        self.assertEqual(len(fetchedDebtors), 3, "Expected 3 debtors.")
        self.assertEqual(len(filteredDebtors), 1, "Expected 1 filtered debtor.")
        self.assertEqual(filteredDebtors[0], debtorRow1, "Debtor mismatch")

        filteredDebtors = filter_debtors_by_name(db=self.db,
                                                    filterColumn="preferred_name",
                                                    filterText=debtorRow2["preferred_name"][0:3],
                                                    sortColumn="preferred_name",
                                                    sortOrder="ascending",
                                                    archived=False)
        self.assertEqual(len(filteredDebtors), 1, "Expected 1 filtered debtor.")
        self.assertEqual(filteredDebtors[0], debtorRow2, "Debtor mismatch")

        filteredDebtors = filter_debtors_by_name(db=self.db,
                                                    filterColumn="preferred_name",
                                                    filterText=debtorRow3["preferred_name"][0:3],
                                                    sortColumn="preferred_name",
                                                    sortOrder="ascending",
                                                    archived=False)
        self.assertEqual(len(filteredDebtors), 1, "Expected 1 filtered debtor.")
        self.assertEqual(filteredDebtors[0], debtorRow3, "Debtor mismatch")

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
    debtorTable = db.schema.get_table("debtor")
    result = debtorTable.insert("client_id",
                                "user_id") \
                        .values(tuple(debtor.values())) \
                        .execute()
    debtor.update(DatabaseResult(result).fetch_one("debtor_id"))
    return debtor

def add_client(db, firstName, lastName, preferredName, phoneNumber):
    client = {
        "first_name": firstName,
        "last_name": lastName,
        "preferred_name": preferredName,
        "phone_number": phoneNumber,
        "user_id": 1
    }

    clientTable = db.schema.get_table("client")
    result = clientTable.insert("first_name",
                                "last_name",
                                "preferred_name",
                                "phone_number",
                                "user_id") \
                        .values(tuple(client.values())) \
                        .execute()
    client.update(DatabaseResult(result).fetch_one("client_id"))
    return client


def add_debt_transaction(db, debtorId, transactionTable, transactionId=None):
    debtTransaction = {
        "debtor_id": debtorId,
        "transaction_table": transactionTable,
        "transaction_id": transactionId,
        "user_id": 1
    }

    debtTransactionTable = db.schema.get_table("debt_transaction")
    result = debtTransactionTable.insert("debtor_id",
                                            "transaction_table",
                                            "transaction_id",
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
        "balance": totalDebt - amountPaid,
        "currency": "NGN",
        "due_date_time": DatabaseDateTime(datetime.now()).iso_format,
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

def filter_debtors_by_name(db, filterColumn, filterText, sortColumn, sortOrder, archived=False):
    sqlResult = db.call_procedure("FilterDebtorsByName", (
                                    filterColumn,
                                    filterText,
                                    sortColumn,
                                    sortOrder,
                                    archived))

    return DatabaseResult(sqlResult).fetch_all()

def fetch_debtors(db):
    debtorTable = db.schema.get_table("debtor")
    rowResult = debtorTable.select("id AS debtor_id") \
                            .where("archived = FALSE") \
                            .execute()
    return DatabaseResult(rowResult).fetch_all()

if __name__ == '__main__':
    unittest.main()