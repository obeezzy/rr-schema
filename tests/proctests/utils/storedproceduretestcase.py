import unittest
import sys
import os
import logging
import sys
from datetime import datetime
import time
from .databaseclient import DatabaseClient

class StoredProcedureTestCase(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()
        self.logger = logging.getLogger(__name__)
        self.db = DatabaseClient()

    def tearDown(self):
        print(f"({round(self.elapsed, 2)}s)")

    @property
    def elapsed(self):
        return time.time() - self.startTime

if str(os.environ.get("LOGLEVEL", "warning")).lower() == "info":
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
elif str(os.environ.get("LOGLEVEL", "warning")).lower() == "debug":
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
else:
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.WARNING)