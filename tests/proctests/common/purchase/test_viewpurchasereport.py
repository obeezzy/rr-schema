#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult, DatabaseDateTime
from datetime import datetime, timedelta

class ViewPurchaseReport(StoredProcedureTestCase):
    def test_view_purchase_report(self):
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
        currentProductQuantity1 = add_current_product_quantity(db=self.db,
                                                                productId=product1["product_id"],
                                                                quantity=38.28)
        product2 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Captain America's shield")
        productUnit2 = add_product_unit(db=self.db,
                                        productId=product2["product_id"],
                                        unit="unit(s)",
                                        costPrice=489.28,
                                        retailPrice=550.38)
        currentProductQuantity2 = add_current_product_quantity(db=self.db,
                                                                productId=product2["product_id"],
                                                                quantity=66.28)

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
        currentProductQuantity3 = add_current_product_quantity(db=self.db,
                                                                productId=product3["product_id"],
                                                                quantity=78.90)

        purchaseTransaction1 = add_purchase_transaction(db=self.db,
                                                        vendorName="Selena Kyle")
        purchasedProduct1 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction1["purchase_transaction_id"],
                                                    productId=product1["product_id"],
                                                    unitPrice=38.27,
                                                    quantity=583.5,
                                                    productUnitId=productUnit1["product_unit_id"],
                                                    cost=378.28,
                                                    discount=8.28)
        purchasedProduct2 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction1["purchase_transaction_id"],
                                                    productId=product2["product_id"],
                                                    unitPrice=38.27,
                                                    quantity=583.5,
                                                    productUnitId=productUnit2["product_unit_id"],
                                                    cost=378.28,
                                                    discount=8.28)
        purchasedProduct3 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction1["purchase_transaction_id"],
                                                    productId=product2["product_id"],
                                                    unitPrice=38.27,
                                                    quantity=583.5,
                                                    productUnitId=productUnit2["product_unit_id"],
                                                    cost=378.28,
                                                    discount=8.28)

        purchaseTransaction2 = add_purchase_transaction(db=self.db,
                                                        vendorName="Harley Quinn")
        purchasedProduct4 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction2["purchase_transaction_id"],
                                                    productId=product3["product_id"],
                                                    unitPrice=38.27,
                                                    quantity=583.5,
                                                    productUnitId=productUnit3["product_unit_id"],
                                                    cost=378.28,
                                                    discount=8.28)
        today = datetime.now()
        tomorrow = today + timedelta(days=1, hours=1)
        viewedPurchaseReport = view_purchase_report(db=self.db,
                                                        fromDateTime=today,
                                                        toDateTime=tomorrow)

        self.assertEqual(len(viewedPurchaseReport), 3, "Expected 3 transactions.")
        self.assertEqual(viewedPurchaseReport[0]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch")
        self.assertEqual(viewedPurchaseReport[0]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch")
        self.assertEqual(viewedPurchaseReport[0]["product_id"],
                            product1["product_id"],
                            "Product ID mismatch")
        self.assertEqual(viewedPurchaseReport[0]["product"],
                            product1["product"],
                            "Product mismatch")
        self.assertEqual(viewedPurchaseReport[0]["quantity_bought"],
                            purchasedProduct1["quantity"],
                            "Quantity mismatch")
        self.assertEqual(viewedPurchaseReport[0]["total_cost"],
                            purchasedProduct1["cost"],
                            "Total cost mismatch")

        self.assertEqual(viewedPurchaseReport[1]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch")
        self.assertEqual(viewedPurchaseReport[1]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch")
        self.assertEqual(viewedPurchaseReport[1]["product_id"],
                            product2["product_id"],
                            "Product ID mismatch")
        self.assertEqual(viewedPurchaseReport[1]["product"],
                            product2["product"],
                            "Product mismatch")
        self.assertEqual(viewedPurchaseReport[1]["quantity_bought"],
                            purchasedProduct2["quantity"] + purchasedProduct3["quantity"],
                            "Quantity mismatch")
        self.assertEqual(viewedPurchaseReport[1]["total_cost"],
                            purchasedProduct2["cost"] + purchasedProduct3["cost"],
                            "Total cost mismatch")

        self.assertEqual(viewedPurchaseReport[2]["product_category_id"],
                            productCategory2["product_category_id"],
                            "Product category ID mismatch")
        self.assertEqual(viewedPurchaseReport[2]["product_category"],
                            productCategory2["category"],
                            "Product category mismatch")
        self.assertEqual(viewedPurchaseReport[2]["product_id"],
                            product3["product_id"],
                            "Product ID mismatch")
        self.assertEqual(viewedPurchaseReport[2]["product"],
                            product3["product"],
                            "Product mismatch")
        self.assertEqual(viewedPurchaseReport[2]["quantity_bought"],
                            purchasedProduct4["quantity"],
                            "Quantity mismatch")
        self.assertEqual(viewedPurchaseReport[2]["total_cost"],
                            purchasedProduct4["cost"],
                            "Total cost mismatch")

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

def add_purchased_product(db, purchaseTransactionId, productId, unitPrice, quantity, productUnitId, cost, discount=0):
    purchasedProduct = {
        "purchase_transaction_id": purchaseTransactionId,
        "product_id": productId,
        "unit_price": unitPrice,
        "quantity": quantity,
        "product_unit_id": productUnitId,
        "currency": "NGN",
        "cost": cost,
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

def add_purchase_transaction(db, vendorName):
    purchaseTransaction = {
        "vendor_name": vendorName,
        "user_id": 1
    }

    purchaseTransactionTable = db.schema.get_table("purchase_transaction")
    result = purchaseTransactionTable.insert("vendor_name",
                                            "user_id") \
                                    .values(tuple(purchaseTransaction.values())) \
                                    .execute()
    purchaseTransaction.update(DatabaseResult(result).fetch_one("purchase_transaction_id"))
    return purchaseTransaction

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

def view_purchase_report(db, fromDateTime, toDateTime):
    sqlResult = db.call_procedure("ViewPurchaseReport", (
                                    DatabaseDateTime(fromDateTime).iso_format,
                                    DatabaseDateTime(toDateTime).iso_format))

    return DatabaseResult(sqlResult).fetch_all()

if __name__ == '__main__':
    unittest.main()