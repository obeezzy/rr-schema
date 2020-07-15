#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

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

        self.assertEqual(addedUser["username"], fetchedUser["username"], "User name mismatch.")
        self.assertEqual(addedUser["first_name"], fetchedUser["first_name"], "First name field mismatch.")
        self.assertEqual(addedUser["last_name"], fetchedUser["last_name"], "Last name field mismatch.")
        self.assertEqual(addedUser["photo"], fetchedUser["photo"], "Photo mismatch.")
        self.assertEqual(addedUser["phone_number"], fetchedUser["phone_number"], "Phone number mismatch.")
        self.assertEqual(addedUser["email_address"], fetchedUser["email_address"], "Email address mismatch.")
        self.assertEqual(addedUser["note_id"], fetchedUser["note_id"], "Note ID mismatch.")
        self.assertEqual(addedUser["user_id"], fetchedUser["user_id"], "User ID mismatch.")

def add_user(db, user, firstName, lastName, photo, phoneNumber, emailAddress):
    user = {
        "username": user,
        "first_name": firstName,
        "last_name": lastName,
        "photo": photo,
        "phone_number": phoneNumber,
        "email_address": emailAddress,
        "note_id": 1,
        "user_id": 1
    }

    db.call_procedure("AddUser", tuple(user.values()))
    result = {}
    for row in db:
        result = {
            "user_id": row["user_id"]
        }
    result.update(user)
    return result

def fetch_user(db, userId):
    db.execute("""SELECT user_id,
                            username,
                            first_name,
                            last_name,
                            photo,
                            phone_number,
                            email_address,
                            note_id
                FROM rr_user
                WHERE username != 'admin'""")
    result = {}
    for row in db:
        return {
            "user_id": row["user_id"],
            "username": row["username"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "photo": row["photo"],
            "phone_number": row["phone_number"],
            "email_address": row["email_address"],
            "note_id": row["note_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
