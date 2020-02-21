#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase

class UpdateBusinessDetails(StoredProcedureTestCase):
    def test_update_business_details(self):
        try:
            inputValues = update_business_details(self)
            storedValues = fetch_business_details(self)

            self.assertEqual(inputValues, storedValues, "Business details table field mismatch.")
        except:
            raise
        finally:
            self.client.cleanup()

def update_business_details(self):
    iName = "Business name"
    iAddress = "Address"
    iBusinessFamily = "RETAIL"
    iEstablishmentYear = 1959
    iPhoneNumber = "123456789"
    iLogo = None
    iExtraDetails = None

    self.client.call_procedure("UpdateBusinessDetails", [
        iName,
        iAddress,
        iBusinessFamily,
        iEstablishmentYear,
        iPhoneNumber,
        iLogo,
        iExtraDetails
    ])

    return (iName,
            iAddress,
            iBusinessFamily,
            iEstablishmentYear,
            iPhoneNumber,
            iLogo,
            iExtraDetails)

def fetch_business_details(self):
    self.client.execute("SELECT name, \
                            address, \
                            business_family, \
                            establishment_year, \
                            phone_number, \
                            logo, \
                            extra_details \
                            FROM business_details")

    return self.client.fetchone()

if __name__ == '__main__':
    unittest.main()