#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseErrorCodes, StoredProcedureTestCase, DatabaseResult

class AddUser(StoredProcedureTestCase):
    def test_add_user(self):
        addedUser = add_user(db=self.db,
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
        self.assertEqual(addedUser["note_id"], fetchedUser["note_id"], "Note ID field mismatch.")
        self.assertEqual(addedUser["user_id"], fetchedUser["user_id"], "User ID field mismatch.")

def add_user(db, user, firstName, lastName, photo, phoneNumber, emailAddress):
    user = {
        "user": user,
        "first_name": firstName,
        "last_name": lastName,
        "photo": photo,
        "phone_number": phoneNumber,
        "email_address": emailAddress,
        "note_id": 1,
        "user_id": 1
    }

    sqlResult = db.call_procedure("AddUser",
                                    tuple(user.values())
    )

    user.update(DatabaseResult(sqlResult).fetch_one())
    return user

def fetch_user(db, userId):
    userTable = db.schema.get_table("rr_user")
    rowResult = userTable.select("user AS user",
                                    "first_name AS first_name",
                                    "last_name AS last_name",
                                    "photo AS photo",
                                    "phone_number AS phone_number",
                                    "email_address AS email_address",
                                    "note_id AS note_id",
                                    "id AS user_id") \
                            .where("id = :user_id") \
                            .bind("user_id", userId) \
                            .execute()
    return DatabaseResult(rowResult).fetch_one()

if __name__ == '__main__':
    unittest.main()