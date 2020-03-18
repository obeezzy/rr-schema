#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class ArchiveStockProduct(StoredProcedureTestCase):
    def test_archive_stock_product(self):
        productCategory1 = add_product_category(db=self.db,
                                        category="Ben 10 aliens")
        productCategory2 = add_product_category(db=self.db,
                                        category="Spider-Man villians")
        product1 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Heatblast")
        product2 = add_product(db=self.db,
                                productCategoryId=productCategory2["product_category_id"],
                                product="Four-Arms")
        product3 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Kingpin")

        archive_stock_product(db=self.db,
                                archived=True,
                                productId=product2["product_id"])
        fetchedProductCategories = fetch_product_category(db=self.db,
                                                            archived=False)
        fetchedProducts = fetch_products(db=self.db,
                                            archived=False)

        self.assertEqual(len(fetchedProductCategories), 1, "Expected 1 category.")
        self.assertEqual(fetchedProductCategories[0]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(fetchedProductCategories[0]["category"],
                            productCategory1["category"], "Product category ID mismatch.")

        self.assertEqual(len(fetchedProducts), 2, "Expected 2 products.")
        self.assertEqual(fetchedProducts[0]["product_id"],
                            product1["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedProducts[0]["product"],
                            product1["product"],
                            "Product mismatch.")

        self.assertEqual(fetchedProducts[1]["product_id"],
                            product3["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedProducts[1]["product"],
                            product3["product"],
                            "Product mismatch.")

        archive_stock_product(db=self.db,
                                archived=False,
                                productId=product2["product_id"])
        fetchedProductCategories = fetch_product_category(db=self.db,
                                                            archived=False)
        fetchedProducts = fetch_products(db=self.db,
                                            archived=False)

        self.assertEqual(len(fetchedProductCategories), 2, "Expected 2 categories.")
        self.assertEqual(fetchedProductCategories[0]["product_category_id"],
                            productCategory1["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(fetchedProductCategories[0]["category"],
                            productCategory1["category"], "Product category mismatch.")
        self.assertEqual(fetchedProductCategories[1]["product_category_id"],
                            productCategory2["product_category_id"],
                            "Product category ID mismatch.")
        self.assertEqual(fetchedProductCategories[1]["category"],
                            productCategory2["category"], "Product category mismatch.")

        self.assertEqual(len(fetchedProducts), 3, "Expected 2 products.")
        self.assertEqual(fetchedProducts[0]["product_id"],
                            product1["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedProducts[0]["product"],
                            product1["product"],
                            "Product mismatch.")

        self.assertEqual(fetchedProducts[1]["product_id"],
                            product2["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedProducts[1]["product"],
                            product2["product"],
                            "Product mismatch.")

        self.assertEqual(fetchedProducts[2]["product_id"],
                            product3["product_id"],
                            "Product ID mismatch.")
        self.assertEqual(fetchedProducts[2]["product"],
                            product3["product"],
                            "Product mismatch.")

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

def archive_stock_product(db, archived, productId):
    args = {
        "archived": archived,
        "product_id": productId,
        "user_id": 1
    }
    sqlResult = db.call_procedure("ArchiveStockProduct", tuple(args.values()))
    return DatabaseResult(sqlResult).fetch_all()

def fetch_product_category(db, archived):
    productCategoryTable = db.schema.get_table("product_category")
    rowResult = productCategoryTable.select("id AS product_category_id",
                                            "category AS category") \
                                        .where("archived = :archived") \
                                        .bind("archived", archived) \
                                        .execute()
    return DatabaseResult(rowResult).fetch_all()

def fetch_products(db, archived):
    productTable = db.schema.get_table("product")
    rowResult = productTable.select("id AS product_id",
                                            "product_category_id AS product_category_id",
                                            "product AS product") \
                                            .where("archived = :archived") \
                                            .bind("archived", archived) \
                                            .execute()
    return DatabaseResult(rowResult).fetch_all()

if __name__ == '__main__':
    unittest.main()