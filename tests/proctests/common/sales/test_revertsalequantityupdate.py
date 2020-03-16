#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class RevertSaleQuantityUpdate(StoredProcedureTestCase):
    def test_revert_sale_quantity_update(self):
        addedSaleTransaction = add_sale_transaction(db=self.db,
                                                        customerName="Tony Stark")
        addedProductCategory = add_product_category(db=self.db,
                                                    category="Suits")
        addedProduct = add_product(db=self.db,
                                    productCategoryId=addedProductCategory["product_category_id"],
                                    product="Iron Man suit")
        addedProductUnit = add_product_unit(db=self.db,
                                            productId=addedProduct["product_id"],
                                            unit="unit(s)",
                                            costPrice=283.18,
                                            retailPrice=844.23)
        addedProductQuantity = add_product_quantity(db=self.db,
                                                    productId=addedProduct["product_id"],
                                                    quantity=200.25)
        fetchedProductQuantity = fetch_current_product_quantity(db=self.db,
                                                                productId=addedProduct["product_id"])
        self.assertEqual(addedProductQuantity["quantity"], fetchedProductQuantity["quantity"], "Quantity mismatch.")

        addedSoldProduct = add_sold_product(db=self.db,
                                            saleTransactionId=addedSaleTransaction["sale_transaction_id"],
                                            productId=addedProduct["product_id"],
                                            productUnitId=addedProductUnit["product_unit_id"],
                                            unitPrice=389.23,
                                            quantity=88.32,
                                            cost=184.28,
                                            discount=101.32)
        alter_product_quantity(db=self.db,
                                productId=addedProduct["product_id"],
                                newQuantity=round(addedProductQuantity["quantity"] - addedSoldProduct["quantity"], 2))
        fetchedProductQuantity = fetch_current_product_quantity(db=self.db,
                                                                productId=addedProduct["product_id"])
        self.assertEqual(round(addedProductQuantity["quantity"] - addedSoldProduct["quantity"], 2),
                            fetchedProductQuantity["quantity"],
                            "Quantity mismatch.")

        revert_sale_quantity_update(db=self.db, 
                                        saleTransactionId=addedSaleTransaction["sale_transaction_id"])

        fetchedProductQuantity = fetch_current_product_quantity(db=self.db,
                                                                productId=addedProduct["product_id"])
        self.assertEqual(addedProductQuantity["quantity"],
                            fetchedProductQuantity["quantity"],
                            "Quantity mismatch.")

def add_sale_transaction(db, customerName, suspended=False):
    saleTransaction = {
        "customer_id": None,
        "customer_name": customerName,
        "suspended": suspended,
        "user_id": 1
    }

    saleTransactionTable = db.schema.get_table("sale_transaction")
    result = saleTransactionTable.insert("customer_id",
                                                "customer_name",
                                                "suspended",
                                                "user_id") \
                                        .values(tuple(saleTransaction.values())) \
                                        .execute()
    saleTransaction.update(DatabaseResult(result).fetch_one("sale_transaction_id"))
    return saleTransaction

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

def add_product_unit(db, productId, unit, costPrice, retailPrice, baseUnitEquivalent=1, preferred=True):
    productUnit = {
        "product_id": productId,
        "unit": unit,
        "cost_price": costPrice,
        "retail_price": retailPrice,
        "base_unit_equivalent": baseUnitEquivalent,
        "preferred": preferred,
        "currency": "NGN",
        "user_id": 1
    }

    productUnitTable = db.schema.get_table("product_unit")
    result = productUnitTable.insert("product_id",
                                        "unit",
                                        "cost_price",
                                        "retail_price",
                                        "base_unit_equivalent",
                                        "preferred",
                                        "currency",
                                        "user_id") \
                                .values(tuple(productUnit.values())) \
                                .execute()
    productUnit.update(DatabaseResult(result).fetch_one("product_unit_id"))
    return productUnit

def add_sold_product(db, saleTransactionId, productId, productUnitId, unitPrice, quantity, cost, discount=0):
    soldProduct = {
        "sale_transaction_id": saleTransactionId,
        "product_id": productId,
        "product_unit_id": productUnitId,
        "unit_price": 1038.39,
        "quantity": 183.25,
        "cost": 1832.28,
        "discount": 138.23,
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

def add_product_quantity(db, productId, quantity):
    productQuantity = {
        "product_id": productId,
        "quantity": quantity,
        "user_id": 1
    }

    currentProductQuantityTable = db.schema.get_table("current_product_quantity")
    result = currentProductQuantityTable.insert("product_id",
                                                "quantity",
                                                "user_id") \
                                        .values(tuple(productQuantity.values())) \
                                        .execute()
    productQuantity.update(DatabaseResult(result).fetch_one("current_product_quantity_id"))
    return productQuantity

def alter_product_quantity(db, productId, newQuantity):
    currentProductQuantityTable = db.schema.get_table("current_product_quantity")
    result = currentProductQuantityTable.update() \
                                        .set("quantity", newQuantity) \
                                        .where("product_id = :productId") \
                                        .bind("productId", productId) \
                                        .execute()

def revert_sale_quantity_update(db, saleTransactionId, userId=1):
    sqlResult = db.call_procedure("RevertSaleQuantityUpdate", (saleTransactionId, userId))
    return bool(DatabaseResult(sqlResult).fetch_one())

def fetch_current_product_quantity(db, productId):
    currentProductQuantityTable = db.schema.get_table("current_product_quantity")
    rowResult = currentProductQuantityTable.select("product_id AS product_id",
                                                    "quantity AS quantity",
                                                    "user_id AS user_id") \
                                            .where("product_id = :productId") \
                                            .bind("productId", productId) \
                                            .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()