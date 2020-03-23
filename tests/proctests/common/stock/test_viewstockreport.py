#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult
from datetime import datetime, date, timedelta

class ViewStockReport(StoredProcedureTestCase):
    def test_view_stock_report(self):
        productCategory1 = add_product_category(db=self.db,
                                                category="Weapons")
        product1 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Mjolnir")
        productUnit1 = add_product_unit(db=self.db,
                                        productId=product1["product_id"],
                                        unit="unit(s)",
                                        costPrice=6.38,
                                        retailPrice=50.38)
        initialProductQuantity1 = add_initial_product_quantity(db=self.db,
                                                                productId=product1["product_id"],
                                                                quantity=39294.28)
        currentProductQuantity1 = add_current_product_quantity(db=self.db,
                                                                productId=product1["product_id"],
                                                                quantity=initialProductQuantity1["quantity"])
        product2 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Captain America's shield")
        productUnit2 = add_product_unit(db=self.db,
                                        productId=product2["product_id"],
                                        unit="unit(s)",
                                        costPrice=489.28,
                                        retailPrice=550.38)
        initialProductQuantity2 = add_initial_product_quantity(db=self.db,
                                                                productId=product2["product_id"],
                                                                quantity=3452.28)
        currentProductQuantity2 = add_current_product_quantity(db=self.db,
                                                                productId=product2["product_id"],
                                                                quantity=initialProductQuantity2["quantity"])

        productCategory2 = add_product_category(db=self.db,
                                                category="More Weapons")
        product3 = add_product(db=self.db,
                                productCategoryId=productCategory2["product_category_id"],
                                product="Hawkeye's arrow")
        productUnit3 = add_product_unit(db=self.db,
                                        productId=product3["product_id"],
                                        unit="unit(s)",
                                        costPrice=138456.83,
                                        retailPrice=383593.32)
        initialProductQuantity3 = add_initial_product_quantity(db=self.db,
                                                                productId=product3["product_id"],
                                                                quantity=2333.90)
        currentProductQuantity3 = add_current_product_quantity(db=self.db,
                                                                productId=product3["product_id"],
                                                                quantity=initialProductQuantity3["quantity"])
        saleTransaction1 = add_sale_transaction(db=self.db, 
                                                customerName="Susan Richards")
        soldProduct1 = add_sold_product(db=self.db,
                                            saleTransactionId=saleTransaction1["sale_transaction_id"],
                                            productId=product1["product_id"],
                                            unitPrice=38.27,
                                            quantity=29.5,
                                            productUnitId=productUnit1["product_unit_id"],
                                            cost=378.28,
                                            discount=8.28)
        newQuantity1 = round(currentProductQuantity1["quantity"] - soldProduct1["quantity"], 2)
        alter_product_quantity(db=self.db,
                                productId=product1["product_id"],
                                newQuantity=newQuantity1)

        soldProduct2 = add_sold_product(db=self.db,
                                            saleTransactionId=saleTransaction1["sale_transaction_id"],
                                            productId=product2["product_id"],
                                            unitPrice=38.27,
                                            quantity=44.5,
                                            productUnitId=productUnit2["product_unit_id"],
                                            cost=378.28,
                                            discount=8.28)
        soldProduct3 = add_sold_product(db=self.db,
                                            saleTransactionId=saleTransaction1["sale_transaction_id"],
                                            productId=product2["product_id"],
                                            unitPrice=38.27,
                                            quantity=33.5,
                                            productUnitId=productUnit2["product_unit_id"],
                                            cost=378.28,
                                            discount=8.28)
        newQuantity2 = round(currentProductQuantity2["quantity"] - soldProduct2["quantity"] - soldProduct3["quantity"], 2)
        alter_product_quantity(db=self.db,
                                productId=product2["product_id"],
                                newQuantity=newQuantity2)

        purchaseTransaction1 = add_purchase_transaction(db=self.db,
                                                        vendorName="Harley Quinn")
        purchasedProduct1 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction1["purchase_transaction_id"],
                                                    productId=product3["product_id"],
                                                    unitPrice=38.27,
                                                    quantity=38.5,
                                                    productUnitId=productUnit3["product_unit_id"],
                                                    cost=378.28,
                                                    discount=8.28)

        purchaseTransaction2 = add_purchase_transaction(db=self.db,
                                                        vendorName="Harley Quinn")
        purchasedProduct2 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction2["purchase_transaction_id"],
                                                    productId=product3["product_id"],
                                                    unitPrice=38.27,
                                                    quantity=22.5,
                                                    productUnitId=productUnit3["product_unit_id"],
                                                    cost=378.28,
                                                    discount=8.28)
        newQuantity3 = round(currentProductQuantity3["quantity"] + purchasedProduct1["quantity"] + purchasedProduct2["quantity"], 2)
        alter_product_quantity(db=self.db,
                                productId=product3["product_id"],
                                newQuantity=newQuantity3)

        today = date.today()
        tomorrow = today + timedelta(days=1)
        viewedStockReport = view_stock_report(db=self.db,
                                                fromDate=today,
                                                toDate=tomorrow)

        self.assertEqual(len(viewedStockReport), 3, "Expected 3 transactions.")
        self.assertEqual(viewedStockReport[0]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch")
        self.assertEqual(viewedStockReport[0]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch")
        self.assertEqual(viewedStockReport[0]["product_id"],
                            product1["product_id"],
                            "Product ID mismatch")
        self.assertEqual(viewedStockReport[0]["product"],
                            product1["product"],
                            "Product mismatch")
        self.assertEqual(viewedStockReport[0]["quantity_sold"],
                            soldProduct1["quantity"],
                            "Quantity sold mismatch")
        self.assertEqual(viewedStockReport[0]["quantity_bought"],
                            0,
                            "Quantity bought mismatch")
        self.assertEqual(viewedStockReport[0]["quantity_in_stock"],
                            newQuantity1,
                            "Quantity in stock mismatch")

        self.assertEqual(viewedStockReport[1]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch")
        self.assertEqual(viewedStockReport[1]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch")
        self.assertEqual(viewedStockReport[1]["product_id"],
                            product2["product_id"],
                            "Product ID mismatch")
        self.assertEqual(viewedStockReport[1]["product"],
                            product2["product"],
                            "Product mismatch")
        self.assertEqual(viewedStockReport[1]["quantity_sold"],
                            soldProduct2["quantity"] + soldProduct3["quantity"],
                            "Quantity sold mismatch")
        self.assertEqual(viewedStockReport[1]["quantity_bought"],
                            0,
                            "Quantity bought mismatch")
        self.assertEqual(viewedStockReport[1]["quantity_in_stock"],
                            newQuantity2,
                            "Quantity in stock mismatch")

        self.assertEqual(viewedStockReport[2]["product_category_id"],
                            productCategory2["product_category_id"],
                            "Product category ID mismatch")
        self.assertEqual(viewedStockReport[2]["product_category"],
                            productCategory2["category"],
                            "Product category mismatch")
        self.assertEqual(viewedStockReport[2]["product_id"],
                            product3["product_id"],
                            "Product ID mismatch")
        self.assertEqual(viewedStockReport[2]["product"],
                            product3["product"],
                            "Product mismatch")
        self.assertEqual(viewedStockReport[2]["quantity_sold"],
                            0,
                            "Quantity sold mismatch")
        self.assertEqual(viewedStockReport[2]["quantity_bought"],
                            purchasedProduct1["quantity"] + purchasedProduct2["quantity"],
                            "Quantity bought mismatch")
        self.assertEqual(viewedStockReport[2]["quantity_in_stock"],
                            newQuantity3,
                            "Quantity in stock mismatch")

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

def view_stock_report(db, fromDate, toDate):
    sqlResult = db.call_procedure("ViewStockReport", (
                                    fromDate,
                                    toDate))
    return DatabaseResult(sqlResult).fetch_all()

if __name__ == '__main__':
    unittest.main()