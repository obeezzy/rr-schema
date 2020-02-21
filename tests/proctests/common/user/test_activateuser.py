#!/usr/bin/env python3
import unittest
from proctests.utils import DatabaseClient, StoredProcedureTestCase, MySqlError

class ActivateUser(StoredProcedureTestCase):
    def test_activate_user(self):
        try:
            activate_user(self, True)
        except:
            raise
        finally:
            self.client.cleanup()

    def test_deactivate_user(self):
        try:
            activate_user(self, False)
        except:
            raise
        finally:
            self.client.cleanup()

def activate_user(self, active):
    pass

if __name__ == '__main__':
    unittest.main()