#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

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

    db.execute("""INSERT INTO credit_transaction (creditor_id,
                                                    transaction_table,
                                                    transaction_id,
                                                    note_id,
                                                    user_id)
                VALUES (%s, %s, %s, %s, %s)""", tuple(creditTransaction.values()))
    db.commit()

def archive_credit_transaction(db, archived, transactionTable, transactionId):
    creditTransaction = {
        "archived": archived,
        "transaction_table": transactionTable,
        "transaction_id": transactionId,
        "user_id": 1
    }

    db.call_procedure("ArchiveCreditTransaction",
                        tuple(creditTransaction.values()))

def fetch_credit_transactions(db, archived=False):
    db.execute("""SELECT id AS credit_transaction_id,
                            creditor_id,
                            transaction_table,
                            transaction_id,
                            note_id,
                            user_id
                FROM credit_transaction
                WHERE archived = %s""", [archived])
    results = [] 
    for row in db:
        result = {
            "credit_transaction_id": row["credit_transaction_id"],
            "creditor_id": row["creditor_id"],
            "transaction_table": row["transaction_table"],
            "transacation_id": row["transaction_id"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
