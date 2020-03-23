#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime, date, timedelta

class ViewSaleTransactions(StoredProcedureTestCase):
    def test_view_sale_transactions(self):
        saleTransaction1 = add_first_sale_transaction(self.db)
        saleTransaction2 = add_second_sale_transaction(self.db)
        saleTransaction3 = add_third_sale_transaction(self.db)

        today = date.today()
        tomorrow = today + timedelta(days=1)
        viewedSaleTransactions = view_sale_transactions(db=self.db,
                                                                fromDate=today,
                                                                toDate=tomorrow)

        self.assertEqual(len(viewedSaleTransactions), 3, "Expected 3 transactions.")
        self.assertEqual(viewedSaleTransactions[0]["sale_transaction_id"],
                            saleTransaction1["sale_transaction_id"],
                            "Sale transaction ID mismatch.")
        self.assertEqual(viewedSaleTransactions[0]["customer_name"],
                            saleTransaction1["customer_name"],
                            "Customer name mismatch.")
        self.assertEqual(viewedSaleTransactions[0]["customer_id"],
                            saleTransaction1["customer_id"],
                            "Customer ID mismatch.")
        self.assertEqual(viewedSaleTransactions[0]["discount"],
                            saleTransaction1["discount"],
                            "Discount mismatch.")
        self.assertEqual(viewedSaleTransactions[0]["suspended"],
                            saleTransaction1["suspended"],
                            "Suspended flag mismatch.")
        self.assertEqual(viewedSaleTransactions[0]["total_amount"],
                            saleTransaction1["total_amount"],
                            "Total amount mismatch.")

        self.assertEqual(viewedSaleTransactions[1]["sale_transaction_id"],
                            saleTransaction2["sale_transaction_id"],
                            "Sale transaction ID mismatch.")
        self.assertEqual(viewedSaleTransactions[1]["customer_name"],
                            saleTransaction2["customer_name"],
                            "Customer name mismatch.")
        self.assertEqual(viewedSaleTransactions[1]["customer_id"],
                            saleTransaction2["customer_id"],
                            "Customer ID mismatch.")
        self.assertEqual(viewedSaleTransactions[1]["discount"],
                            saleTransaction2["discount"],
                            "Discount mismatch.")
        self.assertEqual(viewedSaleTransactions[1]["suspended"],
                            saleTransaction2["suspended"],
                            "Suspended flag mismatch.")
        self.assertEqual(viewedSaleTransactions[1]["total_amount"],
                            saleTransaction2["total_amount"],
                            "Total amount mismatch.")

        self.assertEqual(viewedSaleTransactions[2]["sale_transaction_id"],
                            saleTransaction3["sale_transaction_id"],
                            "Sale transaction ID mismatch.")
        self.assertEqual(viewedSaleTransactions[2]["customer_name"],
                            saleTransaction3["customer_name"],
                            "Customer name mismatch.")
        self.assertEqual(viewedSaleTransactions[2]["customer_id"],
                            saleTransaction3["customer_id"],
                            "Customer ID mismatch.")
        self.assertEqual(viewedSaleTransactions[2]["discount"],
                            saleTransaction3["discount"],
                            "Discount mismatch.")
        self.assertEqual(viewedSaleTransactions[2]["suspended"],
                            saleTransaction3["suspended"],
                            "Suspended flag mismatch.")
        self.assertEqual(viewedSaleTransactions[2]["total_amount"],
                            saleTransaction3["total_amount"],
                            "Total amount mismatch.")

def add_first_sale_transaction(db):
    saleTransaction = add_sale_transaction(db=db,
                                            customerName="Miles Morales")
    salePayment1 = add_sale_payment(db=db,
                                        saleTransactionId=saleTransaction["sale_transaction_id"],
                                        amount=340.45,
                                        paymentMethod="cash")
    salePayment2 = add_sale_payment(db=db,
                                        saleTransactionId=saleTransaction["sale_transaction_id"],
                                        amount=440.45,
                                        paymentMethod="credit-card")
    salePayment3 = add_sale_payment(db=db,
                                        saleTransactionId=saleTransaction["sale_transaction_id"],
                                        amount=390.45,
                                        paymentMethod="cash")

    return {
        "customer_name": saleTransaction["customer_name"],
        "customer_id": saleTransaction["customer_id"],
        "sale_transaction_id": saleTransaction["sale_transaction_id"],
        "total_amount": salePayment1["amount"] + salePayment2["amount"] + salePayment3["amount"],
        "discount": saleTransaction["discount"],
        "suspended": saleTransaction["suspended"]
    }

def add_second_sale_transaction(db):
    saleTransaction = add_sale_transaction(db=db,
                                            customerName="Ororo Monroe")
    salePayment1 = add_sale_payment(db=db,
                                        saleTransactionId=saleTransaction["sale_transaction_id"],
                                        amount=582.45,
                                        paymentMethod="debit-card")
    salePayment2 = add_sale_payment(db=db,
                                        saleTransactionId=saleTransaction["sale_transaction_id"],
                                        amount=233.28,
                                        paymentMethod="credit-card")

    return {
        "customer_name": saleTransaction["customer_name"],
        "customer_id": saleTransaction["customer_id"],
        "sale_transaction_id": saleTransaction["sale_transaction_id"],
        "total_amount": salePayment1["amount"] + salePayment2["amount"],
        "discount": saleTransaction["discount"],
        "suspended": saleTransaction["suspended"]
    }

def add_third_sale_transaction(db):
    saleTransaction = add_sale_transaction(db=db,
                                            customerName="Jean Gray")
    salePayment1 = add_sale_payment(db=db,
                                        saleTransactionId=saleTransaction["sale_transaction_id"],
                                        amount=578.23,
                                        paymentMethod="debit-card")
    salePayment2 = add_sale_payment(db=db,
                                        saleTransactionId=saleTransaction["sale_transaction_id"],
                                        amount=694.95,
                                        paymentMethod="cash")
    salePayment3 = add_sale_payment(db=db,
                                        saleTransactionId=saleTransaction["sale_transaction_id"],
                                        amount=394.38,
                                        paymentMethod="cash")
    salePayment4 = add_sale_payment(db=db,
                                        saleTransactionId=saleTransaction["sale_transaction_id"],
                                        amount=421.57,
                                        paymentMethod="credit-card")

    return {
        "customer_name": saleTransaction["customer_name"],
        "customer_id": saleTransaction["customer_id"],
        "sale_transaction_id": saleTransaction["sale_transaction_id"],
        "total_amount": salePayment1["amount"] + salePayment2["amount"] + salePayment3["amount"] + salePayment4["amount"],
        "discount": saleTransaction["discount"],
        "suspended": saleTransaction["suspended"]
    }

def add_sale_transaction(db, customerName, discount=0, suspended=False):
    saleTransaction = {
        "customer_id": None,
        "customer_name": customerName,
        "discount": discount,
        "suspended": suspended,
        "user_id": 1
    }

    saleTransactionTable = db.schema.get_table("sale_transaction")
    result = saleTransactionTable.insert("customer_id",
                                                "customer_name",
                                                "discount",
                                                "suspended",
                                                "user_id") \
                                    .values(tuple(saleTransaction.values())) \
                                    .execute()
    saleTransaction.update(DatabaseResult(result).fetch_one("sale_transaction_id"))
    return saleTransaction

def add_sale_payment(db, saleTransactionId, amount, paymentMethod, archived=False):
    salePayment = {
        "sale_transaction_id": saleTransactionId,
        "amount": amount,
        #"payment_method": paymentMethod,
        "currency": "NGN",
        "archived": archived,
        "user_id": 1
    }

    salePaymentTable = db.schema.get_table("sale_payment")
    result = salePaymentTable.insert("sale_transaction_id",
                                            "amount",
                                            #"payment_method",
                                            "currency",
                                            "archived",
                                            "user_id") \
                                    .values(tuple(salePayment.values())) \
                                    .execute()
    salePayment.update(DatabaseResult(result).fetch_one("sale_payment_id"))
    return salePayment

def view_sale_transactions(db, fromDate, toDate, suspended=None, archived=None):
    sqlResult = db.call_procedure("ViewSaleTransactions", (
                                    fromDate,
                                    toDate,
                                    suspended,
                                    archived))
    return DatabaseResult(sqlResult).fetch_all()

if __name__ == '__main__':
    unittest.main()