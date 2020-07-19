#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from decimal import Decimal

class AddPurchasePayment(StoredProcedureTestCase):
    def test_add_purchase_payment(self):
        addedClient = add_client(self.db)
        addedVendor = add_vendor(self.db,
                                    clientId=addedClient["client_id"])
        addedPurchaseTransaction = add_purchase_transaction(self.db,
                                                            vendorId=addedVendor["vendor_id"])
        addedNote = add_note(self.db)
        addedPurchasePayment = add_purchase_payment(self.db,
                                                    purchaseTransactionId=addedPurchaseTransaction["purchase_transaction_id"],
                                                    noteId=addedNote["note_id"])
        fetchedPurchasePayment = fetch_purchase_payment(self.db)

        self.assertEqual(addedPurchasePayment["purchase_payment_id"],
                            fetchedPurchasePayment["purchase_payment_id"],
                            "Purchase payment ID mismatch.")
        self.assertEqual(addedPurchasePayment["purchase_transaction_id"],
                            fetchedPurchasePayment["purchase_transaction_id"],
                            "Purchase transaction ID mismatch.")
        self.assertEqual(addedPurchasePayment["amount"],
                            fetchedPurchasePayment["amount"],
                            "Amount mismatch.")
        self.assertEqual(addedPurchasePayment["payment_method"],
                            fetchedPurchasePayment["payment_method"],
                            "Payment method mismatch.")
        self.assertEqual(addedPurchasePayment["currency"],
                            fetchedPurchasePayment["currency"],
                            "Currency mismatch.")
        self.assertEqual(addedPurchasePayment["note_id"],
                            fetchedPurchasePayment["note_id"],
                            "Note ID mismatch.")
        self.assertEqual(addedPurchasePayment["user_id"],
                            fetchedPurchasePayment["user_id"],
                            "User ID mismatch.")

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
                RETURNING id AS client_id,
                    preferred_name,
                    phone_number,
                    user_id""", tuple(client.values()))
    for row in db:
        result = {
            "client_id": row["client_id"],
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

def add_note(db):
    note = {
        "note": "Note",
        "user_id": 1
    }

    db.execute("""INSERT INTO note (note,
                                    user_id)
                VALUES (%s, %s)
                RETURNING id AS note_id,
                    user_id""", tuple(note.values()))
    result = {}
    for row in db:
        result = {
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

def add_purchase_transaction(db, vendorId):
    purchaseTransaction = {
        "vendor_id": vendorId,
        "vendor_name": "Vendor",
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
            "purchase_transaction_id": row["purchase_transaction_id"]
        }
    result.update(purchaseTransaction)
    return result

def add_purchase_payment(db, purchaseTransactionId, noteId):
    purchasePayment = {
        "purchase_transaction_id": purchaseTransactionId,
        "amount": Decimal("100.30"),
        "payment_method": "cash",
        "currency": "NGN",
        "note_id": noteId,
        "user_id": 1
    }

    db.call_procedure("AddPurchasePayment",
                        tuple(purchasePayment.values()))
    result = {}
    for row in db:
        result = {
            "purchase_payment_id": row["purchase_payment_id"]
        }
    result.update(purchasePayment)
    return result

def fetch_purchase_payment(db):
    db.execute("""SELECT id AS purchase_payment_id,
                            purchase_transaction_id,
                            amount,
                            payment_method,
                            currency,
                            note_id,
                            user_id
                FROM purchase_payment""")
    result = {}
    for row in db:
        result = {
            "purchase_payment_id": row["purchase_payment_id"],
            "purchase_transaction_id": row["purchase_transaction_id"],
            "amount": row["amount"],
            "payment_method": row["payment_method"],
            "currency": row["currency"],
            "note_id": row["note_id"],
            "user_id": row["note_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
