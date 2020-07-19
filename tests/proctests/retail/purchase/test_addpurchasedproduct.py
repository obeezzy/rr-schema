#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from decimal import Decimal

class AddPurchasedProduct(StoredProcedureTestCase):
    def test_add_purchased_product(self):
        productCategory = add_product_category(self.db)
        product = add_product(self.db, productCategoryId=productCategory["product_category_id"])
        productUnit = add_product_unit(self.db, productId=product["product_id"])
        purchaseTransaction = add_purchase_transaction(self.db)
        addedPurchasedProduct = add_purchased_product(self.db,
                                                        purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                                        productId=product["product_id"],
                                                        productUnitId=productUnit["product_unit_id"])
        fetchedPurchasedProduct = fetch_purchased_product(self.db)

        self.assertEqual(addedPurchasedProduct["purchased_product_id"],
                            fetchedPurchasedProduct["purchased_product_id"],
                            "Purchased product ID mismatch.")
        self.assertEqual(addedPurchasedProduct["purchase_transaction_id"],
                            fetchedPurchasedProduct["purchase_transaction_id"],
                            "Purchase transaction ID mismatch.")
        self.assertEqual(addedPurchasedProduct["product_id"],
                            fetchedPurchasedProduct["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(addedPurchasedProduct["product_unit_id"],
                            fetchedPurchasedProduct["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(addedPurchasedProduct["unit_price"],
                            fetchedPurchasedProduct["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(addedPurchasedProduct["quantity"],
                            fetchedPurchasedProduct["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(addedPurchasedProduct["cost"],
                            fetchedPurchasedProduct["cost"],
                            "Cost mismatch.")
        self.assertEqual(addedPurchasedProduct["discount"],
                            fetchedPurchasedProduct["discount"],
                            "Discount mismatch.")
        self.assertEqual(addedPurchasedProduct["currency"],
                            fetchedPurchasedProduct["currency"],
                            "Currency mismatch.")
        self.assertEqual(addedPurchasedProduct["user_id"],
                            fetchedPurchasedProduct["user_id"],
                            "User ID mismatch.")

def add_product_category(db):
    productCategory = {
        "category": "Category",
        "user_id": 1
    }

    db.execute("""INSERT INTO product_category (category,
                                                user_id)
                VALUES (%s, %s)
                RETURNING id AS product_category_id""", tuple(productCategory.values()))
    result = {}
    for row in db:
        result = {
            "product_category_id": row["product_category_id"]
        }
    result.update(productCategory)
    return result

def add_product(db, productCategoryId):
    product = {
        "product_category_id": productCategoryId,
        "product": "Product",
        "user_id": 1
    }

    db.execute("""INSERT INTO product (product_category_id,
                                        product,
                                        user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS product_id""", tuple(product.values()))
    result = {}
    for row in db:
        result = {
            "product_id": row["product_id"]
        }
    result.update(product)
    return result

def add_product_unit(db, productId):
    productUnit = {
        "product_id": productId,
        "unit": "unit",
        "base_unit_equivalent": 1,
        "cost_price": Decimal("200.00"),
        "retail_price": Decimal("420.00"),
        "currency": "NGN",
        "user_id": 1
    }

    db.execute("""INSERT INTO product_unit (product_id,
                                            unit,
                                            base_unit_equivalent,
                                            cost_price,
                                            retail_price,
                                            currency,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS product_unit_id""", tuple(productUnit.values()))
    result = {}
    for row in db:
        result = {
            "product_unit_id": row["product_unit_id"]
        }
    result.update(productUnit)
    return result

def add_purchase_transaction(db):
    purchaseTransaction = {
        "vendor_name": "Vendor",
        "user_id": 1
    }

    db.execute("""INSERT INTO purchase_transaction (vendor_name,
                                                    user_id)
                VALUES (%s, %s)
                RETURNING id AS purchase_transaction_id""", tuple(purchaseTransaction.values()))
    result = {}
    for row in db:
        result = {
            "purchase_transaction_id": row["purchase_transaction_id"]
        }
    result.update(purchaseTransaction)
    return result

def add_purchased_product(db, purchaseTransactionId, productId, productUnitId):
    purchasedProduct = {
        "purchase_transaction_id": purchaseTransactionId,
        "product_id": productId,
        "product_unit_id": productUnitId,
        "quantity": Decimal("183.25"),
        "unit_price": Decimal("1038.39"),
        "cost": Decimal("1832.28"),
        "discount": Decimal("138.23"),
        "currency": "NGN",
        "user_id": 1
    }

    db.call_procedure("AddPurchasedProduct",
                        tuple(purchasedProduct.values()))
    result = {}
    for row in db:
        result = {
            "purchased_product_id": row[0]
        }
    result.update(purchasedProduct)
    return result

def fetch_purchased_product(db):
    db.execute("""SELECT id AS purchased_product_id,
                            purchase_transaction_id,
                            product_id,
                            product_unit_id,
                            quantity,
                            unit_price,
                            cost,
                            discount,
                            currency,
                            user_id
                FROM purchased_product""")
    result = {}
    for row in db:
        result = {
            "purchased_product_id": row["purchased_product_id"],
            "purchase_transaction_id": row["purchase_transaction_id"],
            "product_id": row["product_id"],
            "product_unit_id": row["product_unit_id"],
            "quantity": row["quantity"],
            "unit_price": row["unit_price"],
            "cost": row["cost"],
            "discount": row["discount"],
            "currency": row["currency"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
