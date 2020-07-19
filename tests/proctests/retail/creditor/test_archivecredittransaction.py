#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class ArchiveCreditTransaction(StoredProcedureTestCase):
    def test_archive_credit_transaction(self):
        addedClient = add_client(self.db)
        addedCreditor = add_creditor(self.db, clientId=addedClient["client_id"])
        addedNote = add_note(self.db)
        add_credit_transaction(db=self.db,
                                        creditorId=addedCreditor["creditor_id"],
                                        tableRef="sale_transaction",
                                        tableId=22,
                                        noteId=addedNote["note_id"])
        add_credit_transaction(db=self.db,
                                        creditorId=addedCreditor["creditor_id"],
                                        tableRef="purchase_transaction",
                                        tableId=40,
                                        noteId=addedNote["note_id"])
        add_credit_transaction(db=self.db,
                                        creditorId=addedCreditor["creditor_id"],
                                        tableRef="income_transaction",
                                        tableId=58,
                                        noteId=addedNote["note_id"])

        archive_credit_transaction(db=self.db,
                                    archived=True,
                                    tableRef="sale_transaction",
                                    tableId=22)

        fetchedCreditTransactions = fetch_credit_transactions(self.db, archived=False)
        self.assertEqual(len(fetchedCreditTransactions), 2, "Expected 2 credit transactions to be returned.")

        creditTransactionArchived = len([creditTransaction for creditTransaction in fetchedCreditTransactions \
                                        if creditTransaction["credit_transaction_id"] == 1]) == 0
        self.assertEqual(creditTransactionArchived, True, "Credit transaction not archived.")

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

def add_creditor(db, clientId):
    creditor = {
        "client_id": clientId,
        "user_id": 1
    }

    db.execute("""INSERT INTO creditor (client_id,
                                        user_id)
                VALUES (%s, %s)
                RETURNING id AS creditor_id""", tuple(creditor.values()))
    result = {}
    for row in db:
        result = {
            "creditor_id": row["creditor_id"]
        }
    result.update(creditor)
    return result

def add_note(db):
    note = {
        "note": "Note",
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
            "note_id": row["note_id"]
        }
    return result

def add_credit_transaction(db, creditorId, tableRef, tableId, noteId):
    creditTransaction = {
        "creditor_id": creditorId,
        "table_ref": tableRef,
        "transaction_id": tableId,
        "note_id": noteId,
        "user_id": 1
    }

    db.execute("""INSERT INTO credit_transaction (creditor_id,
                                                    table_ref,
                                                    table_id,
                                                    note_id,
                                                    user_id)
                VALUES (%s, %s, %s, %s, %s)""", tuple(creditTransaction.values()))
    db.commit()

def archive_credit_transaction(db, archived, tableRef, tableId):
    creditTransaction = {
        "archived": archived,
        "table_ref": tableRef,
        "table_id": tableId,
        "user_id": 1
    }

    db.call_procedure("ArchiveCreditTransaction",
                        tuple(creditTransaction.values()))

def fetch_credit_transactions(db, archived=False):
    db.execute("""SELECT id AS credit_transaction_id,
                            creditor_id,
                            table_ref,
                            table_id,
                            note_id,
                            user_id
                FROM credit_transaction
                WHERE archived = %s""", [archived])
    results = [] 
    for row in db:
        result = {
            "credit_transaction_id": row["credit_transaction_id"],
            "creditor_id": row["creditor_id"],
            "table_ref": row["table_ref"],
            "table_id": row["table_id"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
