#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseErrorCodes, StoredProcedureTestCase, DatabaseResult

class FetchUserName(StoredProcedureTestCase):
    def test_fetch_user_name(self):
        addedUser = add_rr_user(db=self.db,
                                    user="superman2004",
                                    firstName="Christopher",
                                    lastName="Reeves",
                                    photo=None,
                                    phoneNumber="198389493",
                                    emailAddress="a@b.com")
        fetchedEmailAddress = fetch_user_name(db=self.db,
                                                    emailAddress=addedUser["email_address"])

        self.assertEqual(addedUser["user"], fetchedEmailAddress["user"], "User field mismatch.")
        self.assertEqual(addedUser["user_id"], fetchedEmailAddress["user_id"], "User ID field mismatch.")

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

def fetch_user_name(db, emailAddress):
    sqlResult = db.call_procedure("FetchUserName", (emailAddress,))
    return DatabaseResult(sqlResult).fetch_one()

if __name__ == '__main__':
    unittest.main()