#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class ArchiveDebtTransactionByTransactionTable(StoredProcedureTestCase):
    def test_archive_debt_transaction(self):
        client1 = add_client(self.db,
                                preferredName="Name 1",
                                phoneNumber="12")
        client2 = add_client(self.db,
                                preferredName="Name 2",
                                phoneNumber="123")
        client3 = add_client(self.db,
                                preferredName="Name 3",
                                phoneNumber="1234")

        debtor1 = add_debtor(self.db,
                                clientId=client1["client_id"])
        debtor2 = add_debtor(self.db,
                                clientId=client2["client_id"])
        debtor3 = add_debtor(self.db,
                                clientId=client3["client_id"])

        debtTransaction1 = add_debt_transaction(db=self.db,
                                                debtorId=debtor1["debtor_id"],
                                                tableRef="sale_transaction",
                                                tableId=22)
        debtTransaction2 = add_debt_transaction(db=self.db,
                                                debtorId=debtor2["debtor_id"],
                                                tableRef="purchase_transaction",
                                                tableId=40)
        debtTransaction3 = add_debt_transaction(db=self.db,
                                                debtorId=debtor3["debtor_id"],
                                                tableRef="income_transaction",
                                                tableId=58)

        archive_debt_transaction(db=self.db,
                                    archived=True,
                                    tableRef="sale_transaction",
                                    tableId=22)

        fetchedDebtTransactions = fetch_debt_transactions(self.db, archived=False)
        self.assertEqual(len(fetchedDebtTransactions), 2, "Expected 2 debt transactions to be returned.")

        debtTransactionArchived = len([dt for dt in fetchedDebtTransactions \
                                        if dt["debt_transaction_id"] == debtTransaction1["debt_transaction_id"]]) == 0
        self.assertEqual(debtTransactionArchived, True, "Debt transaction not archived.")

def add_client(db, preferredName, phoneNumber):
    client = {
        "preferred_name": preferredName,
        "phone_number": phoneNumber,
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

def add_debtor(db, clientId):
    debtor = {
        "client_id": clientId,
        "user_id": 1
    }

    db.execute("""INSERT INTO debtor (client_id,
                                        user_id)
                VALUES (%s, %s)
                RETURNING id AS debtor_id""", tuple(debtor.values()))
    result = {}
    for row in db:
        result = {
            "debtor_id": row["debtor_id"]
        }
    result.update(debtor)
    return result

def add_debt_transaction(db, debtorId, tableRef, tableId):
    debtTransaction = {
        "debtor_id": debtorId,
        "table_ref": tableRef,
        "table_id": tableId,
        "note_id": None,
        "user_id": 1
    }

    db.execute("""INSERT INTO debt_transaction (debtor_id,
                                                table_ref,
                                                table_id,
                                                note_id,
                                                user_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id AS debt_transaction_id""", tuple(debtTransaction.values()))
    result = {}
    for row in db:
        result = {
            "debt_transaction_id": row["debt_transaction_id"]
        }
    return result

def archive_debt_transaction(db, archived, tableRef, tableId):
    debtTransaction = {
        "archived": archived,
        "table_ref": tableRef,
        "tableId": tableId,
        "user_id": 1
    }

    db.call_procedure("ArchiveDebtTransactionByTransactionTable",
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
