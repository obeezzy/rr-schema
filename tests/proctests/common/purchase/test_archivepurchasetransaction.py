#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class ArchivePurchaseTransaction(StoredProcedureTestCase):
    def test_archive_purchase_transaction(self):
        client = add_client(db=self.db,
                            firstName="Carol",
                            lastName="Denvers",
                            preferredName="Ms. Marvel",
                            phoneNumber="38492847")
        vendor = add_vendor(db=self.db,
                            clientId=client["client_id"])
        note = add_note(db=self.db,
                        note="Note",
                        tableName="purchase")
        purchaseTransaction1 = add_purchase_transaction(self.db,
                                                        vendorId=vendor["vendor_id"],
                                                        vendorName=client["preferred_name"])
        purchaseTransaction2 = add_purchase_transaction(self.db,
                                                        vendorId=None,
                                                        vendorName="Conceited")
        purchaseTransaction3 = add_purchase_transaction(self.db,
                                                        vendorId=None,
                                                        vendorName="Dumbfoundead")

        archive_purchase_transaction(db=self.db,
                                        archived=True,
                                        purchaseTransactionId=purchaseTransaction2["purchase_transaction_id"])
        fetchedPurchaseTransactions = fetch_purchase_transactions(db=self.db)

        self.assertEqual(len(fetchedPurchaseTransactions), 2, "Expected 3 transactions.")
        self.assertEqual(fetchedPurchaseTransactions[0]["purchase_transaction_id"],
                            purchaseTransaction1["purchase_transaction_id"],
                            "Purchase transaction ID mismatch.")
        self.assertEqual(fetchedPurchaseTransactions[0]["vendor_name"],
                            purchaseTransaction1["vendor_name"],
                            "Vendor name mismatch.")
        self.assertEqual(fetchedPurchaseTransactions[0]["vendor_id"],
                            purchaseTransaction1["vendor_id"],
                            "Vendor ID mismatch.")

        self.assertEqual(fetchedPurchaseTransactions[1]["purchase_transaction_id"],
                            purchaseTransaction3["purchase_transaction_id"],
                            "Purchase transaction ID mismatch.")
        self.assertEqual(fetchedPurchaseTransactions[1]["vendor_name"],
                            purchaseTransaction3["vendor_name"],
                            "Vendor name mismatch.")
        self.assertEqual(fetchedPurchaseTransactions[1]["vendor_id"],
                            purchaseTransaction3["vendor_id"],
                            "Vendor ID mismatch.")

def add_purchase_transaction(db, vendorId, vendorName):
    purchaseTransaction = {
        "vendor_id": vendorId,
        "vendor_name": vendorName,
        "user_id": 1
    }

    purchaseTransactionTable = db.schema.get_table("purchase_transaction")
    result = purchaseTransactionTable.insert("vendor_id",
                                                "vendor_name",
                                                "user_id") \
                                        .values(tuple(purchaseTransaction.values())) \
                                        .execute()
    purchaseTransaction.update(DatabaseResult(result).fetch_one("purchase_transaction_id"))
    return purchaseTransaction

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

def add_vendor(db, clientId):
    vendor = {
        "client_id": clientId,
        "user_id": 1
    }

    vendorTable = db.schema.get_table("vendor")
    result = vendorTable.insert("client_id",
                                "user_id") \
                            .values(tuple(vendor.values())) \
                            .execute()
    vendor.update(DatabaseResult(result).fetch_one("vendor_id"))
    return vendor

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

def archive_purchase_transaction(db, archived, purchaseTransactionId):
    args = {
        "archived": archived,
        "purchase_transaction_id": purchaseTransactionId,
        "user_id": 1
    }
    sqlResult = db.call_procedure("ArchivePurchaseTransaction", tuple(args.values()))
    return DatabaseResult(sqlResult).fetch_all()

def fetch_purchase_transactions(db, archived=False):
    purchaseTransactionTable = db.schema.get_table("purchase_transaction")
    rowResult = purchaseTransactionTable.select("id AS purchase_transaction_id",
                                                "vendor_id AS vendor_id",
                                                "vendor_name AS vendor_name") \
                                            .where("archived = :archived") \
                                            .bind("archived", archived) \
                                            .execute()
    return DatabaseResult(rowResult).fetch_all()

if __name__ == '__main__':
    unittest.main()