#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase
from datetime import datetime, date, timedelta
from decimal import Decimal

class FetchTotalRevenue(StoredProcedureTestCase):
    def test_fetch_total_revenue(self):
        saleTransaction1 = add_sale_transaction(db=self.db,
                                                customerName="Danny Phantom")
        salePayment1 = add_sale_payment(db=self.db,
                                        saleTransactionId=saleTransaction1["sale_transaction_id"],
                                        amount=locale.currency(58.21),
                                        paymentMethod="cash")
        salePayment2 = add_sale_payment(db=self.db,
                                        saleTransactionId=saleTransaction1["sale_transaction_id"],
                                        amount=locale.currency(77.23),
                                        paymentMethod="cash")

        saleTransaction2 = add_sale_transaction(db=self.db,
                                                customerName="Samurai Jack")
        salePayment3 = add_sale_payment(db=self.db,
                                        saleTransactionId=saleTransaction2["sale_transaction_id"],
                                        amount=locale.currency(82.14),
                                        paymentMethod="debit_card")

        today = date.today()
        tomorrow = today + timedelta(days=1)
        fetchedTotalRevenue = fetch_total_revenue(db=self.db,
                                                    fromDate=today,
                                                    toDate=tomorrow)

        self.assertEqual(fetchedTotalRevenue["total_revenue"], 
                            locale.currency(Decimal(salePayment1["amount"].strip(self.db.currency_symbol)) + Decimal(salePayment2["amount"].strip(self.db.currency_symbol)) + Decimal(salePayment3["amount"].strip(self.db.currency_symbol))),
                            "Total revenue mismatch.")


def add_sale_transaction(db, customerName):
    saleTransaction = {
        "customer_name": customerName,
        "user_id": 1
    }

    db.execute("""INSERT INTO sale_transaction (customer_name,
                                                user_id)
                VALUES (%s, %s)
                RETURNING id AS sale_transaction_id,
                    customer_name,
                    user_id""", tuple(saleTransaction.values()))
    result = {}
    for row in db:
        result = {
            "sale_transaction_id": row["sale_transaction_id"],
            "customer_name": row["customer_name"],
            "user_id": row["user_id"]
        }
    return result

def add_sale_payment(db, saleTransactionId, amount, paymentMethod):
    salePayment = {
        "sale_transaction_id": saleTransactionId,
        "amount": amount,
        "payment_method": paymentMethod,
        "currency": "NGN",
        "user_id": 1
    }

    db.execute("""INSERT INTO sale_payment (sale_transaction_id,
                                            amount,
                                            payment_method,
                                            currency,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id AS sale_payment_id,
                    sale_transaction_id,
                    amount,
                    payment_method,
                    currency,
                    user_id""", tuple(salePayment.values()))
    result = {}
    for row in db:
        result = {
            "sale_payment_id": row["sale_payment_id"],
            "sale_transaction_id": row["sale_transaction_id"],
            "amount": row["amount"],
            "payment_method": row["payment_method"],
            "currency": row["currency"],
            "user_id": row["user_id"]
        }
    return result

def fetch_total_revenue(db, fromDate, toDate, archived=False):
    db.call_procedure("FetchTotalRevenue", [fromDate, toDate])
    result = {}
    for row in db:
        result = {
            "created": row["created"],
            "total_revenue": row["total_revenue"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
