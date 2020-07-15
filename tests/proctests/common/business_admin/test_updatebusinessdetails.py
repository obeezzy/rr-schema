#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class UpdateBusinessDetails(StoredProcedureTestCase):
    def test_update_business_details(self):
        updatedBusinessDetails = update_business_details(self.db)
        fetchedBusinessDetails = fetch_business_details(self.db)

        self.assertEqual(updatedBusinessDetails["name"], fetchedBusinessDetails["name"], "Name mismatch.")
        self.assertEqual(updatedBusinessDetails["address"], fetchedBusinessDetails["address"], "Address mismatch.")
        self.assertEqual(updatedBusinessDetails["business_family"], fetchedBusinessDetails["business_family"], "Business family mismatch.")
        self.assertEqual(updatedBusinessDetails["establishment_year"], fetchedBusinessDetails["establishment_year"], "Establishment year mismatch.")
        self.assertEqual(updatedBusinessDetails["phone_number"], fetchedBusinessDetails["phone_number"], "Phone number mismatch.")
        self.assertEqual(updatedBusinessDetails["logo"], fetchedBusinessDetails["logo"], "Logo mismatch.")
        self.assertEqual(updatedBusinessDetails["extra_details"], fetchedBusinessDetails["extra_details"], "Extra details mismatch.")

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
    db.execute("""SELECT name, 
                            address,
                            business_family,
                            establishment_year,
                            phone_number,
                            logo,
                            extra_details
                FROM business_details""")
    result = {}
    for row in db:
        result = {
            "name": row["name"],
            "address": row["address"],
            "business_family": row["business_family"],
            "establishment_year": row["establishment_year"],
            "phone_number": row["phone_number"],
            "logo": row["logo"],
            "extra_details": row["extra_details"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
