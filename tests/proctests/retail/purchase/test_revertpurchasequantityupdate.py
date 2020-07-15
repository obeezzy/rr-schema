#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase

class RevertPurchaseQuantityUpdate(StoredProcedureTestCase):
    def test_revert_purchase_quantity_update(self):
        addedPurchaseTransaction = add_purchase_transaction(db=self.db,
                                                            vendorName="Tony Stark")
        addedProduct = add_product(db=self.db,
                                    product="Iron Man suit")
        addedProductQuantity = add_product_quantity(db=self.db,
                                                    productId=addedProduct["product_id"],
                                                    quantity=200.25)
        fetchedProductQuantity = fetch_current_product_quantity(db=self.db,
                                                                productId=addedProduct["product_id"])
        self.assertEqual(addedProductQuantity["quantity"], fetchedProductQuantity["quantity"], "Quantity mismatch.")

        addedPurchasedProduct = add_purchased_product(db=self.db,
                                                        purchaseTransactionId=addedPurchaseTransaction["purchase_transaction_id"])
        alter_product_quantity(db=self.db,
                                productId=addedProduct["product_id"],
                                newQuantity=addedProductQuantity["quantity"] + addedPurchasedProduct["quantity"])
        fetchedProductQuantity = fetch_current_product_quantity(db=self.db,
                                                                productId=addedProduct["product_id"])
        self.assertEqual(addedProductQuantity["quantity"] + addedPurchasedProduct["quantity"],
                            fetchedProductQuantity["quantity"],
                            "Quantity mismatch.")

        revert_purchase_quantity_update(db=self.db, 
                                        purchaseTransactionId=addedPurchaseTransaction["purchase_transaction_id"])

        fetchedProductQuantity = fetch_current_product_quantity(db=self.db,
                                                                productId=addedProduct["product_id"])
        self.assertEqual(addedProductQuantity["quantity"], fetchedProductQuantity["quantity"], "Quantity mismatch.")

def add_purchase_transaction(db, vendorName, suspended=False):
    purchaseTransaction = {
        "vendor_id": None,
        "vendor_name": vendorName,
        "suspended": suspended,
        "user_id": 1
    }

    db.execute("""INSERT INTO purchase_transaction (vendor_id,
                                                    vendor_name,
                                                    suspended,
                                                    user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id AS purchase_transaction_id,
                    vendor_id,
                    vendor_name,
                    suspended,
                    user_id""", tuple(purchaseTransaction.values()))
    result = {}
    for row in db:
        result = {
            "purchase_transaction_id": row["purchase_transaction_id"],
            "vendor_id": row["vendor_id"],
            "vendor_name": row["vendor_name"],
            "suspended": row["suspended"],
            "user_id": row["user_id"]
        }
    return result

def add_product(db, product):
    product = {
        "product_category_id": 1,
        "product": product,
        "user_id": 1
    }

    db.execute("""INSERT INTO product (product_category_id,
                                        product,
                                        user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS product_id,
                    product_category_id,
                    product,
                    user_id""", tuple(product.values()))
    for row in db:
        result = {
            "product_id": row["product_id"],
            "product_category_id": row["product_category_id"],
            "product": row["product"],
            "user_id": row["user_id"]
        }
    return result

def add_purchased_product(db, purchaseTransactionId):
    purchasedProduct = {
        "purchase_transaction_id": purchaseTransactionId,
        "product_id": 1,
        "product_unit_id": 1,
        "unit_price": locale.currency(1038.39),
        "quantity": 183.25,
        "cost": locale.currency(1832.28),
        "discount": locale.currency(138.23),
        "currency": "NGN",
        "user_id": 1
    }

    db.execute("""INSERT INTO purchased_product (purchase_transaction_id,
                                                    product_id,
                                                    product_unit_id,
                                                    unit_price,
                                                    quantity,
                                                    cost,
                                                    discount,
                                                    currency,
                                                    user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS purchased_product_id,
                    purchase_transaction_id,
                    product_id,
                    product_unit_id,
                    unit_price,
                    quantity,
                    cost,
                    discount,
                    currency,
                    user_id""", tuple(purchasedProduct.values()))
    result = {}
    for row in db:
        result = {
            "purchased_product_id": row["purchased_product_id"],
            "purchase_transaction_id": row["purchase_transaction_id"],
            "product_id": row["product_id"],
            "product_unit_id": row["product_unit_id"],
            "unit_price": row["unit_price"],
            "quantity": row["quantity"],
            "cost": row["cost"],
            "discount": row["discount"],
            "currency": row["currency"],
            "user_id": row["user_id"]
        }
    return result

def add_product_quantity(db, productId, quantity):
    productQuantity = {
        "product_id": productId,
        "quantity": quantity,
        "user_id": 1
    }

    db.execute("""INSERT INTO current_product_quantity (product_id,
                                                        quantity,
                                                        user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS current_product_quantity_id,
                    product_id,
                    quantity,
                    user_id""", tuple(productQuantity.values()))
    for row in db:
        result = {
            "current_product_quantity_id": row["current_product_quantity_id"],
            "product_id": row["product_id"],
            "quantity": row["quantity"],
            "user_id": row["user_id"]
        }
    return result

def alter_product_quantity(db, productId, newQuantity):
    db.execute("""UPDATE current_product_quantity
                    SET quantity = %s
                    WHERE product_id = %s""", [newQuantity, productId])

def revert_purchase_quantity_update(db, purchaseTransactionId, userId=1):
    db.call_procedure("RevertPurchaseQuantityUpdate", [purchaseTransactionId, userId])

def fetch_current_product_quantity(db, productId):
    db.execute("""SELECT product_id,
                            quantity,
                            user_id
                FROM current_product_quantity
                WHERE product_id = %s""", [productId])
    result = {}
    for row in db:
        result = {
            "product_id": row["product_id"],
            "quantity": row["quantity"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
