#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase

class FilterStockProducts(StoredProcedureTestCase):
    @unittest.skip("Needs to be refactored.")
    def test_filter_stock_products(self):
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
                                        costPrice=23.48,
                                        retailPrice=76.33)
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

        filteredProducts = filter_stock_products(db=self.db,
                                                    filterText="row",
                                                    sortOrder="ascending",
                                                    productCategoryId=productCategory2["product_category_id"])
                                                

        self.assertEqual(len(filteredProducts), 1, "Expected 1 product.")
        self.assertEqual(filteredProducts[0]["product_category_id"],
                            productCategory2["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(filteredProducts[0]["product_category"],
                            productCategory2["category"],
                            "Product category mismatch.")
        self.assertEqual(filteredProducts[0]["product_id"],
                            product3["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(filteredProducts[0]["product"],
                            product3["product"],
                            "Product mismatch.")
        self.assertEqual(filteredProducts[0]["description"],
                            product3["description"],
                            "Description mismatch.")
        self.assertEqual(filteredProducts[0]["divisible"],
                            product3["divisible"],
                            "Divisible mismatch.")
        self.assertEqual(filteredProducts[0]["quantity"],
                            currentProductQuantity3["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(filteredProducts[0]["product_unit_id"],
                            productUnit3["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(filteredProducts[0]["product_unit"],
                            productUnit3["unit"],
                            "Product unit mismatch.")
        self.assertEqual(filteredProducts[0]["cost_price"],
                            productUnit3["cost_price"],
                            "Cost price mismatch.")
        self.assertEqual(filteredProducts[0]["retail_price"],
                            productUnit3["retail_price"],
                            "Retail price mismatch.")
        self.assertEqual(filteredProducts[0]["user_id"],
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
            "user_id": row["user_id"],
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
                    product,
                    description,
                    divisible,
                    user_id""", tuple(product.values()))
    result = {}
    for row in db:
        result = {
            "product_id": row["product_id"],
            "product": row["product"],
            "description": row["description"],
            "divisible": row["divisible"],
            "user_id": row["user_id"],
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
            "user_id": row["user_id"],
        }
    return result

def filter_stock_products(db, filterText, sortOrder, productCategoryId):
    db.call_procedure("FilterStockProducts", [filterText, sortOrder, productCategoryId])
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
            "created": row["currency"],
            "last_edited": row["currency"],
            "user_id": row["user_id"],
            "username": row["username"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
