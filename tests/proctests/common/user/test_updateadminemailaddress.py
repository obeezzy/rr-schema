#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseErrorCodes, StoredProcedureTestCase, DatabaseResult

class UpdateAdminEmailAddress(StoredProcedureTestCase):
    def test_update_admin_email_address(self):
        addedUser = add_rr_user(db=self.db,
                                    user="superman2004",
                                    firstName="Christopher",
                                    lastName="Reeves",
                                    photo=None,
                                    phoneNumber="198389493",
                                    emailAddress="a@b.com")
        newEmailAddress = "b@a.com"
        update_admin_email_address(db=self.db,
                                    emailAddress=newEmailAddress)

        fetchedAdminUser = fetch_admin_user(db=self.db)
        self.assertEqual(newEmailAddress, fetchedAdminUser["email_address"], "User field mismatch.")
        self.assertEqual(1, fetchedAdminUser["user_id"], "User ID field mismatch.")

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

def fetch_admin_user(db):
    userTable = db.schema.get_table("rr_user")
    rowResult = userTable.select("id AS user_id",
                                    "email_address AS email_address") \
                .execute()
    return DatabaseResult(rowResult).fetch_one()

def update_admin_email_address(db, emailAddress):
    sqlResult = db.call_procedure("UpdateAdminEmailAddress", (emailAddress,))

if __name__ == '__main__':
    unittest.main()