#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class AddCustomer(StoredProcedureTestCase):
    def test_add_customer(self):
        addedCustomer = add_customer(self.db)
        fetchedCustomer = fetch_customer(self.db)

        self.assertEqual(addedCustomer, fetchedCustomer, "Customer mismatch.")

def add_customer(db):
    customer = {
        "client_id": 1,
        "note_id": 1,
        "user_id": 1
    }

    sqlResult = db.call_procedure("AddCustomer",
                                    tuple(customer.values()))
    customer.update(DatabaseResult(sqlResult).fetch_one())
    return customer

def fetch_customer(db):
    customerTable = db.schema.get_table("customer")
    rowResult = customerTable.select("id AS customer_id",
                                        "client_id AS client_id",
                                        "note_id AS note_id",
                                        "user_id AS user_id") \
                                .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()