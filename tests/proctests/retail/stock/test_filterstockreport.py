#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from datetime import datetime, date, timedelta
from decimal import Decimal

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
                                                costPrice=Decimal("6.38"),
                                                retailPrice=Decimal("50.38"))
        self.productQuantitySnapshot1 = add_product_quantity_snapshot(db=self.db,
                                                                    productId=self.product1["product_id"],
                                                                    quantity=39294.28)
        self.currentProductQuantity1 = add_product_quantity(db=self.db,
                                                                    productId=self.product1["product_id"],
                                                                    quantity=self.productQuantitySnapshot1["quantity"])
        self.product2 = add_product(db=self.db,
                                    productCategoryId=self.productCategory1["product_category_id"],
                                    product="Arch Linux")
        self.productUnit2 = add_product_unit(db=self.db,
                                                productId=self.product2["product_id"],
                                                unit="unit(s)",
                                                costPrice=Decimal("489.28"),
                                                retailPrice=Decimal("550.38"))
        self.productQuantitySnapshot2 = add_product_quantity_snapshot(db=self.db,
                                                                    productId=self.product2["product_id"],
                                                                    quantity=3452.28)
        self.currentProductQuantity2 = add_product_quantity(db=self.db,
                                                                    productId=self.product2["product_id"],
                                                                    quantity=self.productQuantitySnapshot2["quantity"])

        self.productCategory2 = add_product_category(db=self.db,
                                                        category="Android versions")
        self.product3 = add_product(db=self.db,
                                    productCategoryId=self.productCategory2["product_category_id"],
                                    product="Oreo")
        self.productUnit3 = add_product_unit(db=self.db,
                                                productId=self.product3["product_id"],
                                                unit="unit(s)",
                                                costPrice=Decimal("138456.83"),
                                                retailPrice=Decimal("383593.32"))
        self.productQuantitySnapshot3 = add_product_quantity_snapshot(db=self.db,
                                                                    productId=self.product3["product_id"],
                                                                    quantity=2333.90)
        self.currentProductQuantity3 = add_product_quantity(db=self.db,
                                                                    productId=self.product3["product_id"],
                                                                    quantity=self.productQuantitySnapshot3["quantity"])
        self.saleTransaction1 = add_sale_transaction(db=self.db, 
                                                     customerName="Susan Richards")
        self.soldProduct1 = add_sold_product(db=self.db,
                                                saleTransactionId=self.saleTransaction1["sale_transaction_id"],
                                                productId=self.product1["product_id"],
                                                unitPrice=Decimal("38.27"),
                                                quantity=29.5,
                                                productUnitId=self.productUnit1["product_unit_id"],
                                                cost=Decimal("378.28"),
                                                discount=Decimal("8.28"))
        self.newQuantity1 = self.currentProductQuantity1["quantity"] - self.soldProduct1["quantity"],
        alter_product_quantity(db=self.db,
                                productId=self.product1["product_id"],
                                newQuantity=self.newQuantity1)

        self.soldProduct2 = add_sold_product(db=self.db,
                                                saleTransactionId=self.saleTransaction1["sale_transaction_id"],
                                                productId=self.product2["product_id"],
                                                unitPrice=Decimal("38.27"),
                                                quantity=44.5,
                                                productUnitId=self.productUnit2["product_unit_id"],
                                                cost=Decimal("378.28"),
                                                discount=Decimal("8.28"))
        self.soldProduct3 = add_sold_product(db=self.db,
                                                saleTransactionId=self.saleTransaction1["sale_transaction_id"],
                                                productId=self.product2["product_id"],
                                                unitPrice=Decimal("38.27"),
                                                quantity=33.5,
                                                productUnitId=self.productUnit2["product_unit_id"],
                                                cost=Decimal("378.28"),
                                                discount=Decimal("8.28"))
        self.newQuantity2 = self.currentProductQuantity2["quantity"] - self.soldProduct2["quantity"] - self.soldProduct3["quantity"]
        alter_product_quantity(db=self.db,
                                productId=self.product2["product_id"],
                                newQuantity=self.newQuantity2)

        self.purchaseTransaction1 = add_purchase_transaction(db=self.db,
                                                                vendorName="Harley Quinn")
        self.purchasedProduct1 = add_purchased_product(db=self.db,
                                                        purchaseTransactionId=self.purchaseTransaction1["purchase_transaction_id"],
                                                        productId=self.product3["product_id"],
                                                        unitPrice=Decimal("38.27"),
                                                        quantity=38.5,
                                                        productUnitId=self.productUnit3["product_unit_id"],
                                                        cost=Decimal("378.28"),
                                                        discount=Decimal("8.28"))

        self.purchaseTransaction2 = add_purchase_transaction(db=self.db,
                                                                vendorName="Harley Quinn")
        self.purchasedProduct2 = add_purchased_product(db=self.db,
                                                        purchaseTransactionId=self.purchaseTransaction2["purchase_transaction_id"],
                                                        productId=self.product3["product_id"],
                                                        unitPrice=Decimal("38.27"),
                                                        quantity=22.5,
                                                        productUnitId=self.productUnit3["product_unit_id"],
                                                        cost=Decimal("378.28"),
                                                        discount=Decimal("8.28"))
        self.newQuantity3 = self.currentProductQuantity3["quantity"] + self.purchasedProduct1["quantity"] + self.purchasedProduct2["quantity"]
        alter_product_quantity(db=self.db,
                                productId=self.product3["product_id"],
                                newQuantity=self.newQuantity3)

    @unittest.skip("Needs to be refactored.")
    def test_filter_stock_report(self):
        today = date.today()
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
                            self.purchasedProduct1["quantity"] + self.purchasedProduct2["quantity"],
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

    @unittest.skip("Needs to be refactored.")
    def test_apply_filter(self):
        today = date.today()
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

    @unittest.skip("Needs to be refactored.")
    def test_apply_sort(self):
        today = date.today()
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

def add_sale_transaction(db, customerName, discount=0, suspended=False, noteId=None):
    saleTransaction = {
        "customer_name": customerName,
        "customer_id": None,
        "discount": discount,
        "suspended": suspended,
        "note_id": noteId,
        "user_id": 1
    }

    db.execute("""INSERT INTO sale_transaction (customer_name,
                                                customer_id,
                                                discount,
                                                suspended,
                                                note_id,
                                                user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id AS sale_transaction_id,
                    customer_name,
                    customer_id,
                    discount,
                    suspended,
                    note_id,
                    user_id""", tuple(saleTransaction.values()))
    result = {}
    for row in db:
        result = {
            "sale_transaction_id": row["sale_transaction_id"],
            "customer_name": row["customer_name"],
            "customer_id": row["customer_id"],
            "discount": row["discount"],
            "suspended": row["suspended"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

def add_purchase_transaction(db, vendorName, discount=0, suspended=False, noteId=None):
    purchaseTransaction = {
        "vendor_name": vendorName,
        "vendor_id": None,
        "discount": discount,
        "suspended": suspended,
        "note_id": noteId,
        "user_id": 1
    }

    db.execute("""INSERT INTO sale_transaction (customer_name,
                                                customer_id,
                                                discount,
                                                suspended,
                                                note_id,
                                                user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id AS purchase_transaction_id,
                    customer_name,
                    customer_id,
                    discount,
                    suspended,
                    note_id,
                    user_id""", tuple(purchaseTransaction.values()))
    result = {}
    for row in db:
        result = {
            "purchase_transaction_id": row["purchase_transaction_id"],
            "customer_id": row["customer_id"],
            "customer_name": row["customer_name"],
            "discount": row["discount"],
            "suspended": row["suspended"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

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

    db.execute("""INSERT INTO sold_product (sale_transaction_id,
                                            product_id,
                                            unit_price,
                                            quantity,
                                            product_unit_id,
                                            currency,
                                            cost,
                                            discount,
                                            user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS sold_product_id,
                    sale_transaction_id,
                    product_id,
                    unit_price,
                    quantity,
                    product_unit_id,
                    currency,
                    cost,
                    discount,
                    user_id""", tuple(soldProduct.values()))
    result = {}
    for row in db:
        result = {
            "sold_product_id": row["sold_product_id"],
            "sale_transaction_id": row["sale_transaction_id"],
            "product_id": row["product_id"],
            "unit_price": row["unit_price"],
            "quantity": row["quantity"],
            "product_unit_id": row["product_unit_id"],
            "currency": row["currency"],
            "cost": row["cost"],
            "discount": row["discount"],
            "user_id": row["user_id"]
        }
    return result

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

    db.execute("""INSERT INTO purchased_product (purchase_transaction_id,
                                                    product_id,
                                                    unit_price,
                                                    quantity,
                                                    product_unit_id,
                                                    currency,
                                                    cost,
                                                    note_id,
                                                    discount,
                                                    user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS purchased_product_id,
                    purchase_transaction_id,
                    product_id,
                    unit_price,
                    quantity,
                    product_unit_id,
                    currency,
                    cost,
                    note_id,
                    discount,
                    user_id""", tuple(purchasedProduct.values()))
    result = {}
    for row in db:
        result = {
            "purchased_product_id": row["purchased_product_id"],
            "purchase_transaction_id": row["purchase_transaction_id"],
            "product_id": row["product_id"],
            "unit_price": row["unit_price"],
            "quantity": row["quantity"],
            "product_unit_id": row["product_unit_id"],
            "currency": row["currency"],
            "cost": row["cost"],
            "note_id": row["note_id"],
            "discount": row["discount"],
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

def add_product_quantity_snapshot(db, productId, quantity):
    productQuantitySnapshot = {
        "product_id": productId,
        "quantity": quantity,
        "reason": "sale_transaction",
        "user_id": 1
    }

    db.execute("""INSERT INTO product_quantity_snapshot (product_id,
                                                        quantity,
                                                        reason,
                                                        user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id AS product_quantity_snapshot_id,
                    product_id,
                    quantity,
                    reason,
                    user_id""", tuple(productQuantitySnapshot.values()))
    result = {}
    for row in db:
        result = {
            "product_quantity_snapshot_id": row["product_quantity_snapshot_id"],
            "product_id": row["product_id"],
            "quantity": row["quantity"],
            "reason": row["reason"],
            "user_id": row["user_id"]
        }
    return result

def add_product_quantity(db, productId, quantity):
    currentProductQuantity = {
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
                    user_id""", tuple(currentProductQuantity.values()))
    result = {}
    for row in db:
        result = {
            "product_quantity_id": row["product_quantity_id"],
            "product_id": row["product_id"],
            "quantity": row["quantity"],
            "user_id": row["user_id"]
        }
    return result

def alter_product_quantity(db, productId, newQuantity):
    db.execute("""UPDATE product_quantity
                    SET quantity = %s
                    WHERE product_id = %s""", [newQuantity, productId])

def filter_stock_report(db, filterColumn, filterText, sortColumn, sortOrder, fromDate, toDate):
    db.call_procedure("FilterStockReport", [filterColumn, filterText, sortColumn, sortOrder, fromDate, toDate])
    results = []
    for row in db:
        result = {
            "": row[""],
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
