#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult
from datetime import datetime, timedelta

class FetchTotalRevenue(StoredProcedureTestCase):
    def test_fetch_debtor(self):
        saleTransaction1 = add_sale_transaction(db=self.db,
                                                customerName="Danny Phantom")
        salePayment1 = add_sale_payment(db=self.db,
                                        saleTransactionId=saleTransaction1["sale_transaction_id"],
                                        amount=58.21,
                                        paymentMethod="cash")
        salePayment2 = add_sale_payment(db=self.db,
                                        saleTransactionId=saleTransaction1["sale_transaction_id"],
                                        amount=77.23,
                                        paymentMethod="cash")

        saleTransaction2 = add_sale_transaction(db=self.db,
                                                customerName="Samurai Jack")
        salePayment3 = add_sale_payment(db=self.db,
                                        saleTransactionId=saleTransaction2["sale_transaction_id"],
                                        amount=82.14,
                                        paymentMethod="debit-card")

        today = datetime.date(datetime.now())
        tomorrow = datetime.date(datetime.now() + timedelta(days=1))
        fetchedTotalRevenue = fetch_total_revenue(db=self.db,
                                                    fromDate=today,
                                                    toDate=tomorrow)

        self.assertEqual(fetchedTotalRevenue["total_revenue"], 
                            round(salePayment1["amount"] + salePayment2["amount"] + salePayment3["amount"], 2),
                            "Total revenue mismatch.")


def add_sale_transaction(db, customerName):
    saleTransaction = {
        "customer_name": customerName,
        "user_id": 1
    }

    saleTransactionTable = db.schema.get_table("sale_transaction")
    result = saleTransactionTable.insert("customer_name",
                                            "user_id") \
                        .values(tuple(saleTransaction.values())) \
                        .execute()
    saleTransaction.update(DatabaseResult(result).fetch_one("sale_transaction_id"))
    return saleTransaction

def add_sale_payment(db, saleTransactionId, amount, paymentMethod):
    salePayment = {
        "sale_transaction_id": saleTransactionId,
        "amount": amount,
        #"payment_method": paymentMethod,
        "currency": "NGN",
        "user_id": 1
    }

    salePaymentTable = db.schema.get_table("sale_payment")
    result = salePaymentTable.insert("sale_transaction_id",
                                        "amount",
                                        #"payment_method",
                                        "currency",
                                        "user_id") \
                                .values(tuple(salePayment.values())) \
                                .execute()
    salePayment.update(DatabaseResult(result).fetch_one("sale_payment_id"))
    return salePayment

def add_debtor(db, client, note):
    debtor = {
        "client_id": client["client_id"],
        "note_id": note["note_id"],
        "user_id": 1
    }
    debtorTable = db.schema.get_table("debtor")
    result = debtorTable.insert("client_id",
                                "note_id",
                                "user_id") \
                            .values(tuple(debtor.values())) \
                            .execute()
    del client["client_id"]
    debtor.update(client)
    debtor.update(DatabaseResult(result).fetch_one("debtor_id"))
    debtor["note"] = note["note"]
    return debtor

def add_note(db):
    note = {
        "note": "His middle name is Gonzalo.",
        "user_id": 1
    }
    noteTable = db.schema.get_table("note")
    result = noteTable.insert("note",
                                "user_id") \
                            .values(tuple(note.values())) \
                            .execute()
    note.update(DatabaseResult(result).fetch_one("note_id"))
    return note

def fetch_total_revenue(db, fromDate, toDate, archived=False):
    sqlResult = db.call_procedure("FetchTotalRevenue", (fromDate, toDate))
    return DatabaseResult(sqlResult).fetch_one("total_revenue")

if __name__ == '__main__':
    unittest.main()