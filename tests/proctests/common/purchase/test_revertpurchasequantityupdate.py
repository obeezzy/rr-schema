#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

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

    purchaseTransactionTable = db.schema.get_table("purchase_transaction")
    result = purchaseTransactionTable.insert("vendor_id",
                                                "vendor_name",
                                                "suspended",
                                                "user_id") \
                                        .values(tuple(purchaseTransaction.values())) \
                                        .execute()
    purchaseTransaction.update(DatabaseResult(result).fetch_one("purchase_transaction_id"))
    return purchaseTransaction

def add_product(db, product):
    productDict = {
        "product_category_id": 1,
        "product": product,
        "user_id": 1
    }
    productTable = db.schema.get_table("product")
    result = productTable.insert("product_category_id",
                                    "product",
                                    "user_id") \
                                .values(tuple(productDict.values())) \
                                .execute()
    productDict.update(DatabaseResult(result).fetch_one("product_id"))
    return productDict

def add_purchased_product(db, purchaseTransactionId):
    purchasedProduct = {
        "purchase_transaction_id": purchaseTransactionId,
        "product_id": 1,
        "product_unit_id": 1,
        "unit_price": 1038.39,
        "quantity": 183.25,
        "cost": 1832.28,
        "discount": 138.23,
        "currency": "NGN",
        "user_id": 1
    }

    purchasedProductTable = db.schema.get_table("purchased_product")
    result = purchasedProductTable.insert("purchase_transaction_id",
                                            "product_id",
                                            "product_unit_id",
                                            "unit_price",
                                            "quantity",
                                            "cost",
                                            "discount",
                                            "currency",
                                            "user_id") \
                                    .values(tuple(purchasedProduct.values())) \
                                    .execute()
    purchasedProduct.update(DatabaseResult(result).fetch_one("purchased_product_id"))
    return purchasedProduct

def add_product_quantity(db, productId, quantity):
    productQuantity = {
        "product_id": productId,
        "quantity": quantity,
        "user_id": 1
    }

    currentProductQuantityTable = db.schema.get_table("current_product_quantity")
    result = currentProductQuantityTable.insert("product_id",
                                                "quantity",
                                                "user_id") \
                                .values(tuple(productQuantity.values())) \
                                .execute()
    productQuantity.update(DatabaseResult(result).fetch_one("current_product_quantity_id"))
    return productQuantity

def alter_product_quantity(db, productId, newQuantity):
    currentProductQuantityTable = db.schema.get_table("current_product_quantity")
    result = currentProductQuantityTable.update() \
                                .set("quantity", newQuantity) \
                                .where("product_id = :productId") \
                                .bind("productId", productId) \
                                .execute()

def revert_purchase_quantity_update(db, purchaseTransactionId, userId=1):
    sqlResult = db.call_procedure("RevertPurchaseQuantityUpdate", (purchaseTransactionId, userId))
    return bool(DatabaseResult(sqlResult).fetch_one())

def fetch_current_product_quantity(db, productId):
    currentProductQuantityTable = db.schema.get_table("current_product_quantity")
    rowResult = currentProductQuantityTable.select("product_id AS product_id",
                                                    "quantity AS quantity",
                                                    "user_id AS user_id") \
                                            .where("product_id = :productId") \
                                            .bind("productId", productId) \
                                            .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()