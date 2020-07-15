#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class UpdateAdminEmailAddress(StoredProcedureTestCase):
    def test_update_admin_email_address(self):
        addedUser = add_user(db=self.db,
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
        self.assertEqual(newEmailAddress, fetchedAdminUser["email_address"], "Email address mismatch.")
        self.assertEqual(addedUser["user_id"], fetchedAdminUser["user_id"], "User ID mismatch.")

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

def fetch_admin_user(db):
    db.execute("""SELECT id AS user_id,
                            email_address
                FROM rr_user""")
    result = {}
    for row in db:
        result = {
            "user_id": row["user_id"],
            "email_address": row["email_address"]
        }
    return result

def update_admin_email_address(db, emailAddress):
    db.call_procedure("UpdateAdminEmailAddress", [emailAddress])

if __name__ == '__main__':
    unittest.main()
