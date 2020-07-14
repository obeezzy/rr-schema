#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class ArchiveSaleTransaction(StoredProcedureTestCase):
    def test_archive_sale_transaction(self):
        client = add_client(db=self.db,
                            firstName="Carol",
                            lastName="Denvers",
                            preferredName="Ms. Marvel",
                            phoneNumber="38492847")
        customer = add_customer(db=self.db,
                            clientId=client["client_id"])
        note = add_note(db=self.db,
                        note="Note",
                        tableName="sale")
        saleTransaction1 = add_sale_transaction(self.db,
                                                    customerId=customer["customer_id"],
                                                    customerName=client["preferred_name"])
        saleTransaction2 = add_sale_transaction(self.db,
                                                    customerId=None,
                                                    customerName="Conceited")
        saleTransaction3 = add_sale_transaction(self.db,
                                                    customerId=None,
                                                    customerName="Dumbfoundead")

        archive_sale_transaction(db=self.db,
                                    archived=True,
                                    saleTransactionId=saleTransaction2["sale_transaction_id"])
        fetchedSaleTransactions = fetch_sale_transactions(db=self.db)

        self.assertEqual(len(fetchedSaleTransactions), 2, "Expected 2 transactions.")
        self.assertEqual(fetchedSaleTransactions[0]["sale_transaction_id"],
                            saleTransaction1["sale_transaction_id"],
                            "Sale transaction ID mismatch.")
        self.assertEqual(fetchedSaleTransactions[0]["customer_name"],
                            saleTransaction1["customer_name"],
                            "Customer name mismatch.")
        self.assertEqual(fetchedSaleTransactions[0]["customer_id"],
                            saleTransaction1["customer_id"],
                            "Customer ID mismatch.")

        self.assertEqual(fetchedSaleTransactions[1]["sale_transaction_id"],
                            saleTransaction3["sale_transaction_id"],
                            "Sale transaction ID mismatch.")
        self.assertEqual(fetchedSaleTransactions[1]["customer_name"],
                            saleTransaction3["customer_name"],
                            "Customer name mismatch.")
        self.assertEqual(fetchedSaleTransactions[1]["customer_id"],
                            saleTransaction3["customer_id"],
                            "Customer ID mismatch.")

def add_sale_transaction(db, customerId, customerName):
    saleTransaction = {
        "customer_id": customerId,
        "customer_name": customerName,
        "user_id": 1
    }

    db.execute("""INSERT INTO sale_transaction (customer_id,
                                                customer_name,
                                                user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS sale_transaction_id,
                    customer_id,
                    customer_name,
                    user_id""", tuple(saleTransaction.values()))
    result = {}
    for row in db:
        result = {
            "sale_transaction_id": row["sale_transaction_id"],
            "customer_id": row["customer_id"],
            "customer_name": row["customer_name"],
            "user_id": row["user_id"]
        }
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
            "client_id": row["client_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "preferred_name": row["preferred_name"],
            "phone_number": row["phone_number"],
            "user_id": row["user_id"]
        }
    return result

def add_customer(db, clientId):
    customer = {
        "client_id": clientId,
        "user_id": 1
    }

    db.execute("""INSERT INTO customer (client_id,
                                        user_id)
                VALUES (%s, %s)
                RETURNING id AS customer_id,
                    client_id,
                    user_id""", tuple(customer.values()))
    result = {}
    for row in db:
        result = {
            "customer_id": row["customer_id"],
            "client_id": row["client_id"],
            "user_id": row["user_id"]
        }
    return result

def add_note(db, note, tableName):
    note = {
        "note": note,
        "table_name": tableName,
        "user_id": 1
    }

    db.execute("""INSERT INTO note (note,
                                    table_name,
                                    user_id)
                VALUES (%s, %s, %s)
                RETURNING Id AS note_id,
                    note,
                    table_name,
                    user_id""", tuple(note.values()))
    result = {}
    for row in db:
        result = {
            "note_id": row["note_id"],
            "note": row["note"],
            "table_name": row["table_name"],
            "user_id": row["user_id"]
        }
    return result

def archive_sale_transaction(db, archived, saleTransactionId):
    args = {
        "archived": archived,
        "sale_transaction_id": saleTransactionId,
        "user_id": 1
    }
    db.call_procedure("ArchiveSaleTransaction", tuple(args.values()))

def fetch_sale_transactions(db, archived=False):
    db.execute("""SELECT id AS sale_transaction_id,
                            customer_id,
                            customer_name
                FROM sale_transaction
                WHERE archived = %s""", [archived])
    results = []
    for row in db:
        result = {
            "sale_transaction_id": row["sale_transaction_id"],
            "customer_id": row["customer_id"],
            "customer_name": row["customer_name"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
