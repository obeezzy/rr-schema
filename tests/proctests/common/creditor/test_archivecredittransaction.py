#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class ArchiveCreditTransaction(StoredProcedureTestCase):
    def test_archive_credit_transaction(self):
        add_single_credit_transaction(db=self.db,
                                        creditorId=1,
                                        transactionTable="sale_transaction",
                                        transactionId=22)
        add_single_credit_transaction(db=self.db,
                                        creditorId=2,
                                        transactionTable="purchase_transaction",
                                        transactionId=40)
        add_single_credit_transaction(db=self.db,
                                        creditorId=3,
                                        transactionTable="income_transaction",
                                        transactionId=58)

        archive_credit_transaction(db=self.db,
                                    archived=True,
                                    transactionTable="sale_transaction",
                                    transactionId=22)

        fetchedCreditTransactions = fetch_credit_transactions(self.db, archived=False)
        self.assertEqual(len(fetchedCreditTransactions), 2, "Expected 2 credit transactions to be returned.")

        creditTransactionArchived = len([creditTransaction for creditTransaction in fetchedCreditTransactions \
                                        if creditTransaction["credit_transaction_id"] == 1]) == 0
        self.assertEqual(creditTransactionArchived, True, "Credit transaction not archived.")

def add_single_credit_transaction(db, creditorId, transactionTable, transactionId):
    creditTransaction = {
        "creditor_id": creditorId,
        "transaction_table": transactionTable,
        "transaction_id": transactionId,
        "note_id": 1,
        "user_id": 1
    }

    creditTransactionTable = db.schema.get_table("credit_transaction")
    creditTransactionTable.insert("creditor_id",
                                    "transaction_table",
                                    "transaction_id",
                                    "note_id ",
                                    "user_id") \
                            .values(tuple(creditTransaction.values())) \
                            .execute()

def archive_credit_transaction(db, archived, transactionTable, transactionId):
    creditTransaction = {
        "archived": archived,
        "transaction_table": transactionTable,
        "transaction_id": transactionId,
        "user_id": 1
    }

    sqlResult = db.call_procedure("ArchiveCreditTransaction",
                                        tuple(creditTransaction.values()))
    creditTransaction.update(DatabaseResult(sqlResult).fetch_one())
    return creditTransaction

def fetch_credit_transactions(db, archived=None):
    creditTransactionTable = db.schema.get_table("credit_transaction")
    rowResult = creditTransactionTable.select("id AS credit_transaction_id",
                                                "creditor_id AS creditor_id",
                                                "transaction_table AS transaction_table",
                                                "transaction_id AS transaction_id",
                                                "note_id AS note_id",
                                                "user_id AS user_id") \
                                        .where("archived = IFNULL(:archived, FALSE)") \
                                        .bind("archived", archived) \
                                        .execute()
    return DatabaseResult(rowResult).fetch_all()

if __name__ == '__main__':
    unittest.main()