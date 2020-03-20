#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult
from datetime import datetime, timedelta

class FilterStockReport(StoredProcedureTestCase):
    def setUp(self):
        super().setUp()
        self.productCategory1 = add_product_category(db=self.db,
                                                        category="Linux distros")
        self.product1 = add_product(db=self.db,
                                    productCategoryId=self.productCategory1["product_category_id"],
                                    product="Ubuntu")
        self.productUnit1 = add_product_unit(db=self.db,
                                                productId=self.product1["product_id"],
                                                unit="unit(s)",
                                                costPrice=6.38,
                                                retailPrice=50.38)
        self.initialProductQuantity1 = add_initial_product_quantity(db=self.db,
                                                                    productId=self.product1["product_id"],
                                                                    quantity=39294.28)
        self.currentProductQuantity1 = add_current_product_quantity(db=self.db,
                                                                    productId=self.product1["product_id"],
                                                                    quantity=self.initialProductQuantity1["quantity"])
        self.product2 = add_product(db=self.db,
                                    productCategoryId=self.productCategory1["product_category_id"],
                                    product="Arch Linux")
        self.productUnit2 = add_product_unit(db=self.db,
                                                productId=self.product2["product_id"],
                                                unit="unit(s)",
                                                costPrice=489.28,
                                                retailPrice=550.38)
        self.initialProductQuantity2 = add_initial_product_quantity(db=self.db,
                                                                    productId=self.product2["product_id"],
                                                                    quantity=3452.28)
        self.currentProductQuantity2 = add_current_product_quantity(db=self.db,
                                                                    productId=self.product2["product_id"],
                                                                    quantity=self.initialProductQuantity2["quantity"])

        self.productCategory2 = add_product_category(db=self.db,
                                                        category="Android versions")
        self.product3 = add_product(db=self.db,
                                    productCategoryId=self.productCategory2["product_category_id"],
                                    product="Oreo")
        self.productUnit3 = add_product_unit(db=self.db,
                                                productId=self.product3["product_id"],
                                                unit="unit(s)",
                                                costPrice=138456.83,
                                                retailPrice=383593.32)
        self.initialProductQuantity3 = add_initial_product_quantity(db=self.db,
                                                                    productId=self.product3["product_id"],
                                                                    quantity=2333.90)
        self.currentProductQuantity3 = add_current_product_quantity(db=self.db,
                                                                    productId=self.product3["product_id"],
                                                                    quantity=self.initialProductQuantity3["quantity"])
        self.saleTransaction1 = add_sale_transaction(db=self.db, 
                                                     customerName="Susan Richards")
        self.soldProduct1 = add_sold_product(db=self.db,
                                                saleTransactionId=self.saleTransaction1["sale_transaction_id"],
                                                productId=self.product1["product_id"],
                                                unitPrice=38.27,
                                                quantity=29.5,
                                                productUnitId=self.productUnit1["product_unit_id"],
                                                cost=378.28,
                                                discount=8.28)
        self.newQuantity1 = round(self.currentProductQuantity1["quantity"] - self.soldProduct1["quantity"], 2)
        alter_product_quantity(db=self.db,
                                productId=self.product1["product_id"],
                                newQuantity=self.newQuantity1)

        self.soldProduct2 = add_sold_product(db=self.db,
                                                saleTransactionId=self.saleTransaction1["sale_transaction_id"],
                                                productId=self.product2["product_id"],
                                                unitPrice=38.27,
                                                quantity=44.5,
                                                productUnitId=self.productUnit2["product_unit_id"],
                                                cost=378.28,
                                                discount=8.28)
        self.soldProduct3 = add_sold_product(db=self.db,
                                                saleTransactionId=self.saleTransaction1["sale_transaction_id"],
                                                productId=self.product2["product_id"],
                                                unitPrice=38.27,
                                                quantity=33.5,
                                                productUnitId=self.productUnit2["product_unit_id"],
                                                cost=378.28,
                                                discount=8.28)
        self.newQuantity2 = round(self.currentProductQuantity2["quantity"] - self.soldProduct2["quantity"] - self.soldProduct3["quantity"], 2)
        alter_product_quantity(db=self.db,
                                productId=self.product2["product_id"],
                                newQuantity=self.newQuantity2)

        self.purchaseTransaction1 = add_purchase_transaction(db=self.db,
                                                                vendorName="Harley Quinn")
        self.purchasedProduct1 = add_purchased_product(db=self.db,
                                                        purchaseTransactionId=self.purchaseTransaction1["purchase_transaction_id"],
                                                        productId=self.product3["product_id"],
                                                        unitPrice=38.27,
                                                        quantity=38.5,
                                                        productUnitId=self.productUnit3["product_unit_id"],
                                                        cost=378.28,
                                                        discount=8.28)

        self.purchaseTransaction2 = add_purchase_transaction(db=self.db,
                                                                vendorName="Harley Quinn")
        self.purchasedProduct2 = add_purchased_product(db=self.db,
                                                        purchaseTransactionId=self.purchaseTransaction2["purchase_transaction_id"],
                                                        productId=self.product3["product_id"],
                                                        unitPrice=38.27,
                                                        quantity=22.5,
                                                        productUnitId=self.productUnit3["product_unit_id"],
                                                        cost=378.28,
                                                        discount=8.28)
        self.newQuantity3 = round(self.currentProductQuantity3["quantity"] + self.purchasedProduct1["quantity"] + self.purchasedProduct2["quantity"], 2)
        alter_product_quantity(db=self.db,
                                productId=self.product3["product_id"],
                                newQuantity=self.newQuantity3)

    def test_filter_stock_report(self):
        today = datetime.date(datetime.now())
        tomorrow = today + timedelta(days=1)
        filteredStockReport = filter_stock_report(db=self.db,
                                                    filterColumn="product_category",
                                                    filterText="",
                                                    sortColumn="product_category",
                                                    sortOrder="ascending",
                                                    fromDate=today,
                                                    toDate=tomorrow)

        self.assertEqual(len(filteredStockReport), 3, "Expected 3 transactions.")
        self.assertEqual(filteredStockReport[0]["product_category_id"],
                            self.productCategory2["product_category_id"],
                            "Product category ID mismatch")
        self.assertEqual(filteredStockReport[0]["product_category"],
                            self.productCategory2["category"],
                            "Product category mismatch")
        self.assertEqual(filteredStockReport[0]["product_id"],
                            self.product3["product_id"],
                            "Product ID mismatch")
        self.assertEqual(filteredStockReport[0]["product"],
                            self.product3["product"],
                            "Product mismatch")
        self.assertEqual(filteredStockReport[0]["quantity_sold"],
                            0,
                            "Quantity sold mismatch")
        self.assertEqual(filteredStockReport[0]["quantity_bought"],
                            round(self.purchasedProduct1["quantity"] + self.purchasedProduct2["quantity"], 2),
                            "Quantity bought mismatch")
        self.assertEqual(filteredStockReport[0]["quantity_in_stock"],
                            self.newQuantity3,
                            "Quantity in stock mismatch")

        self.assertEqual(filteredStockReport[1]["product_category_id"],
                            self.productCategory1["product_category_id"],
                            "Product category ID mismatch")
        self.assertEqual(filteredStockReport[1]["product_category"],
                            self.productCategory1["category"],
                            "Product category mismatch")
        self.assertEqual(filteredStockReport[1]["product_id"],
                            self.product2["product_id"],
                            "Product ID mismatch")
        self.assertEqual(filteredStockReport[1]["product"],
                            self.product2["product"],
                            "Product mismatch")
        self.assertEqual(filteredStockReport[1]["quantity_sold"],
                            self.soldProduct2["quantity"] + self.soldProduct3["quantity"],
                            "Quantity sold mismatch")
        self.assertEqual(filteredStockReport[1]["quantity_bought"],
                            0,
                            "Quantity bought mismatch")
        self.assertEqual(filteredStockReport[1]["quantity_in_stock"],
                            self.newQuantity2,
                            "Quantity in stock mismatch")

        self.assertEqual(filteredStockReport[2]["product_category_id"],
                            self.productCategory1["product_category_id"],
                            "Product category ID mismatch")
        self.assertEqual(filteredStockReport[2]["product_category"],
                            self.productCategory1["category"],
                            "Product category mismatch")
        self.assertEqual(filteredStockReport[2]["product_id"],
                            self.product1["product_id"],
                            "Product ID mismatch")
        self.assertEqual(filteredStockReport[2]["product"],
                            self.product1["product"],
                            "Product mismatch")
        self.assertEqual(filteredStockReport[2]["quantity_sold"],
                            self.soldProduct1["quantity"],
                            "Quantity sold mismatch")
        self.assertEqual(filteredStockReport[2]["quantity_bought"],
                            0,
                            "Quantity bought mismatch")
        self.assertEqual(filteredStockReport[2]["quantity_in_stock"],
                            self.newQuantity1,
                            "Quantity in stock mismatch")

    def test_apply_filter(self):
        today = datetime.date(datetime.now())
        tomorrow = today + timedelta(days=1)
        filteredStockReport = filter_stock_report(db=self.db,
                                                    filterColumn="product_category",
                                                    filterText="lin",
                                                    sortColumn="product_category",
                                                    sortOrder="ascending",
                                                    fromDate=today,
                                                    toDate=tomorrow)
        self.assertEqual(len(filteredStockReport), 2, "Expected 2 transactions.")
        self.assertEqual(filteredStockReport[0]["product_id"],
                            self.product2["product_id"],
                            "Product ID mismatch")
        self.assertEqual(filteredStockReport[1]["product_id"],
                            self.product1["product_id"],
                            "Product ID mismatch")

    def test_apply_sort(self):
        today = datetime.date(datetime.now())
        tomorrow = today + timedelta(days=1)
        filteredStockReport = filter_stock_report(db=self.db,
                                                    filterColumn=None,
                                                    filterText=None,
                                                    sortColumn="product_category",
                                                    sortOrder="ascending",
                                                    fromDate=today,
                                                    toDate=tomorrow)
        self.assertEqual(len(filteredStockReport), 3, "Expected 3 transactions.")
        self.assertEqual(filteredStockReport[0]["product_id"],
                            self.product3["product_id"],
                            "Product ID mismatch")
        self.assertEqual(filteredStockReport[1]["product_id"],
                            self.product2["product_id"],
                            "Product ID mismatch")
        self.assertEqual(filteredStockReport[2]["product_id"],
                            self.product1["product_id"],
                            "Product ID mismatch")

def add_product_category(db, category):
    productCategory = {
        "category": category,
        "user_id": 1
    }

    productCategoryTable = db.schema.get_table("product_category")
    result = productCategoryTable.insert("category",
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

def add_sale_transaction(db, customerName, discount=0, suspended=False, noteId=None):
    saleTransaction = {
        "customer_name": customerName,
        "customer_id": None,
        "discount": discount,
        "suspended": suspended,
        "note_id": noteId,
        "user_id": 1
    }

    saleTransactionTable = db.schema.get_table("sale_transaction")
    result = saleTransactionTable.insert("customer_name",
                                            "customer_id",
                                            "discount",
                                            "suspended",
                                            "note_id",
                                            "user_id") \
                                    .values(tuple(saleTransaction.values())) \
                                    .execute()
    saleTransaction.update(DatabaseResult(result).fetch_one("sale_transaction_id"))
    return saleTransaction

def add_purchase_transaction(db, vendorName, discount=0, suspended=False, noteId=None):
    purchaseTransaction = {
        "vendor_name": vendorName,
        "vendor_id": None,
        "discount": discount,
        "suspended": suspended,
        "note_id": noteId,
        "user_id": 1
    }

    purchaseTransactionTable = db.schema.get_table("sale_transaction")
    result = purchaseTransactionTable.insert("customer_name",
                                                "customer_id",
                                                "discount",
                                                "suspended",
                                                "note_id",
                                                "user_id") \
                                        .values(tuple(purchaseTransaction.values())) \
                                        .execute()
    purchaseTransaction.update(DatabaseResult(result).fetch_one("purchase_transaction_id"))
    return purchaseTransaction

def add_sold_product(db, saleTransactionId, productId, unitPrice, quantity, productUnitId, cost, discount=0):
    soldProduct = {
        "sale_transactionId": saleTransactionId,
        "product_id": productId,
        "unit_price": unitPrice,
        "quantity": quantity,
        "product_unit_id": productUnitId,
        "currency": "NGN",
        "cost": cost,
        "discount": discount,
        "user_id": 1
    }

    soldProductTable = db.schema.get_table("sold_product")
    result = soldProductTable.insert("sale_transaction_id",
                                            "product_id",
                                            "unit_price",
                                            "quantity",
                                            "product_unit_id",
                                            "currency",
                                            "cost",
                                            "discount",
                                            "user_id") \
                                    .values(tuple(soldProduct.values())) \
                                    .execute()
    soldProduct.update(DatabaseResult(result).fetch_one("sold_product_id"))
    return soldProduct

def add_purchased_product(db, purchaseTransactionId, productId, unitPrice, quantity, productUnitId, cost, noteId=None, discount=0):
    purchasedProduct = {
        "purchase_transaction_id": purchaseTransactionId,
        "product_id": productId,
        "unit_price": unitPrice,
        "quantity": quantity,
        "product_unit_id": productUnitId,
        "currency": "NGN",
        "cost": cost,
        "note_id": noteId,
        "discount": discount,
        "user_id": 1
    }

    purchasedProductTable = db.schema.get_table("purchased_product")
    result = purchasedProductTable.insert("purchase_transaction_id",
                                            "product_id",
                                            "unit_price",
                                            "quantity",
                                            "product_unit_id",
                                            "currency",
                                            "cost",
                                            "note_id",
                                            "discount",
                                            "user_id") \
                                    .values(tuple(purchasedProduct.values())) \
                                    .execute()
    purchasedProduct.update(DatabaseResult(result).fetch_one("purchased_product_id"))
    return purchasedProduct

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

def add_initial_product_quantity(db, productId, quantity):
    initialProductQuantity = {
        "product_id": productId,
        "quantity": quantity,
        "reason": "sale_transaction",
        "user_id": 1
    }

    initialProductQuantityTable = db.schema.get_table("initial_product_quantity")
    result = initialProductQuantityTable.insert("product_id",
                                                "quantity",
                                                "reason",
                                                "user_id") \
                                            .values(tuple(initialProductQuantity.values())) \
                                            .execute()
    initialProductQuantity.update(DatabaseResult(result).fetch_one("initial_product_quantity_id"))
    return initialProductQuantity

def add_current_product_quantity(db, productId, quantity):
    currentProductQuantity = {
        "product_id": productId,
        "quantity": quantity,
        "user_id": 1
    }

    currentProductQuantityTable = db.schema.get_table("current_product_quantity")
    result = currentProductQuantityTable.insert("product_id",
                                                "quantity",
                                                "user_id") \
                                            .values(tuple(currentProductQuantity.values())) \
                                            .execute()
    currentProductQuantity.update(DatabaseResult(result).fetch_one("current_product_quantity_id"))
    return currentProductQuantity

def alter_product_quantity(db, productId, newQuantity):
    currentProductQuantityTable = db.schema.get_table("current_product_quantity")
    result = currentProductQuantityTable.update() \
                                        .set("quantity", newQuantity) \
                                        .where("product_id = :productId") \
                                        .bind("productId", productId) \
                                        .execute()

def filter_stock_report(db, filterColumn, filterText, sortColumn, sortOrder, fromDate, toDate):
    sqlResult = db.call_procedure("FilterStockReport", (
                                    filterColumn,
                                    filterText,
                                    sortColumn,
                                    sortOrder,
                                    fromDate,
                                    toDate))
    return DatabaseResult(sqlResult).fetch_all()

if __name__ == '__main__':
    unittest.main()