#!/usr/bin/env python3
import unittest
from testutils import DatabaseClient, StoredProcedureTestCase, MySqlError

class AddClient(StoredProcedureTestCase):
    def test_add_client(self):
        try:
            inputValues = add_client(self)
            storedValues = fetch_client(self)

            self.assertEqual(inputValues, storedValues, "Client table field mismatch.")
        except MySqlError as e:
            print(e)
        finally:
            self.client.cleanup()

    def test_add_two_clients(self):
        try:
            add_client(self)
            add_client(self)
        except MySqlError as e:
            print(e)
        finally:
            self.client.cleanup()

def add_client(self):
    iFirstName = "First name"
    iLastName = "Last name"
    iPreferredName = "Preferred name"
    iPhoneNumber = "1234567890"
    iAddress = "Address"
    iNoteId = None
    iUserId = 1

    self.client.call_procedure("AddClient", [
        iFirstName,
        iLastName,
        iPreferredName,
        iPhoneNumber,
        iAddress,
        iNoteId,
        iUserId
    ])

    return (iFirstName,
            iLastName,
            iPreferredName,
            iPhoneNumber,
            iAddress,
            iNoteId,
            iUserId)

def fetch_client(self):
    self.client.execute("SELECT first_name, \
                            last_name, \
                            preferred_name, \
                            phone_number, \
                            address, \
                            note_id, \
                            user_id \
                            FROM client")

    return self.client.fetchone()

if __name__ == '__main__':
    unittest.main()