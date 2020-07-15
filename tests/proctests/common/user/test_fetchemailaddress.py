#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

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
                                                    user=addedUser["username"])

        self.assertEqual(addedUser["email_address"], fetchedEmailAddress["email_address"], "Email address field mismatch.")
        self.assertEqual(addedUser["user_id"], fetchedEmailAddress["user_id"], "User ID field mismatch.")

def add_user(db, user, firstName, lastName, photo, phoneNumber, emailAddress):
    user = {
        "user": user,
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
            "username": row["username"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "photo": row["photo"],
            "phone_number": row["phone_number"],
            "email_address": row["email_address"],
            "user_id": row["user_id"]
        }
    return result

def fetch_email_address(db, user):
    db.call_procedure("FetchEmailAddress", [user])
    result = {}
    for row in db:
        result = {
            "user_id": row["user_id"],
            "email_address": row["email_address"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
