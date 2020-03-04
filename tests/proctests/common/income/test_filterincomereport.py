#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime, timedelta

class FilterIncomeReport(StoredProcedureTestCase):
    def test_filter_income_report(self):
        incomeTransaction1 = add_income_transaction(db=self.db,
                                                        clientName="Jack Dorsey",
                                                        purpose="Buy Twitter",
                                                        amount=40)
        incomeTransaction2 = add_income_transaction(db=self.db,
                                                        clientName="Elon Musk",
                                                        purpose="Buy Tesla",
                                                        amount=90)
        incomeTransaction3 = add_income_transaction(db=self.db,
                                                        clientName="Mark Zuckerberg",
                                                        purpose="Buy Facebook",
                                                        amount=190)

        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        filteredIncomeReport = filter_income_report(db=self.db,
                                                        filterColumn="purpose",
                                                        filterText=incomeTransaction1["purpose"][0:6],
                                                        sortColumn="purpose",
                                                        sortOrder="ascending",
                                                        fromDateTime=today,
                                                        toDateTime=tomorrow)
        fetchedIncomeTransactions = fetch_income_transactions(self.db)

        self.assertEqual(len(fetchedIncomeTransactions), 3, "Expected 3 transactions.")
        self.assertEqual(len(filteredIncomeReport), 1, "Expected 1 transaction.")
        self.assertEqual(filteredIncomeReport[0]["income_transaction_id"], incomeTransaction1["income_transaction_id"], "Income transaction ID mismatch")
        self.assertEqual(filteredIncomeReport[0]["purpose"], incomeTransaction1["purpose"], "Purpose mismatch")
        self.assertEqual(filteredIncomeReport[0]["amount"], incomeTransaction1["amount"], "Amount mismatch")

        filteredIncomeReport = filter_income_report(db=self.db,
                                                        filterColumn="purpose",
                                                        filterText=incomeTransaction2["purpose"][0:6],
                                                        sortColumn="purpose",
                                                        sortOrder="ascending",
                                                        fromDateTime=today,
                                                        toDateTime=tomorrow)
        self.assertEqual(len(fetchedIncomeTransactions), 3, "Expected 3 transactions.")
        self.assertEqual(len(filteredIncomeReport), 1, "Expected 1 transaction.")
        self.assertEqual(filteredIncomeReport[0]["income_transaction_id"], incomeTransaction2["income_transaction_id"], "Income transaction ID mismatch")
        self.assertEqual(filteredIncomeReport[0]["purpose"], incomeTransaction2["purpose"], "Purpose mismatch")
        self.assertEqual(filteredIncomeReport[0]["amount"], incomeTransaction2["amount"], "Amount mismatch")

        filteredIncomeReport = filter_income_report(db=self.db,
                                                        filterColumn="purpose",
                                                        filterText=incomeTransaction3["purpose"][0:6],
                                                        sortColumn="purpose",
                                                        sortOrder="ascending",
                                                        fromDateTime=today,
                                                        toDateTime=tomorrow)
        self.assertEqual(len(fetchedIncomeTransactions), 3, "Expected 3 transactions.")
        self.assertEqual(len(filteredIncomeReport), 1, "Expected 1 transaction.")
        self.assertEqual(filteredIncomeReport[0]["income_transaction_id"], incomeTransaction3["income_transaction_id"], "Income transaction ID mismatch")
        self.assertEqual(filteredIncomeReport[0]["purpose"], incomeTransaction3["purpose"], "Purpose mismatch")
        self.assertEqual(filteredIncomeReport[0]["amount"], incomeTransaction3["amount"], "Amount mismatch")

def add_income_transaction(db, clientName, purpose, amount):
    incomeTransaction = {
        "client_name": clientName,
        "purpose": purpose,
        "amount": amount,
        "payment_method": "cash",
        "currency": "NGN",
        "user_id": 1
    }

    incomeTransactionTable = db.schema.get_table("income_transaction")
    result = incomeTransactionTable.insert("client_name",
                                            "purpose",
                                            "amount",
                                            "payment_method",
                                            "currency",
                                            "user_id") \
                                    .values(tuple(incomeTransaction.values())) \
                                    .execute()
    incomeTransaction.update(DatabaseResult(result).fetch_one("income_transaction_id"))
    return incomeTransaction

def filter_income_report(db, filterColumn, filterText, sortColumn, sortOrder, fromDateTime, toDateTime):
    sqlResult = db.call_procedure("FilterIncomeReport", (
                                    filterColumn,
                                    filterText,
                                    sortColumn,
                                    sortOrder,
                                    DatabaseDateTime(fromDateTime).iso_format,
                                    DatabaseDateTime(toDateTime).iso_format))

    return DatabaseResult(sqlResult).fetch_all()

def fetch_income_transactions(db):
    incomeTransactionTable = db.schema.get_table("income_transaction")
    rowResult = incomeTransactionTable.select("id AS income_transaction_id",
                                                "client_name AS client_name",
                                                "purpose AS purpose",
                                                "amount AS amount",
                                                "payment_method AS payment_method",
                                                "currency AS currency",
                                                "user_id AS user_id") \
                                        .where("archived = FALSE") \
                                        .execute()
    return DatabaseResult(rowResult).fetch_all()

if __name__ == '__main__':
    unittest.main()