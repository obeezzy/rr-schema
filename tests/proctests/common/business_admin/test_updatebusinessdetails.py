#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase

class UpdateBusinessDetails(StoredProcedureTestCase):
    def test_update_business_details(self):
        try:
            updatedBusinessDetails = update_business_details(self)
            fetchedBusinessDetails = fetch_business_details(self)

            self.assertEqual(updatedBusinessDetails, fetchedBusinessDetails,
                            "Record mismatch for business details.")
        except:
            raise
        finally:
            self.db.cleanup()

def update_business_details(self):
    businessDetails = {
        "name": "Business name",
        "address": "Address",
        "business_family": "RETAIL",
        "establishment_year": 1959,
        "phone_number": "123456789",
        "logo": None,
        "extra_details": None
    }

    self.db.call_procedure("UpdateBusinessDetails",
                            list(businessDetails.values())
    )

    return businessDetails

def fetch_business_details(self):
    return self.db.execute("SELECT name, \
                            address, \
                            business_family, \
                            establishment_year, \
                            phone_number, \
                            logo, \
                            extra_details \
                            FROM business_details")

if __name__ == '__main__':
    unittest.main()