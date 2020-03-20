#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseErrorCodes, StoredProcedureTestCase, DatabaseResult

class FetchUser(StoredProcedureTestCase):
    def test_fetch_user(self):
        addedUser = add_rr_user(db=self.db,
                                    user="superman2004",
                                    firstName="Christopher",
                                    lastName="Reeves",
                                    photo=None,
                                    phoneNumber="198389493",
                                    emailAddress="a@b.com")
        fetchedUser = fetch_user(db=self.db,
                                    userId=addedUser["user_id"])

        self.assertEqual(addedUser["user"], fetchedUser["user"], "User field mismatch.")
        self.assertEqual(addedUser["first_name"], fetchedUser["first_name"], "First name field mismatch.")
        self.assertEqual(addedUser["last_name"], fetchedUser["last_name"], "Last name field mismatch.")
        self.assertEqual(addedUser["photo"], fetchedUser["photo"], "Photo field mismatch.")
        self.assertEqual(addedUser["phone_number"], fetchedUser["phone_number"], "Phone number field mismatch.")
        self.assertEqual(addedUser["email_address"], fetchedUser["email_address"], "Email address field mismatch.")
        self.assertEqual(addedUser["user_id"], fetchedUser["user_id"], "User ID field mismatch.")

def add_rr_user(db, user, firstName, lastName, photo, phoneNumber, emailAddress):
    userDict = {
        "user": user,
        "first_name": firstName,
        "last_name": lastName,
        "photo": photo,
        "phone_number": phoneNumber,
        "email_address": emailAddress,
        "user_id": 1
    }

    rrUserTable = db.schema.get_table("rr_user")
    result = rrUserTable.insert("user",
                                "first_name",
                                "last_name",
                                "photo",
                                "phone_number",
                                "email_address",
                                "user_id") \
                            .values(tuple(userDict.values())) \
                            .execute()
    userDict.update(DatabaseResult(result).fetch_one("user_id"))
    return userDict

def fetch_user(db, userId, archived=False):
    sqlResult = db.call_procedure("FetchUser", (userId, archived))
    return DatabaseResult(sqlResult).fetch_one()

if __name__ == '__main__':
    unittest.main()