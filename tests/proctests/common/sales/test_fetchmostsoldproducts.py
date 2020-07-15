#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase
from datetime import datetime, date, timedelta
from decimal import Decimal

class FetchMostSoldProducts(StoredProcedureTestCase):
    def test_fetch_most_sold_products(self):
        productCategory1 = add_product_category(db=self.db,
                                                category="TVs")
        product1 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="LG")
        productUnit1 = add_product_unit(db=self.db,
                                        productId=product1["product_id"],
                                        unit="unit(s)",
                                        costPrice=locale.currency(285.28),
                                        retailPrice=locale.currency(302.31))

        product2 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Samsung")
        productUnit2 = add_product_unit(db=self.db,
                                        productId=product2["product_id"],
                                        unit="unit(s)",
                                        costPrice=locale.currency(543.28),
                                        retailPrice=locale.currency(602.31))

        productCategory2 = add_product_category(db=self.db,
                                                category="Computers")
        product3 = add_product(db=self.db,
                                productCategoryId=productCategory2["product_category_id"],
                                product="Dell")
        productUnit3 = add_product_unit(db=self.db,
                                        productId=product3["product_id"],
                                        unit="unit(s)",
                                        costPrice=locale.currency(285.28),
                                        retailPrice=locale.currency(302.31))

        saleTransaction = add_sale_transaction(db=self.db,
                                                customerName="Philip DeFranco")
        soldProduct1 = add_sold_product(db=self.db,
                                        saleTransactionId=saleTransaction["sale_transaction_id"],
                                        productId=product1["product_id"],
                                        unitPrice=locale.currency(51.22),
                                        quantity=1000.75,
                                        productUnitId=productUnit1["product_unit_id"],
                                        cost=locale.currency(73.32))
        soldProduct2 = add_sold_product(db=self.db,
                                        saleTransactionId=saleTransaction["sale_transaction_id"],
                                        productId=product2["product_id"],
                                        unitPrice=locale.currency(38.22),
                                        quantity=900.75,
                                        productUnitId=productUnit2["product_unit_id"],
                                        cost=locale.currency(89.88))
        soldProduct3 = add_sold_product(db=self.db,
                                        saleTransactionId=saleTransaction["sale_transaction_id"],
                                        productId=product3["product_id"],
                                        unitPrice=locale.currency(76.22),
                                        quantity=700.75,
                                        productUnitId=productUnit3["product_unit_id"],
                                        cost=locale.currency(77.32))

        today = date.today()
        tomorrow = today + timedelta(days=1)
        fetchedMostSoldProducts = fetch_most_sold_products(db=self.db,
                                                            fromDate=today,
                                                            toDate=tomorrow,
                                                            limit=5)
        self.assertEqual(len(fetchedMostSoldProducts), 3, "Expected 3 products.")
        self.assertEqual(fetchedMostSoldProducts[0]["product_category_id"], 
                            productCategory1["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(fetchedMostSoldProducts[0]["product_category"], 
                            productCategory1["category"],
                            "Product category mismatch.")
        self.assertEqual(fetchedMostSoldProducts[0]["product_id"], 
                            product1["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedMostSoldProducts[0]["product"], 
                            product1["product"],
                            "Product mismatch.")
        self.assertEqual(fetchedMostSoldProducts[0]["product_unit_id"], 
                            productUnit1["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(fetchedMostSoldProducts[0]["product_unit"], 
                            productUnit1["unit"],
                            "Product unit mismatch.")
        self.assertEqual(fetchedMostSoldProducts[0]["total_revenue"], 
                            locale.currency(Decimal(soldProduct1["cost"].strip(self.db.currency_symbol)) - Decimal(soldProduct1["discount"].strip(self.db.currency_symbol))),
                            "Total revenue mismatch.")
        self.assertEqual(fetchedMostSoldProducts[0]["total_quantity"], 
                            soldProduct1["quantity"],
                            "Total quantity mismatch.")

        self.assertEqual(fetchedMostSoldProducts[1]["product_category_id"], 
                            productCategory1["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(fetchedMostSoldProducts[1]["product_category"], 
                            productCategory1["category"],
                            "Product category mismatch.")
        self.assertEqual(fetchedMostSoldProducts[1]["product_id"], 
                            product2["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedMostSoldProducts[1]["product"], 
                            product2["product"],
                            "Product mismatch.")
        self.assertEqual(fetchedMostSoldProducts[1]["product_unit_id"], 
                            productUnit2["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(fetchedMostSoldProducts[1]["product_unit"], 
                            productUnit2["unit"],
                            "Product unit mismatch.")
        self.assertEqual(fetchedMostSoldProducts[1]["total_revenue"], 
                            locale.currency(Decimal(soldProduct2["cost"].strip(self.db.currency_symbol)) - Decimal(soldProduct2["discount"].strip(self.db.currency_symbol))),
                            "Total revenue mismatch.")
        self.assertEqual(fetchedMostSoldProducts[1]["total_quantity"], 
                            soldProduct2["quantity"],
                            "Total quantity mismatch.")

        self.assertEqual(fetchedMostSoldProducts[2]["product_category_id"], 
                            productCategory2["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(fetchedMostSoldProducts[2]["product_category"], 
                            productCategory2["category"],
                            "Product category mismatch.")
        self.assertEqual(fetchedMostSoldProducts[2]["product_id"], 
                            product3["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedMostSoldProducts[2]["product"], 
                            product3["product"],
                            "Product mismatch.")
        self.assertEqual(fetchedMostSoldProducts[2]["product_unit_id"], 
                            productUnit3["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(fetchedMostSoldProducts[2]["product_unit"], 
                            productUnit3["unit"],
                            "Product unit mismatch.")
        self.assertEqual(fetchedMostSoldProducts[2]["total_revenue"], 
                            locale.currency(Decimal(soldProduct3["cost"].strip(self.db.currency_symbol)) - Decimal(soldProduct3["discount"].strip(self.db.currency_symbol))),
                            "Total revenue mismatch.")
        self.assertEqual(fetchedMostSoldProducts[2]["total_quantity"], 
                            soldProduct3["quantity"],
                            "Total quantity mismatch.")

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
                    product,
                    user_id""", tuple(product.values()))
    result = {}
    for row in db:
        result = {
            "product_id": row["product_id"],
            "product": row["product"],
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

def add_sale_transaction(db, customerName):
    saleTransaction = {
        "customer_id": None,
        "customer_name": customerName,
        "user_id": 1
    }

    db.execute("""INSERT INTO sale_transaction (customer_id,
                                                customer_name,
                                                user_id)
                VALUES (%s, %s, %s)
                RETURNING id AS sale_transaction_id,
                    customer_id,
                    customer_name,
                    user_id""", tuple(saleTransaction.values()))
    result = {}
    for row in db:
        result = {
            "sale_transaction_id": row["sale_transaction_id"],
            "customer_id": row["customer_id"],
            "customer_name": row["customer_name"],
            "user_id": row["user_id"]
        }
    return result

def add_sold_product(db, saleTransactionId, productId, productUnitId, unitPrice, quantity, cost, discount=0):
    soldProduct = {
        "sale_transaction_id": saleTransactionId,
        "product_id": productId,
        "product_unit_id": productUnitId,
        "unit_price": unitPrice,
        "quantity": quantity,
        "cost": cost,
        "discount": discount,
        "currency": "NGN",
        "user_id": 1
    }

    db.execute("""INSERT INTO sold_product (sale_transaction_id,
                                            product_id,
                                            product_unit_id,
                                            unit_price,
                                            quantity,
                                            cost,
                                            discount,
                                            currency,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS sold_product_id,
                    sale_transaction_id,
                    product_id,
                    product_unit_id,
                    unit_price,
                    quantity,
                    cost,
                    discount,
                    currency,
                    user_id""", tuple(soldProduct.values()))
    result = {}
    for row in db:
        result = {
            "sold_product_id": row["sold_product_id"],
            "sale_transaction_id": row["sale_transaction_id"],
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

def fetch_most_sold_products(db, fromDate, toDate, limit=0):
    db.call_procedure("FetchMostSoldProducts", [fromDate, toDate, limit])
    results = []
    for row in db:
        result = {
            "product_category_id": row["product_category_id"],
            "product_category": row["product_category"],
            "product_id": row["product_id"],
            "product": row["product"],
            "product_unit_id": row["product_unit_id"],
            "product_unit": row["product_unit"],
            "total_revenue": row["total_revenue"],
            "total_quantity": row["total_quantity"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
