#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class ViewPurchaseTransactionProducts(StoredProcedureTestCase):
    def test_view_purchase_transaction_products(self):
        productCategory1 = add_product_category(db=self.db,
                                                category="Yamaha")
        product1 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Keyboard")
        productUnit1 = add_product_unit(db=self.db,
                                        productId=product1["product_id"],
                                        unit="unit(s)",
                                        baseUnitEquivalent=1,
                                        costPrice=183.32,
                                        retailPrice=182.95)
        product2 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Guitar")
        productUnit2 = add_product_unit(db=self.db,
                                        productId=product1["product_id"],
                                        unit="unit(s)",
                                        baseUnitEquivalent=1,
                                        costPrice=183.32,
                                        retailPrice=182.95)

        productCategory2 = add_product_category(db=self.db,
                                                category="Logitech")
        product3 = add_product(db=self.db,
                                productCategoryId=productCategory2["product_category_id"],
                                product="MX Master")
        productUnit3 = add_product_unit(db=self.db,
                                        productId=product1["product_id"],
                                        unit="unit(s)",
                                        baseUnitEquivalent=1,
                                        costPrice=400.32,
                                        retailPrice=382.95)
        purchaseTransaction = add_purchase_transaction(self.db, vendorName="Carol Denvers")
        purchasedProduct1 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                                    productId=product1["product_id"],
                                                    unitPrice=89.66,
                                                    quantity=43.5,
                                                    productUnitId=productUnit1["product_unit_id"],
                                                    cost=459.34,
                                                    discount=96.38)
        purchasedProduct2 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                                    productId=product2["product_id"],
                                                    unitPrice=27.36,
                                                    quantity=54.5,
                                                    productUnitId=productUnit2["product_unit_id"],
                                                    cost=389.22,
                                                    discount=28.38)
        purchasedProduct3 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                                    productId=product3["product_id"],
                                                    unitPrice=36.86,
                                                    quantity=64.5,
                                                    productUnitId=productUnit3["product_unit_id"],
                                                    cost=483.23,
                                                    discount=38.48)

        viewedPurchaseTransactionProducts = view_purchase_transaction_products(db=self.db,
                                                                                purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                                                                suspended=False,
                                                                                archived=False)

        self.assertEqual(len(viewedPurchaseTransactionProducts), 3, "Expected 3 transactions.")
        self.assertEqual(viewedPurchaseTransactionProducts[0]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[0]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[0]["product_id"],
                            product1["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[0]["product"],
                            product1["product"],
                            "Product mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[0]["unit_price"],
                            purchasedProduct1["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[0]["quantity"],
                            purchasedProduct1["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[0]["product_unit"],
                            productUnit1["unit"],
                            "Unit mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[0]["cost"],
                            purchasedProduct1["cost"],
                            "Cost mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[0]["discount"],
                            purchasedProduct1["discount"],
                            "Discount mismatch.")

        self.assertEqual(viewedPurchaseTransactionProducts[1]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[1]["product_category"],
                            productCategory1["category"],
                            "Product category mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[1]["product_id"],
                            product2["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[1]["product"],
                            product2["product"],
                            "Product mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[1]["unit_price"],
                            purchasedProduct2["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[1]["quantity"],
                            purchasedProduct2["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[1]["product_unit"],
                            productUnit2["unit"],
                            "Unit mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[1]["cost"],
                            purchasedProduct2["cost"],
                            "Cost mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[1]["discount"],
                            purchasedProduct2["discount"],
                            "Discount mismatch.")

        self.assertEqual(viewedPurchaseTransactionProducts[2]["product_category_id"],
                            productCategory2["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[2]["product_category"],
                            productCategory2["category"],
                            "Product category mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[2]["product_id"],
                            product3["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[2]["product"],
                            product3["product"],
                            "Product mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[2]["unit_price"],
                            purchasedProduct3["unit_price"],
                            "Unit price mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[2]["quantity"],
                            purchasedProduct3["quantity"],
                            "Quantity mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[2]["product_unit"],
                            productUnit3["unit"],
                            "Unit mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[2]["cost"],
                            purchasedProduct3["cost"],
                            "Cost mismatch.")
        self.assertEqual(viewedPurchaseTransactionProducts[2]["discount"],
                            purchasedProduct3["discount"],
                            "Discount mismatch.")

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

def add_product_unit(db, productId, unit, baseUnitEquivalent, costPrice, retailPrice):
    productUnit = {
        "product_id": productId,
        "unit": unit,
        "base_unit_equivalent": baseUnitEquivalent,
        "cost_price": costPrice,
        "retail_price": retailPrice,
        "currency": "NGN",
        "user_id": 1
    }

    productUnitTable = db.schema.get_table("product_unit")
    result = productUnitTable.insert("product_id",
                                        "unit",
                                        "base_unit_equivalent",
                                        "cost_price",
                                        "retail_price",
                                        "currency",
                                        "user_id") \
                                .values(tuple(productUnit.values())) \
                                .execute()
    productUnit.update(DatabaseResult(result).fetch_one("product_unit_id"))
    return productUnit

def add_purchase_transaction(db, vendorName, discount=0, suspended=False):
    purchaseTransaction = {
        "vendor_id": None,
        "vendor_name": vendorName,
        "discount": discount,
        "suspended": suspended,
        "user_id": 1
    }

    purchaseTransactionTable = db.schema.get_table("purchase_transaction")
    result = purchaseTransactionTable.insert("vendor_id",
                                                "vendor_name",
                                                "discount",
                                                "suspended",
                                                "user_id") \
                                        .values(tuple(purchaseTransaction.values())) \
                                        .execute()
    purchaseTransaction.update(DatabaseResult(result).fetch_one("purchase_transaction_id"))
    return purchaseTransaction

def view_purchase_transaction_products(db, purchaseTransactionId, suspended=None, archived=None):
    args = {
        "purchase_transaction_id": purchaseTransactionId,
        "suspended": suspended,
        "archived": archived
    }
    sqlResult = db.call_procedure("ViewPurchaseTransactionProducts", tuple(args.values()))
    return DatabaseResult(sqlResult).fetch_all()

if __name__ == '__main__':
    unittest.main()