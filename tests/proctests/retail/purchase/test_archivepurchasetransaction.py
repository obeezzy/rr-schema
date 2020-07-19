#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

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
                        note="Note")
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

    db.execute("""INSERT INTO purchase_transaction (vendor_id,
                                                    vendor_name,
                                                    user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS purchase_transaction_id""", tuple(purchaseTransaction.values()))
    result = {}
    for row in db:
        result = {
            "purchase_transaction_id": row[0]
        }
    result.update(purchaseTransaction)
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

def add_vendor(db, clientId):
    vendor = {
        "client_id": clientId,
        "user_id": 1
    }

    db.execute("""INSERT INTO vendor (client_id,
                                        user_id)
                VALUES (%s, %s)
                RETURNING id AS vendor_id,
                    client_id,
                    user_id""", tuple(vendor.values()))
    for row in db:
        result = {
            "vendor_id": row["vendor_id"],
            "client_id": row["client_id"],
            "user_id": row["user_id"]
        }
    return result

def add_note(db, note):
    note = {
        "note": note,
        "user_id": 1
    }

    db.execute("""INSERT INTO note (note,
                                    user_id)
                VALUES (%s, %s)
                RETURNING id AS note_id""", tuple(note.values()))
    result = {}
    for row in db:
        result = {
            "note_id": row["note_id"]
        }
    return result

def archive_purchase_transaction(db, archived, purchaseTransactionId):
    args = {
        "archived": archived,
        "purchase_transaction_id": purchaseTransactionId,
        "user_id": 1
    }
    db.call_procedure("ArchivePurchaseTransaction", tuple(args.values()))

def fetch_purchase_transactions(db, archived=False):
    db.execute("""SELECT id AS purchase_transaction_id,
                            vendor_id,
                            vendor_name
                FROM purchase_transaction
                WHERE archived = %s""", [archived])
    results = []
    for row in db:
        result = {
            "purchase_transaction_id": row["purchase_transaction_id"],
            "vendor_id": row["vendor_id"],
            "vendor_name": row["vendor_name"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
