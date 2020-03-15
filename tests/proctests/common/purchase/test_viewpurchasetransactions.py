#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime, timedelta

class ViewPurchaseTransactions(StoredProcedureTestCase):
    def test_view_purchase_transactions(self):
        purchaseTransaction1 = add_first_purchase_transaction(self.db)
        purchaseTransaction2 = add_second_purchase_transaction(self.db)
        purchaseTransaction3 = add_third_purchase_transaction(self.db)

        beginningOfDay = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
        minuteFromNow = datetime.now() + timedelta(minutes=1)
        viewedPurchaseTransactions = view_purchase_transactions(db=self.db,
                                                                fromDateTime=beginningOfDay,
                                                                toDateTime=minuteFromNow)

        self.assertEqual(len(viewedPurchaseTransactions), 3, "Expected 3 transactions.")
        self.assertEqual(viewedPurchaseTransactions[0]["purchase_transaction_id"],
                            purchaseTransaction1["purchase_transaction_id"],
                            "Purchase transaction ID mismatch.")
        self.assertEqual(viewedPurchaseTransactions[0]["vendor_name"],
                            purchaseTransaction1["vendor_name"],
                            "Vendor name mismatch.")
        self.assertEqual(viewedPurchaseTransactions[0]["vendor_id"],
                            purchaseTransaction1["vendor_id"],
                            "Vendor ID mismatch.")
        self.assertEqual(viewedPurchaseTransactions[0]["discount"],
                            purchaseTransaction1["discount"],
                            "Discount mismatch.")
        self.assertEqual(viewedPurchaseTransactions[0]["suspended"],
                            purchaseTransaction1["suspended"],
                            "Suspended flag mismatch.")
        self.assertEqual(viewedPurchaseTransactions[0]["total_amount"],
                            purchaseTransaction1["total_amount"],
                            "Total amount mismatch.")

        self.assertEqual(viewedPurchaseTransactions[1]["purchase_transaction_id"],
                            purchaseTransaction2["purchase_transaction_id"],
                            "Purchase transaction ID mismatch.")
        self.assertEqual(viewedPurchaseTransactions[1]["vendor_name"],
                            purchaseTransaction2["vendor_name"],
                            "Vendor name mismatch.")
        self.assertEqual(viewedPurchaseTransactions[1]["vendor_id"],
                            purchaseTransaction2["vendor_id"],
                            "Vendor ID mismatch.")
        self.assertEqual(viewedPurchaseTransactions[1]["discount"],
                            purchaseTransaction2["discount"],
                            "Discount mismatch.")
        self.assertEqual(viewedPurchaseTransactions[1]["suspended"],
                            purchaseTransaction2["suspended"],
                            "Suspended flag mismatch.")
        self.assertEqual(viewedPurchaseTransactions[1]["total_amount"],
                            purchaseTransaction2["total_amount"],
                            "Total amount mismatch.")

        self.assertEqual(viewedPurchaseTransactions[2]["purchase_transaction_id"],
                            purchaseTransaction3["purchase_transaction_id"],
                            "Purchase transaction ID mismatch.")
        self.assertEqual(viewedPurchaseTransactions[2]["vendor_name"],
                            purchaseTransaction3["vendor_name"],
                            "Vendor name mismatch.")
        self.assertEqual(viewedPurchaseTransactions[2]["vendor_id"],
                            purchaseTransaction3["vendor_id"],
                            "Vendor ID mismatch.")
        self.assertEqual(viewedPurchaseTransactions[2]["discount"],
                            purchaseTransaction3["discount"],
                            "Discount mismatch.")
        self.assertEqual(viewedPurchaseTransactions[2]["suspended"],
                            purchaseTransaction3["suspended"],
                            "Suspended flag mismatch.")
        self.assertEqual(viewedPurchaseTransactions[2]["total_amount"],
                            purchaseTransaction3["total_amount"],
                            "Total amount mismatch.")

def add_first_purchase_transaction(db):
    purchaseTransaction = add_purchase_transaction(db=db,
                                                    vendorName="Miles Morales")
    purchasePayment1 = add_purchase_payment(db=db,
                                            purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                            amount=340.45,
                                            paymentMethod="cash")
    purchasePayment2 = add_purchase_payment(db=db,
                                            purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                            amount=440.45,
                                            paymentMethod="credit-card")
    purchasePayment3 = add_purchase_payment(db=db,
                                            purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                            amount=390.45,
                                            paymentMethod="cash")

    return {
        "vendor_name": purchaseTransaction["vendor_name"],
        "vendor_id": purchaseTransaction["vendor_id"],
        "purchase_transaction_id": purchaseTransaction["purchase_transaction_id"],
        "total_amount": purchasePayment1["amount"] + purchasePayment2["amount"] + purchasePayment3["amount"],
        "discount": purchaseTransaction["discount"],
        "suspended": purchaseTransaction["suspended"]
    }

def add_second_purchase_transaction(db):
    purchaseTransaction = add_purchase_transaction(db=db,
                                                    vendorName="Ororo Monroe")
    purchasePayment1 = add_purchase_payment(db=db,
                                            purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                            amount=582.45,
                                            paymentMethod="debit-card")
    purchasePayment2 = add_purchase_payment(db=db,
                                            purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                            amount=233.28,
                                            paymentMethod="credit-card")

    return {
        "vendor_name": purchaseTransaction["vendor_name"],
        "vendor_id": purchaseTransaction["vendor_id"],
        "purchase_transaction_id": purchaseTransaction["purchase_transaction_id"],
        "total_amount": purchasePayment1["amount"] + purchasePayment2["amount"],
        "discount": purchaseTransaction["discount"],
        "suspended": purchaseTransaction["suspended"]
    }

def add_third_purchase_transaction(db):
    purchaseTransaction = add_purchase_transaction(db=db,
                                                    vendorName="Jean Gray")
    purchasePayment1 = add_purchase_payment(db=db,
                                            purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                            amount=578.23,
                                            paymentMethod="debit-card")
    purchasePayment2 = add_purchase_payment(db=db,
                                            purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                            amount=694.95,
                                            paymentMethod="cash")
    purchasePayment3 = add_purchase_payment(db=db,
                                            purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                            amount=394.38,
                                            paymentMethod="cash")
    purchasePayment4 = add_purchase_payment(db=db,
                                            purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                            amount=421.57,
                                            paymentMethod="credit-card")

    return {
        "vendor_name": purchaseTransaction["vendor_name"],
        "vendor_id": purchaseTransaction["vendor_id"],
        "purchase_transaction_id": purchaseTransaction["purchase_transaction_id"],
        "total_amount": purchasePayment1["amount"] + purchasePayment2["amount"] + purchasePayment3["amount"] + purchasePayment4["amount"],
        "discount": purchaseTransaction["discount"],
        "suspended": purchaseTransaction["suspended"]
    }

def add_purchase_transaction(db, vendorName, discount=0, suspended=False):
    purchaseTransaction = {
        "vendor_id": None,
        "vendor_name": vendorName,
        "discount": discount,
        "suspended": suspended,
        "user_id": 1
    }

    purchaseTransactionTable = db.schema.get_table("purchase_transaction")
    result = purchaseTransactionTable.insert("vendor_id",
                                                "vendor_name",
                                                "discount",
                                                "suspended",
                                                "user_id") \
                                        .values(tuple(purchaseTransaction.values())) \
                                        .execute()
    purchaseTransaction.update(DatabaseResult(result).fetch_one("purchase_transaction_id"))
    return purchaseTransaction

def add_purchase_payment(db, purchaseTransactionId, amount, paymentMethod, archived=False):
    purchasePayment = {
        "purchase_transaction_id": purchaseTransactionId,
        "amount": amount,
        #"payment_method": paymentMethod,
        "currency": "NGN",
        "archived": archived,
        "user_id": 1
    }

    purchasePaymentTable = db.schema.get_table("purchase_payment")
    result = purchasePaymentTable.insert("purchase_transaction_id",
                                            "amount",
                                            #"payment_method",
                                            "currency",
                                            "archived",
                                            "user_id") \
                                    .values(tuple(purchasePayment.values())) \
                                    .execute()
    purchasePayment.update(DatabaseResult(result).fetch_one("purchase_payment_id"))
    return purchasePayment

def view_purchase_transactions(db, fromDateTime, toDateTime, suspended=None, archived=None):
    args = {
        "from": DatabaseDateTime(fromDateTime).iso_format,
        "to": DatabaseDateTime(toDateTime).iso_format,
        "suspended": suspended,
        "archived": archived
    }
    sqlResult = db.call_procedure("ViewPurchaseTransactions", tuple(args.values()))
    return DatabaseResult(sqlResult).fetch_all()

if __name__ == '__main__':
    unittest.main()