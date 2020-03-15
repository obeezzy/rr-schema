#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class ViewSoldProducts(StoredProcedureTestCase):
    def test_view_sold_products(self):
        productCategory1 = add_product_category(db=self.db,
                                                category="Consoles")
        product1 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Xbox One")
        productUnit1 = add_product_unit(db=self.db,
                                        productId=product1["product_id"],
                                        unit="box(es)",
                                        costPrice=95.22,
                                        retailPrice=199.33)
        productCategory2 = add_product_category(db=self.db,
                                                category="Mice")
        product2 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Logitech MX Master")
        productUnit2 = add_product_unit(db=self.db,
                                        productId=product2["product_id"],
                                        unit="box(es)",
                                        costPrice=95.22,
                                        retailPrice=199.33)
        saleTransaction = add_sale_transaction(db=self.db,
                                                customerName="Mary-Jane Watson")
        soldProduct1 = add_sold_product(db=self.db,
                                            saleTransactionId=saleTransaction["sale_transaction_id"],
                                            productId=product1["product_id"],
                                            productUnitId=productUnit1["product_unit_id"],
                                            unitPrice=1038.38,
                                            quantity=375.25,
                                            cost=69.57,
                                            discount=38.21)
        soldProduct2 = add_sold_product(db=self.db,
                                            saleTransactionId=saleTransaction["sale_transaction_id"],
                                            productId=product1["product_id"],
                                            productUnitId=productUnit1["product_unit_id"],
                                            unitPrice=38.38,
                                            quantity=99.25,
                                            cost=39.57,
                                            discount=38.21)
        soldProduct3 = add_sold_product(db=self.db,
                                            saleTransactionId=saleTransaction["sale_transaction_id"],
                                            productId=product2["product_id"],
                                            productUnitId=productUnit2["product_unit_id"],
                                            unitPrice=23.38,
                                            quantity=399.25,
                                            cost=11.57,
                                            discount=53.21)
        fetchedSoldProducts = fetch_sold_products(self.db)

        self.assertEqual(len(fetchedSoldProducts), 3, "Expected 3 sold products.")
        self.assertEqual(fetchedSoldProducts[0]["sold_product_id"],
                            soldProduct1["sold_product_id"],
                            "Sold product ID mismatch.")
        self.assertEqual(fetchedSoldProducts[0]["sale_transaction_id"],
                            soldProduct1["sale_transaction_id"],
                            "Sale transaction ID mismatch.")
        self.assertEqual(fetchedSoldProducts[0]["product_id"],
                            soldProduct1["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedSoldProducts[0]["product_unit_id"],
                            soldProduct1["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(fetchedSoldProducts[0]["unit_price"],
                            soldProduct1["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(fetchedSoldProducts[0]["quantity"],
                            soldProduct1["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(fetchedSoldProducts[0]["cost"],
                            soldProduct1["cost"],
                            "Cost mismatch.")
        self.assertEqual(fetchedSoldProducts[0]["discount"],
                            soldProduct1["discount"],
                            "Discount mismatch.")
        self.assertEqual(fetchedSoldProducts[0]["currency"],
                            soldProduct1["currency"],
                            "Currency mismatch.")
        self.assertEqual(fetchedSoldProducts[0]["user_id"],
                            soldProduct1["user_id"],
                            "User ID mismatch.")

        self.assertEqual(fetchedSoldProducts[1]["sold_product_id"],
                            soldProduct2["sold_product_id"],
                            "Sold product ID mismatch.")
        self.assertEqual(fetchedSoldProducts[1]["sale_transaction_id"],
                            soldProduct2["sale_transaction_id"],
                            "Sale transaction ID mismatch.")
        self.assertEqual(fetchedSoldProducts[1]["product_id"],
                            soldProduct1["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedSoldProducts[1]["product_unit_id"],
                            soldProduct2["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(fetchedSoldProducts[1]["unit_price"],
                            soldProduct2["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(fetchedSoldProducts[1]["quantity"],
                            soldProduct2["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(fetchedSoldProducts[1]["cost"],
                            soldProduct2["cost"],
                            "Cost mismatch.")
        self.assertEqual(fetchedSoldProducts[1]["discount"],
                            soldProduct2["discount"],
                            "Discount mismatch.")
        self.assertEqual(fetchedSoldProducts[1]["currency"],
                            soldProduct2["currency"],
                            "Currency mismatch.")
        self.assertEqual(fetchedSoldProducts[1]["user_id"],
                            soldProduct2["user_id"],
                            "User ID mismatch.")

        self.assertEqual(fetchedSoldProducts[2]["sold_product_id"],
                            soldProduct3["sold_product_id"],
                            "Sold product ID mismatch.")
        self.assertEqual(fetchedSoldProducts[2]["sale_transaction_id"],
                            soldProduct3["sale_transaction_id"],
                            "Sale transaction ID mismatch.")
        self.assertEqual(fetchedSoldProducts[2]["product_id"],
                            soldProduct3["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedSoldProducts[2]["product_unit_id"],
                            soldProduct3["product_unit_id"],
                            "Product unit ID mismatch.")
        self.assertEqual(fetchedSoldProducts[2]["unit_price"],
                            soldProduct3["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(fetchedSoldProducts[2]["quantity"],
                            soldProduct3["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(fetchedSoldProducts[2]["cost"],
                            soldProduct3["cost"],
                            "Cost mismatch.")
        self.assertEqual(fetchedSoldProducts[2]["discount"],
                            soldProduct3["discount"],
                            "Discount mismatch.")
        self.assertEqual(fetchedSoldProducts[2]["currency"],
                            soldProduct3["currency"],
                            "Currency mismatch.")
        self.assertEqual(fetchedSoldProducts[2]["user_id"],
                            soldProduct3["user_id"],
                            "User ID mismatch.")

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

def fetch_sold_products(db):
    soldProductTable = db.schema.get_table("sold_product")
    rowResult = soldProductTable.select("id AS sold_product_id",
                                            "sale_transaction_id AS sale_transaction_id",
                                            "product_id AS product_id",
                                            "product_unit_id AS product_unit_id",
                                            "unit_price AS unit_price",
                                            "quantity AS quantity",
                                            "cost AS cost",
                                            "discount AS discount",
                                            "currency AS currency",
                                            "user_id AS user_id") \
                                        .execute()
    return DatabaseResult(rowResult).fetch_all()

if __name__ == '__main__':
    unittest.main()