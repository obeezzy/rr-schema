#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class AddCustomer(StoredProcedureTestCase):
    def test_add_customer(self):
        addedCustomer = add_customer(self.db)
        fetchedCustomer = fetch_customer(self.db)

        self.assertEqual(addedCustomer["customer_id"], fetchedCustomer["customer_id"], "Customer ID mismatch.")
        self.assertEqual(addedCustomer["client_id"], fetchedCustomer["client_id"], "Client ID mismatch.")
        self.assertEqual(addedCustomer["note_id"], fetchedCustomer["note_id"], "Note ID mismatch.")
        self.assertEqual(addedCustomer["user_id"], fetchedCustomer["user_id"], "User ID mismatch.")

def add_customer(db):
    customer = {
        "client_id": 1,
        "note_id": 1,
        "user_id": 1
    }

    db.call_procedure("AddCustomer",
                        tuple(customer.values()))
    result = {}
    for row in db:
        result = {
            "customer_id": row[0]
        }
    result.update(customer)
    return result

def fetch_customer(db):
    db.execute("""SELECT id AS customer_id,
                            client_id,
                            note_id,
                            user_id
                FROM customer""")
    result = {}
    for row in db:
        result = {
            "customer_id": row["customer_id"],
            "client_id": row["client_id"],
            "note_id": row["note_id"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
