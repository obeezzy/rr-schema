#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

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

    db.execute("""INSERT INTO debt_transaction (debtor_id,
                                                transaction_table,
                                                note_id,
                                                user_id)
                VALUES (%s, %s, %s, %s)""", tuple(debtTransaction.values()))

def archive_debt_transaction_by_debtor_id(db, debtTransactionId):
    debtTransaction = {
        "archived": True,
        "debt_transaction_id": debtTransactionId,
        "user_id": 1
    }

    db.call_procedure("ArchiveDebtTransactionById",
                       tuple(debtTransaction.values()))

def fetch_debt_transactions(db, archived=False):
    db.execute("""SELECT id AS debt_transaction_id
                FROM debt_transaction
                WHERE archived = %s""", [archived])
    results = []
    for row in db:
        result = {
            "debt_transaction_id": row["debt_transaction_id"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
