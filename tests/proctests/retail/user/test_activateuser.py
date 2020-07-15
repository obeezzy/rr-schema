#!/usr/bin/env python3
import unittest
from proctests.utils import StoredProcedureTestCase

class ActivateUser(StoredProcedureTestCase):
    def test_activate_user(self):
        activate_user(self.db, True)

    def test_deactivate_user(self):
        activate_user(self.db, False)

def activate_user(db, active=True):
    pass

if __name__ == '__main__':
    unittest.main()