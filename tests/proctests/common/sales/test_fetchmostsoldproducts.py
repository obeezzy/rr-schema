#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult
from datetime import datetime, date, timedelta

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
                                        costPrice=285.28,
                                        retailPrice=302.31)

        product2 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Samsung")
        productUnit2 = add_product_unit(db=self.db,
                                        productId=product2["product_id"],
                                        unit="unit(s)",
                                        costPrice=543.28,
                                        retailPrice=602.31)

        productCategory2 = add_product_category(db=self.db,
                                                category="Computers")
        product3 = add_product(db=self.db,
                                productCategoryId=productCategory2["product_category_id"],
                                product="Dell")
        productUnit3 = add_product_unit(db=self.db,
                                        productId=product3["product_id"],
                                        unit="unit(s)",
                                        costPrice=285.28,
                                        retailPrice=302.31)

        saleTransaction = add_sale_transaction(db=self.db,
                                                customerName="Philip DeFranco")
        soldProduct1 = add_sold_product(db=self.db,
                                        saleTransactionId=saleTransaction["sale_transaction_id"],
                                        productId=product1["product_id"],
                                        unitPrice=51.22,
                                        quantity=1000.75,
                                        productUnitId=productUnit1["product_unit_id"],
                                        cost=73.32)
        soldProduct2 = add_sold_product(db=self.db,
                                        saleTransactionId=saleTransaction["sale_transaction_id"],
                                        productId=product2["product_id"],
                                        unitPrice=38.22,
                                        quantity=900.75,
                                        productUnitId=productUnit2["product_unit_id"],
                                        cost=89.88)
        soldProduct3 = add_sold_product(db=self.db,
                                        saleTransactionId=saleTransaction["sale_transaction_id"],
                                        productId=product3["product_id"],
                                        unitPrice=76.22,
                                        quantity=700.75,
                                        productUnitId=productUnit3["product_unit_id"],
                                        cost=77.32)

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
                            round(soldProduct1["cost"] - soldProduct1["discount"], 2),
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
                            round(soldProduct2["cost"] - soldProduct2["discount"], 2),
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
                            soldProduct3["cost"] - soldProduct3["discount"],
                            "Total revenue mismatch.")
        self.assertEqual(fetchedMostSoldProducts[2]["total_quantity"], 
                            soldProduct3["quantity"],
                            "Total quantity mismatch.")

def add_product_category(db, category):
    productCategory = {
        "category": category,
        "user_id": 1
    }

    categoryTable = db.schema.get_table("product_category")
    result = categoryTable.insert("category",
                                    "user_id") \
                            .values(tuple(productCategory.values())) \
                            .execute()
    productCategory.update(DatabaseResult(result).fetch_one("product_category_id"))
    return productCategory

def add_product(db, productCategoryId, product):
    productDict = {
        "product_category_id": productCategoryId,
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

    productUnitTable = db.schema.get_table("product_unit")
    result = productUnitTable.insert("product_id",
                                        "unit",
                                        "base_unit_equivalent",
                                        "preferred",
                                        "cost_price",
                                        "retail_price",
                                        "currency",
                                        "user_id") \
                                    .values(tuple(productUnit.values())) \
                                    .execute()
    productUnit.update(DatabaseResult(result).fetch_one("product_unit_id"))
    return productUnit

def add_sale_transaction(db, customerName):
    saleTransaction = {
        "customer_id": None,
        "customer_name": customerName,
        "user_id": 1
    }

    saleTransactionTable = db.schema.get_table("sale_transaction")
    result = saleTransactionTable.insert("customer_id",
                                            "customer_name",
                                            "user_id") \
                                    .values(tuple(saleTransaction.values())) \
                                    .execute()
    saleTransaction.update(DatabaseResult(result).fetch_one("sale_transaction_id"))
    return saleTransaction

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

    soldProductTable = db.schema.get_table("sold_product")
    result = soldProductTable.insert("sale_transaction_id",
                                        "product_id",
                                        "product_unit_id",
                                        "unit_price",
                                        "quantity",
                                        "cost",
                                        "discount",
                                        "currency",
                                        "user_id") \
                                .values(tuple(soldProduct.values())) \
                                .execute()
    soldProduct.update(DatabaseResult(result).fetch_one("sold_product_id"))
    return soldProduct

def fetch_most_sold_products(db, fromDate, toDate, limit=0):
    sqlResult = db.call_procedure("FetchMostSoldProducts", (fromDate, toDate, limit))
    return DatabaseResult(sqlResult).fetch_all()

if __name__ == '__main__':
    unittest.main()