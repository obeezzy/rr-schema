#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

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

    saleTransactionTable = db.schema.get_table("sale_transaction")
    result = saleTransactionTable.insert("customer_id",
                                            "customer_name",
                                            "user_id") \
                                    .values(tuple(saleTransaction.values())) \
                                    .execute()
    saleTransaction.update(DatabaseResult(result).fetch_one("sale_transaction_id"))
    return saleTransaction

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

def add_customer(db, clientId):
    customer = {
        "client_id": clientId,
        "user_id": 1
    }

    customerTable = db.schema.get_table("customer")
    result = customerTable.insert("client_id",
                                "user_id") \
                            .values(tuple(customer.values())) \
                            .execute()
    customer.update(DatabaseResult(result).fetch_one("customer_id"))
    return customer

def add_note(db, note, tableName):
    noteDict = {
        "note": note,
        "table_name": tableName,
        "user_id": 1
    }

    noteTable = db.schema.get_table("note")
    result = noteTable.insert("note",
                                "table_name",
                                "user_id") \
                        .values(tuple(noteDict.values())) \
                        .execute()
    noteDict.update(DatabaseResult(result).fetch_one("note_id"))
    return noteDict

def archive_sale_transaction(db, archived, saleTransactionId):
    args = {
        "archived": archived,
        "sale_transaction_id": saleTransactionId,
        "user_id": 1
    }
    sqlResult = db.call_procedure("ArchiveSaleTransaction", tuple(args.values()))
    return DatabaseResult(sqlResult).fetch_all()

def fetch_sale_transactions(db, archived=False):
    saleTransactionTable = db.schema.get_table("sale_transaction")
    rowResult = saleTransactionTable.select("id AS sale_transaction_id",
                                                "customer_id AS customer_id",
                                                "customer_name AS customer_name") \
                                            .where("archived = :archived") \
                                            .bind("archived", archived) \
                                            .execute()
    return DatabaseResult(rowResult).fetch_all()

if __name__ == '__main__':
    unittest.main()