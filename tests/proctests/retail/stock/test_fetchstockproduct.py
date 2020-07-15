#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase
from datetime import datetime, date

class FetchStockProduct(StoredProcedureTestCase):
    def test_fetch_stock_product(self):
        productCategory = add_product_category(db=self.db,
                                                category="TVs")
        product = add_product(db=self.db,
                                productCategoryId=productCategory["product_category_id"],
                                product="LG",
                                description="Description")
        productUnit = add_product_unit(db=self.db,
                                        productId=product["product_id"],
                                        unit="unit(s)",
                                        costPrice=locale.currency(285.28),
                                        retailPrice=locale.currency(302.31))
        currentProductQuantity = add_current_product_quantity(db=self.db,
                                                                productId=product["product_id"],
                                                                quantity=38.825)

        fetchedStockProduct = fetch_stock_product(db=self.db,
                                                    productId=product["product_id"])
        self.assertEqual(fetchedStockProduct["product_category_id"], 
                            productCategory["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(fetchedStockProduct["product_category"], 
                            productCategory["category"],
                            "Product category mismatch.")
        self.assertEqual(fetchedStockProduct["product_id"], 
                            product["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedStockProduct["product"], 
                            product["product"],
                            "Product mismatch.")
        self.assertEqual(fetchedStockProduct["product_unit_id"], 
                            productUnit["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(fetchedStockProduct["product_unit"], 
                            productUnit["unit"],
                            "Product unit mismatch.")
        self.assertEqual(fetchedStockProduct["description"], 
                            product["description"],
                            "Description mismatch.")
        self.assertEqual(fetchedStockProduct["divisible"], 
                            product["divisible"],
                            "Divisible flag mismatch.")
        self.assertEqual(fetchedStockProduct["quantity"], 
                            currentProductQuantity["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(fetchedStockProduct["cost_price"], 
                            productUnit["cost_price"],
                            "Cost price mismatch.")
        self.assertEqual(fetchedStockProduct["retail_price"], 
                            productUnit["retail_price"],
                            "Retail price mismatch.")
        self.assertEqual(fetchedStockProduct["currency"], 
                            productUnit["currency"],
                            "Currency mismatch.")
        self.assertEqual(fetchedStockProduct["created"].date(),
                            date.today(),
                            "Created date/time mismatch.")
        self.assertEqual(fetchedStockProduct["last_edited"].date(),
                            date.today(),
                            "Last edited date/time flag mismatch.")
        self.assertEqual(fetchedStockProduct["user_id"], 
                            1,
                            "User ID mismatch.")
        self.assertEqual(fetchedStockProduct["username"], 
                            "admin",
                            "User mismatch.")

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

def add_product(db, productCategoryId, product, description, divisible=True):
    product = {
        "product_category_id": productCategoryId,
        "product": product,
        "description": description,
        "divisible": divisible,
        "user_id": 1
    }
    
    db.execute("""INSERT INTO product (product_category_id,
                                        product,
                                        description,
                                        divisible,
                                        user_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id AS product_id,
                    product_category_id,
                    product,
                    description,
                    divisible,
                    user_id""", tuple(product.values()))
    result = {}
    for row in db:
        result = {
            "product_id": row["product_id"],
            "product_category_id": row["product_category_id"],
            "product": row["product"],
            "description": row["description"],
            "divisible": row["divisible"],
            "user_id": row["user_id"]
        }
    return result

def add_product_unit(db, productId, unit, costPrice, retailPrice, baseUnitEquivalent=1, preferred=True):
    productUnit = {
        "product_id": productId,
        "unit": unit,
        "base_unit_equivalent": baseUnitEquivalent,
        "preferred": preferred,
        "cost_price": costPrice,
        "retail_price": retailPrice,
        "currency": "NGN",
        "user_id": 1
    }

    db.execute("""INSERT INTO product_unit (product_id,
                                            unit,
                                            base_unit_equivalent,
                                            preferred,
                                            cost_price,
                                            retail_price,
                                            currency,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS product_unit_id,
                    product_id,
                    unit,
                    base_unit_equivalent,
                    preferred,
                    cost_price,
                    retail_price,
                    currency,
                    user_id""", tuple(productUnit.values()))
    result = {}
    for row in db:
        result = {
            "product_unit_id": row["product_unit_id"],
            "unit": row["unit"],
            "product_id": row["product_id"],
            "base_unit_equivalent": row["base_unit_equivalent"],
            "preferred": row["preferred"],
            "cost_price": row["cost_price"],
            "retail_price": row["retail_price"],
            "currency": row["currency"],
            "user_id": row["user_id"]
        }
    return result

def add_current_product_quantity(db, productId, quantity):
    currentProductQuantity = {
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
                    user_id""", tuple(currentProductQuantity.values()))
    result = {}
    for row in db:
        result = {
            "current_product_quantity_id": row["current_product_quantity_id"],
            "product_id": row["product_id"],
            "quantity": row["quantity"],
            "user_id": row["user_id"]
        }
    return result

def fetch_stock_product(db, productId):
    db.call_procedure("FetchStockProduct", [productId])
    result = {}
    for row in db:
        result = {
            "product_id": row["product_id"],
            "product_category_id": row["product_category_id"],
            "product_category": row["product_category"],
            "product": row["product"],
            "description": row["description"],
            "divisible": row["divisible"],
            "image": row["image"],
            "quantity": row["quantity"],
            "product_unit_id": row["product_unit_id"],
            "product_unit": row["product_unit"],
            "cost_price": row["cost_price"],
            "retail_price": row["retail_price"],
            "currency": row["currency"],
            "created": row["created"],
            "last_edited": row["last_edited"],
            "user_id": row["user_id"],
            "username": row["username"],
        }
    return result

if __name__ == '__main__':
    unittest.main()
