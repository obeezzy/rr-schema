#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class FetchUser(StoredProcedureTestCase):
    def test_fetch_user(self):
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
        self.assertEqual(addedUser["photo"], fetchedUser["photo"], "Photo field mismatch.")
        self.assertEqual(addedUser["phone_number"], fetchedUser["phone_number"], "Phone number field mismatch.")
        self.assertEqual(addedUser["email_address"], fetchedUser["email_address"], "Email address field mismatch.")
        self.assertEqual(addedUser["user_id"], fetchedUser["user_id"], "User ID field mismatch.")

def add_user(db, user, firstName, lastName, photo, phoneNumber, emailAddress):
    user = {
        "username": user,
        "first_name": firstName,
        "last_name": lastName,
        "photo": photo,
        "phone_number": phoneNumber,
        "email_address": emailAddress,
        "user_id": 1
    }

    db.execute("""INSERT INTO rr_user (username,
                                        first_name,
                                        last_name,
                                        photo,
                                        phone_number,
                                        email_address,
                                        user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id AS user_id,
                    username,
                    first_name,
                    last_name,
                    photo,
                    phone_number,
                    email_address""", tuple(user.values()))
    result = {}
    for row in db:
        result = {
            "user_id": row["user_id"],
            "username": row["username"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "photo": row["photo"],
            "phone_number": row["phone_number"],
            "email_address": row["email_address"]
        }
    return result

def fetch_user(db, userId, archived=False):
    db.call_procedure("FetchUser", [userId, archived])
    result = {}
    for row in db:
        result = {
            "user_id": row["user_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "username": row["username"],
            "photo": row["photo"],
            "phone_number": row["phone_number"],
            "email_address": row["email_address"],
            "active": row["active"],
            "note": row["note"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
