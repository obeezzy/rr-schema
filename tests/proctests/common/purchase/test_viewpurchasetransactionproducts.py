#!/usr/bin/env python3
import unittest
import locale
from proctests.utils import StoredProcedureTestCase

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
                                        costPrice=locale.currency(183.32),
                                        retailPrice=locale.currency(182.95))
        product2 = add_product(db=self.db,
                                productCategoryId=productCategory1["product_category_id"],
                                product="Guitar")
        productUnit2 = add_product_unit(db=self.db,
                                        productId=product1["product_id"],
                                        unit="unit(s)",
                                        costPrice=locale.currency(183.32),
                                        retailPrice=locale.currency(182.95))

        productCategory2 = add_product_category(db=self.db,
                                                category="Logitech")
        product3 = add_product(db=self.db,
                                productCategoryId=productCategory2["product_category_id"],
                                product="MX Master")
        productUnit3 = add_product_unit(db=self.db,
                                        productId=product1["product_id"],
                                        unit="unit(s)",
                                        costPrice=locale.currency(400.32),
                                        retailPrice=locale.currency(382.95))
        purchaseTransaction = add_purchase_transaction(self.db, vendorName="Carol Denvers")
        purchasedProduct1 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                                    productId=product1["product_id"],
                                                    unitPrice=locale.currency(89.66),
                                                    quantity=43.5,
                                                    productUnitId=productUnit1["product_unit_id"],
                                                    cost=locale.currency(459.34),
                                                    discount=locale.currency(96.38))
        purchasedProduct2 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                                    productId=product2["product_id"],
                                                    unitPrice=locale.currency(27.36),
                                                    quantity=54.5,
                                                    productUnitId=productUnit2["product_unit_id"],
                                                    cost=locale.currency(389.22),
                                                    discount=locale.currency(28.38))
        purchasedProduct3 = add_purchased_product(db=self.db,
                                                    purchaseTransactionId=purchaseTransaction["purchase_transaction_id"],
                                                    productId=product3["product_id"],
                                                    unitPrice=locale.currency(36.86),
                                                    quantity=64.5,
                                                    productUnitId=productUnit3["product_unit_id"],
                                                    cost=locale.currency(483.23),
                                                    discount=locale.currency(38.48))

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

def add_purchased_product(db, purchaseTransactionId, productId, unitPrice, quantity, productUnitId, cost, discount="$0"):
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

    db.execute("""INSERT INTO purchased_product (purchase_transaction_id,
                                                    product_id,
                                                    unit_price,
                                                    quantity,
                                                    product_unit_id,
                                                    currency,
                                                    cost,
                                                    discount,
                                                    user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS purchased_product_id,
                    purchase_transaction_id,
                    product_id,
                    unit_price,
                    quantity,
                    product_unit_id,
                    currency,
                    cost,
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

def add_purchase_transaction(db, vendorName, discount=0, suspended=False):
    purchaseTransaction = {
        "vendor_id": None,
        "vendor_name": vendorName,
        "discount": discount,
        "suspended": suspended,
        "user_id": 1
    }

    db.execute("""INSERT INTO purchase_transaction (vendor_id,
                                                    vendor_name,
                                                    discount,
                                                    suspended,
                                                    user_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id AS purchase_transaction_id,
                    vendor_id,
                    vendor_name,
                    discount,
                    suspended,
                    user_id""", tuple(purchaseTransaction.values()))
    result = {}
    for row in db:
        result = {
            "purchase_transaction_id": row["purchase_transaction_id"],
            "vendor_id": row["vendor_id"],
            "vendor_name": row["vendor_name"],
            "discount": row["discount"],
            "suspended": row["suspended"],
            "user_id": row["user_id"]
        }
    return result

def view_purchase_transaction_products(db, purchaseTransactionId, suspended=None, archived=None):
    args = {
        "purchase_transaction_id": purchaseTransactionId,
        "suspended": suspended,
        "archived": archived
    }
    db.call_procedure("ViewPurchaseTransactionProducts", tuple(args.values()))
    results = []
    for row in db:
        result = {
            "product_category_id": row["product_category_id"],
            "product_category": row["product_category"],
            "product_id": row["product_id"],
            "product": row["product"],
            "unit_price": row["unit_price"],
            "quantity": row["quantity"],
            "product_unit_id": row["product_unit_id"],
            "product_unit": row["product_unit"],
            "cost": row["cost"],
            "discount": row["discount"],
            "currency": row["currency"],
            "note_id": row["note_id"],
            "note": row["note"],
            "archived": row["archived"],
            "created": row["created"],
            "last_edited": row["last_edited"],
            "user_id": row["user_id"],
            "username": row["username"]
        }
        results.append(result)
    return results

if __name__ == '__main__':
    unittest.main()
