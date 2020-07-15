#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase
from datetime import datetime, date, timedelta
from decimal import Decimal

class ViewPurchaseTransactions(StoredProcedureTestCase):
    def test_view_purchase_transactions(self):
        purchaseTransaction1 = add_first_purchase_transaction(self.db)
        purchaseTransaction2 = add_second_purchase_transaction(self.db)
        purchaseTransaction3 = add_third_purchase_transaction(self.db)

        today = date.today()
        tomorrow = today + timedelta(days=1)
        viewedPurchaseTransactions = view_purchase_transactions(db=self.db,
                                                                fromDate=today,
                                                                toDate=tomorrow)

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
                                            amount=locale.currency(340.45),
                                            paymentMethod="cash")
    purchasePayment2 = add_purchase_payment(db=db,
                                            purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                            amount=locale.currency(440.45),
                                            paymentMethod="credit_card")
    purchasePayment3 = add_purchase_payment(db=db,
                                            purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                            amount=locale.currency(390.45),
                                            paymentMethod="cash")

    return {
        "vendor_name": purchaseTransaction["vendor_name"],
        "vendor_id": purchaseTransaction["vendor_id"],
        "purchase_transaction_id": purchaseTransaction["purchase_transaction_id"],
        "total_amount": locale.currency(Decimal(purchasePayment1["amount"].strip("$")) + Decimal(purchasePayment2["amount"].strip("$")) + Decimal(purchasePayment3["amount"].strip("$"))),
        "discount": purchaseTransaction["discount"],
        "suspended": purchaseTransaction["suspended"]
    }

def add_second_purchase_transaction(db):
    purchaseTransaction = add_purchase_transaction(db=db,
                                                    vendorName="Ororo Monroe")
    purchasePayment1 = add_purchase_payment(db=db,
                                            purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                            amount=locale.currency(582.45),
                                            paymentMethod="debit_card")
    purchasePayment2 = add_purchase_payment(db=db,
                                            purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                            amount=locale.currency(233.28),
                                            paymentMethod="credit_card")

    return {
        "vendor_name": purchaseTransaction["vendor_name"],
        "vendor_id": purchaseTransaction["vendor_id"],
        "purchase_transaction_id": purchaseTransaction["purchase_transaction_id"],
        "total_amount": locale.currency(Decimal(purchasePayment1["amount"].strip("$")) + Decimal(purchasePayment2["amount"].strip("$"))),
        "discount": purchaseTransaction["discount"],
        "suspended": purchaseTransaction["suspended"]
    }

def add_third_purchase_transaction(db):
    purchaseTransaction = add_purchase_transaction(db=db,
                                                    vendorName="Jean Gray")
    purchasePayment1 = add_purchase_payment(db=db,
                                            purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                            amount=locale.currency(578.23),
                                            paymentMethod="debit_card")
    purchasePayment2 = add_purchase_payment(db=db,
                                            purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                            amount=locale.currency(694.95),
                                            paymentMethod="cash")
    purchasePayment3 = add_purchase_payment(db=db,
                                            purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                            amount=locale.currency(394.38),
                                            paymentMethod="cash")
    purchasePayment4 = add_purchase_payment(db=db,
                                            purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                            amount=locale.currency(421.57),
                                            paymentMethod="credit_card")

    return {
        "vendor_name": purchaseTransaction["vendor_name"],
        "vendor_id": purchaseTransaction["vendor_id"],
        "purchase_transaction_id": purchaseTransaction["purchase_transaction_id"],
        "total_amount": locale.currency(Decimal(purchasePayment1["amount"].strip("$")) + Decimal(purchasePayment2["amount"].strip("$")) + Decimal(purchasePayment3["amount"].strip("$")) + Decimal(purchasePayment4["amount"].strip("$"))),
        "discount": purchaseTransaction["discount"],
        "suspended": purchaseTransaction["suspended"]
    }

def add_purchase_transaction(db, vendorName, discount="$0", suspended=False):
    purchaseTransaction = {
        "vendor_id": None,
        "vendor_name": vendorName,
        "discount": discount,
        "suspended": suspended,
        "user_id": 1
    }

    db.execute("""INSERT INTO purchase_transaction (vendor_id,
                                                    vendor_name,
                                                    discount,
                                                    suspended,
                                                    user_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id AS purchase_transaction_id,
                    vendor_id,
                    vendor_name,
                    discount,
                    suspended,
                    user_id""", tuple(purchaseTransaction.values()))
    result = {}
    for row in db:
        result = {
            "purchase_transaction_id": row["purchase_transaction_id"],
            "vendor_id": row["vendor_id"],
            "vendor_name": row["vendor_name"],
            "discount": row["discount"],
            "suspended": row["suspended"],
            "user_id": row["user_id"]
        }
    return result

def add_purchase_payment(db, purchaseTransactionId, amount, paymentMethod, archived=False):
    purchasePayment = {
        "purchase_transaction_id": purchaseTransactionId,
        "amount": amount,
        "payment_method": paymentMethod,
        "currency": "NGN",
        "archived": archived,
        "user_id": 1
    }

    db.execute("""INSERT INTO purchase_payment (purchase_transaction_id,
                                                amount,
                                                payment_method,
                                                currency,
                                                archived,
                                                user_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id AS purchase_payment_id,
                        purchase_transaction_id,
                        amount,
                        payment_method,
                        currency,
                        archived,
                        user_id""", tuple(purchasePayment.values()))
    result = {}
    for row in db:
        result = {
            "purchase_payment_id": row["purchase_payment_id"],
            "purchase_transaction_id": row["purchase_transaction_id"],
            "amount": row["amount"],
            "payment_method": row["payment_method"],
            "currency": row["currency"],
            "archived": row["archived"],
            "user_id": row["user_id"]
        }
    return result

def view_purchase_transactions(db, fromDate, toDate, suspended=False, archived=False):
    db.call_procedure("ViewPurchaseTransactions", [fromDate, toDate, suspended, archived])
    results = []
    for row in db:
        result = {
            "purchase_transaction_id": row["purchase_transaction_id"],
            "vendor_name": row["vendor_name"],
            "vendor_id": row["vendor_id"],
            "discount": row["discount"].replace(",", ""),
            "suspended": row["suspended"],
            "note_id": row["note_id"],
            "total_amount": row["total_amount"].replace(",", ""),
            "note": row["note"],
            "archived": row["archived"],
            "created": row["created"],
            "last_edited": row["last_edited"],
            "user_id": row["user_id"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
