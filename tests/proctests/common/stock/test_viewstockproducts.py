#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase
from datetime import datetime, date

class ViewStockProducts(StoredProcedureTestCase):
    def test_view_stock_products(self):
        productCategory1 = add_product_category(db=self.db,
                                                category="Pianos")
        product1 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Yamaha",
                                description="The best",
                                divisible=False)
        productUnit1 = add_product_unit(db=self.db,
                                        productId=product1["product_id"],
                                        unit="unit(s)",
                                        costPrice=locale.currency(23.48),
                                        retailPrice=locale.currency(76.33))
        currentProductQuantity1 = add_current_product_quantity(db=self.db,
                                                                productId=product1["product_id"],
                                                                quantity=50.125)
        product2 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Casio",
                                description="I've used the cheap version.",
                                divisible=True)
        productUnit2 = add_product_unit(db=self.db,
                                        productId=product2["product_id"],
                                        unit="unit(s)",
                                        costPrice=locale.currency(23.48),
                                        retailPrice=locale.currency(76.33))
        currentProductQuantity2 = add_current_product_quantity(db=self.db,
                                                                productId=product2["product_id"],
                                                                quantity=20.25)
        productCategory2 = add_product_category(db=self.db,
                                                category="Guitars")
        product3 = add_product(db=self.db,
                                productCategoryId=productCategory2["product_category_id"],
                                product="Rowland",
                                description="Think I had these back in Covenant University.",
                                divisible=False)
        productUnit3 = add_product_unit(db=self.db,
                                        productId=product3["product_id"],
                                        unit="unit(s)",
                                        costPrice=locale.currency(23.48),
                                        retailPrice=locale.currency(76.33))
        currentProductQuantity3 = add_current_product_quantity(db=self.db,
                                                                productId=product3["product_id"],
                                                                quantity=10.625)

        fetchedProducts = view_stock_products(db=self.db,
                                                productCategoryId=productCategory1["product_category_id"],
                                                sortOrder="ascending")

        self.assertEqual(len(fetchedProducts), 2, "Expected 2 product categories.")
        self.assertEqual(fetchedProducts[0]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(fetchedProducts[0]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch.")
        self.assertEqual(fetchedProducts[0]["product_id"],
                            product2["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedProducts[0]["product"],
                            product2["product"],
                            "Product mismatch.")
        self.assertEqual(fetchedProducts[0]["description"],
                            product2["description"],
                            "Description mismatch.")
        self.assertEqual(fetchedProducts[0]["divisible"],
                            product2["divisible"],
                            "Divisible mismatch.")
        self.assertEqual(fetchedProducts[0]["quantity"],
                            currentProductQuantity2["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(fetchedProducts[0]["product_unit_id"],
                            productUnit2["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(fetchedProducts[0]["product_unit"],
                            productUnit2["unit"],
                            "Product unit mismatch.")
        self.assertEqual(fetchedProducts[0]["cost_price"],
                            productUnit2["cost_price"],
                            "Cost price mismatch.")
        self.assertEqual(fetchedProducts[0]["retail_price"],
                            productUnit2["retail_price"],
                            "Retail price mismatch.")
        self.assertEqual(fetchedProducts[0]["created"].date(),
                            date.today(),
                            "Time created mismatch.")
        self.assertEqual(fetchedProducts[0]["last_edited"].date(),
                            date.today(),
                            "Time modified mismatch.")
        self.assertEqual(fetchedProducts[0]["user_id"],
                            product2["user_id"],
                            "User ID mismatch.")

        self.assertEqual(fetchedProducts[1]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(fetchedProducts[1]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch.")
        self.assertEqual(fetchedProducts[1]["product_id"],
                            product1["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedProducts[1]["product"],
                            product1["product"],
                            "Product mismatch.")
        self.assertEqual(fetchedProducts[1]["description"],
                            product1["description"],
                            "Description mismatch.")
        self.assertEqual(fetchedProducts[1]["divisible"],
                            product1["divisible"],
                            "Divisible mismatch.")
        self.assertEqual(fetchedProducts[1]["quantity"],
                            currentProductQuantity1["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(fetchedProducts[1]["product_unit_id"],
                            productUnit1["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(fetchedProducts[1]["product_unit"],
                            productUnit1["unit"],
                            "Product unit mismatch.")
        self.assertEqual(fetchedProducts[1]["cost_price"],
                            productUnit1["cost_price"],
                            "Cost price mismatch.")
        self.assertEqual(fetchedProducts[1]["retail_price"],
                            productUnit1["retail_price"],
                            "Retail price mismatch.")
        self.assertEqual(fetchedProducts[1]["created"].date(),
                            date.today(),
                            "Time created mismatch.")
        self.assertEqual(fetchedProducts[1]["last_edited"].date(),
                            date.today(),
                            "Time modified mismatch.")
        self.assertEqual(fetchedProducts[1]["user_id"],
                            product1["user_id"],
                            "User ID mismatch.")

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

def add_product(db, productCategoryId, product, description, divisible):
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
            "product_id": row["product_id"],
            "unit": row["unit"],
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

def view_stock_products(db, productCategoryId, sortOrder=None):
    db.call_procedure("ViewStockProducts", [productCategoryId, sortOrder])
    results = []
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
            "username": row["username"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
