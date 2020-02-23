#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase

class ActivateUser(StoredProcedureTestCase):
    def test_activate_user(self):
        activate_user(self, True)

    def test_deactivate_user(self):
        activate_user(self, False)

def activate_user(self, active):
    pass

if __name__ == '__main__':
    unittest.main()