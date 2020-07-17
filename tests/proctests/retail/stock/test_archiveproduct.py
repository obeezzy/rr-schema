#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class ArchiveProduct(StoredProcedureTestCase):
    def test_archive_product(self):
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

        archive_product(db=self.db,
                                archived=True,
                                productId=product2["product_id"])
        fetchedProductCategories = fetch_product_categories(db=self.db,
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

        archive_product(db=self.db,
                                archived=False,
                                productId=product2["product_id"])
        fetchedProductCategories = fetch_product_categories(db=self.db,
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

        self.assertEqual(len(fetchedProducts), 3, "Expected 3 products.")
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

def archive_product(db, archived, productId):
    args = {
        "archived": archived,
        "product_id": productId,
        "user_id": 1
    }
    db.call_procedure("ArchiveProduct", tuple(args.values()))

def fetch_product_categories(db, archived):
    db.execute("""SELECT id AS product_category_id,
                                category
                FROM product_category
                WHERE archived = %s""", [archived])
    results = []
    for row in db:
        result = {
            "product_category_id": row["product_category_id"],
            "category": row["category"]
        }
        results.append(result)
    return results

def fetch_products(db, archived):
    db.execute("""SELECT id AS product_id,
                            product_category_id,
                            product
                FROM product
                WHERE archived = %s
                ORDER BY created""", [archived])
    results = []
    for row in db:
        result = {
            "product_id": row["product_id"],
            "product_category_id": row["product_category_id"],
            "product": row["product"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
