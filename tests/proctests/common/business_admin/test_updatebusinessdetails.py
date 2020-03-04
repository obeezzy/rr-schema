#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase, DatabaseResult

class UpdateBusinessDetails(StoredProcedureTestCase):
    def test_update_business_details(self):
        updatedBusinessDetails = update_business_details(self.db)
        fetchedBusinessDetails = fetch_business_details(self.db)

        self.assertEqual(updatedBusinessDetails, fetchedBusinessDetails, "Business details mismatch.")

def update_business_details(db):
    businessDetails = {
        "name": "Business name",
        "address": "Address",
        "business_family": "RETAIL",
        "establishment_year": 1959,
        "phone_number": "123456789",
        "logo": None,
        "extra_details": None
    }

    db.call_procedure("UpdateBusinessDetails",
                            tuple(businessDetails.values()))

    return businessDetails

def fetch_business_details(db):
    businessDetailsTable = db.schema.get_table("business_details")
    rowResult = businessDetailsTable.select("name",
                                            "address",
                                            "business_family",
                                            "establishment_year",
                                            "phone_number",
                                            "logo",
                                            "extra_details") \
                                        .execute()

    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()