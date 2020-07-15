#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase
from psycopg2.extras import Json

class FetchUserByName(StoredProcedureTestCase):
    def test_fetch_user_by_name(self):
        addedUser = add_user(db=self.db,
                                    user="Spider-Man",
                                    firstName="Miles",
                                    lastName="Morales")
        addedUserPrivilege = add_user_privilege(db=self.db,
                                                userId=addedUser["user_id"],
                                                userPrivilege={
                                                    "type": "sales"
                                                })
        fetchedUser = fetch_user_by_name(db=self.db,
                                            user=addedUser["username"])

        self.assertEqual(addedUser["username"], fetchedUser["username"], "User mismatch.")
        self.assertEqual(addedUser["user_id"], fetchedUser["user_id"], "User ID mismatch.")

def add_user(db, user, firstName, lastName):
    user = {
        "username": user,
        "first_name": firstName,
        "last_name": lastName,
        "user_id": 1
    }

    db.execute("""INSERT INTO rr_user (username,
                                        first_name,
                                        last_name,
                                        user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id AS user_id,
                    username,
                    first_name,
                    last_name""", tuple(user.values()))
    result = {}
    for row in db:
        result = {
            "username": row["username"],
            "user_id": row["user_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"]
        }
    return result

def add_user_privilege(db, userId, userPrivilege):
    userPrivilege = {
        "user_id": userId,
        'user_privileges': Json(userPrivilege)
    }

    db.execute("""INSERT INTO user_privilege (user_id,
                                                privileges)
                VALUES (%s, %s)
                RETURNING user_id,
                    privileges""", tuple(userPrivilege.values()))
    result = {}
    for row in db:
        result = {
            "user_id": row["user_id"],
            "privileges": row["privileges"]
        }
    return result

def fetch_user_by_name(db, user):
    db.call_procedure("FetchUserByName", (user,))
    result = {}
    for row in db:
        result = {
            "username": row["username"],
            "user_id": row["user_id"]
        }
    return result

if __name__ == '__main__':
    unittest.main()
