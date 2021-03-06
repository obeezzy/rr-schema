#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class DeductProductQuantity(StoredProcedureTestCase):
    def test_deduct_product_quantity(self):
        productCategory = add_product_category(db=self.db,
                                                category="Some category")
        product = add_product(db=self.db,
                                productCategoryId=productCategory["product_category_id"],
                                product="Some product")
        productUnit = add_product_unit(db=self.db,
                                        productId=product["product_id"],
                                        unit="G-Unit",
                                        costPrice=832.38,
                                        retailPrice=943.28)
        productQuantity = add_product_quantity(db=self.db,
                                                productId=product["product_id"],
                                                quantity=200.5)
        newQuantity = 200.125
        newProductQuantity = deduct_product_quantity(db=self.db,
                                                        productId=product["product_id"],
                                                        quantity=newQuantity,
                                                        reason="sale_transaction")
        fetchedProductQuantitySnapshot = fetch_product_quantity_snapshot(db=self.db, productId=product["product_id"])
        fetchedProductQuantity = fetch_product_quantity(db=self.db, productId=product["product_id"])

        self.assertGreater(len(fetchedProductQuantitySnapshot), 0, "Expected 1 row.")
        self.assertGreater(len(fetchedProductQuantity), 0, "Expected 1 row.")
        self.assertEqual(fetchedProductQuantity["quantity"],
                            productQuantity["quantity"] - newQuantity,
                            "Quantity mismatch.")
        self.assertEqual(fetchedProductQuantity["quantity"],
                            newProductQuantity,
                            "New quantity mismatch.")
        self.assertEqual(fetchedProductQuantitySnapshot["quantity"],
                            productQuantity["quantity"],
                            "Snapshot quatity mismatch.")

def add_product_category(db, category):
    productCategory = {
        "category": category,
        "user_id": 1
    }

    db.execute("""INSERT INTO product_category (category,
                                                user_id)
                VALUES (%s, %s)
                RETURNING id AS product_category_id,
                    category,
                    user_id""", tuple(productCategory.values()))
    result = {}
    for row in db:
        result = {
            "product_category_id": row["product_category_id"],
            "category": row["category"],
            "user_id": row["user_id"]
        }
    return result

def add_product(db, productCategoryId, product):
    product = {
        "product_category_id": productCategoryId,
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
    result = {}
    for row in db:
        result = {
            "product_id": row["product_id"],
            "product_category_id": row["product_category_id"],
            "product": row["product"],
            "user_id": row["user_id"]
        }
    return result

def add_product_unit(db, productId, unit, costPrice, retailPrice, baseUnitEquivalent=1, preferred=True):
    productUnit = {
        "product_id": productId,
        "unit": unit,
        "cost_price": costPrice,
        "retailPrice": retailPrice,
        "base_unit_equivalent": baseUnitEquivalent,
        "preferred": preferred,
        "currency": "NGN",
        "user_id": 1
    }

    db.execute("""INSERT INTO product_unit (product_id,
                                            unit,
                                            cost_price,
                                            retail_price,
                                            base_unit_equivalent,
                                            preferred,
                                            currency,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS product_unit_id,
                    product_id,
                    unit,
                    cost_price,
                    retail_price,
                    base_unit_equivalent,
                    preferred,
                    currency,
                    user_id""", tuple(productUnit.values()))
    result = {}
    for row in db:
        result = {
            "product_unit_id": row["product_unit_id"],
            "product_id": row["product_id"],
            "unit": row["unit"],
            "cost_price": row["cost_price"],
            "retail_price": row["retail_price"],
            "base_unit_equivalent": row["base_unit_equivalent"],
            "preferred": row["preferred"],
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

    db.execute("""INSERT INTO product_quantity (product_id,
                                                quantity,
                                                user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS product_quantity_id,
                    product_id,
                    quantity,
                    user_id""", tuple(productQuantity.values()))
    result = {}
    for row in db:
        result = {
            "product_quantity_id": row["product_quantity_id"],
            "product_id": row["product_id"],
            "quantity": row["quantity"],
            "user_id": row["user_id"]
        }
    return result

def deduct_product_quantity(db, productId, quantity, reason, userId=1):
    db.call_procedure("DeductProductQuantity", [productId, quantity, reason, userId])
    result = 0
    for row in db:
        result = row["new_quantity"]
    return result

def fetch_product_quantity_snapshot(db, productId):
    db.execute("""SELECT id AS product_quantity_snapshot_id,
                            product_id,
                            quantity,
                            user_id
                FROM product_quantity_snapshot
                WHERE product_id = %s""", [productId])
    result = {}
    for row in db:
        result = {
            "product_quantity_snapshot_id": row["product_quantity_snapshot_id"],
            "product_id": row["product_id"],
            "quantity": row["quantity"],
            "user_id": row["user_id"]
        }
    return result

def fetch_product_quantity(db, productId):
    db.execute("""SELECT id AS product_quantity_id,
                            product_id,
                            quantity,
                            user_id
                FROM product_quantity
                WHERE product_id = %s""", [productId])
    result = {}
    for row in db:
        result = {
            "product_quantity_id": row["product_quantity_id"],
            "product_id": row["product_id"],
            "quantity": row["quantity"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
