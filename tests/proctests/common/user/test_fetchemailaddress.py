#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseErrorCodes, StoredProcedureTestCase, DatabaseResult

class FetchEmailAddress(StoredProcedureTestCase):
    def test_fetch_email_address(self):
        addedUser = add_user(db=self.db,
                                user="superman2004",
                                firstName="Christopher",
                                lastName="Reeves",
                                photo=None,
                                phoneNumber="198389493",
                                emailAddress="a@b.com")
        fetchedEmailAddress = fetch_email_address(db=self.db,
                                                    user=addedUser["user"])

        self.assertEqual(addedUser["email_address"], fetchedEmailAddress["email_address"], "Email address field mismatch.")
        self.assertEqual(addedUser["user_id"], fetchedEmailAddress["user_id"], "User ID field mismatch.")

def add_user(db, user, firstName, lastName, photo, phoneNumber, emailAddress):
    userDict = {
        "user": user,
        "first_name": firstName,
        "last_name": lastName,
        "photo": photo,
        "phone_number": phoneNumber,
        "email_address": emailAddress,
        "user_id": 1
    }

    userTable = db.schema.get_table("rr_user")
    result = userTable.insert("user",
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

def fetch_email_address(db, user):
    sqlResult = db.call_procedure("FetchEmailAddress", (user,))
    return DatabaseResult(sqlResult).fetch_one()

if __name__ == '__main__':
    unittest.main()