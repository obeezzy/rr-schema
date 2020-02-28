#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase, DatabaseResult
from datetime import datetime

class ArchiveDebtTransactionByDebtorId(StoredProcedureTestCase):
    def test_archive_debt_transaction_by_id(self):
        add_single_debt_transaction(db=self.db,
                                    debtorId=1)
        add_single_debt_transaction(db=self.db,
                                    debtorId=2)
        add_single_debt_transaction(db=self.db,
                                    debtorId=3)

        archive_debt_transaction_by_debtor_id(db=self.db,
                                                debtTransactionId=1)

        fetchedDebtTransactions = fetch_debt_transactions(self.db)
        self.assertEqual(len(fetchedDebtTransactions), 2, "Expected 2 debt transactions to be returned.")

        debtTransactionArchived = len([debtTransaction for debtTransaction in fetchedDebtTransactions \
                                        if debtTransaction["debt_transaction_id"] == 1]) == 0
        self.assertEqual(debtTransactionArchived, True, "Debt transaction not archived.")

def add_single_debt_transaction(db, debtorId, transactionTable="debtor"):
    debtTransaction = {
        "debtor_id": debtorId,
        "transaction_table": transactionTable,
        "note_id": 1,
        "user_id": 1
    }

    debtTransactionTable = db.schema.get_table("debt_transaction")
    debtTransactionTable.insert("debtor_id",
                                    "transaction_table",
                                    "note_id ",
                                    "user_id") \
                            .values(tuple(debtTransaction.values())) \
                            .execute()

def archive_debt_transaction_by_debtor_id(db, debtTransactionId):
    debtTransaction = {
        "archived": True,
        "debt_transaction_id": debtTransactionId,
        "user_id": 1
    }

    db.call_procedure("ArchiveDebtTransactionById",
                        tuple(debtTransaction.values()))

def fetch_debt_transactions(db, archived=False):
    debtTransactionTable = db.schema.get_table("debt_transaction")
    rowResult = debtTransactionTable.select("id AS debt_transaction_id",
                                                "debtor_id AS debtor_id",
                                                "transaction_table AS transaction_table",
                                                "note_id AS note_id",
                                                "user_id AS user_id") \
                                        .where("archived = :archived") \
                                        .bind("archived", archived) \
                                        .execute()
    return DatabaseResult(rowResult).fetch_all()

if __name__ == '__main__':
    unittest.main()