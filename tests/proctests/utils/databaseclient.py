import psycopg2
import psycopg2.extras
from pathlib import Path
import re
from datetime import datetime
import logging
import locale

from .config import config

class DatabaseClient(object):
    INIT_SQL = Path(".").resolve().parent.joinpath("sql/common/init.sql")
    PROCEDURE_DIR = Path(".").resolve().parent.joinpath("sql/common/procedures")

    def __init__(self):
        self._conn = None
        self._cursor = None
        self._open_connection("postgres")
        self._drop_database(config["database"])
        self._create_database(config["database"])
        self._close_connection()
        self._open_connection(config["database"])
        self._init_database()
        self._create_procedures()

    def __del__(self):
        if self._conn is not None:
            self._conn.close()

    def __iter__(self):
        return iter(self._cursor)

    @property
    def lastrowid(self):
        return self._cursor.lastrowid

    @property
    def currency_symbol(self):
        return locale.currency(0.0)[0]

    def call_procedure(self, procedure, args=()):
        effectiveProcedureCall = f"SELECT {procedure}({args})"
        logging.debug(f"Effective procedure call: {effectiveProcedureCall}")
        self._cursor.callproc(procedure, args)

    def execute(self, sql, values=None):
        if values is not None:
            self._cursor.execute(sql, values)
        else:
            self._cursor.execute(sql)

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def commit(self):
        self._conn.commit()

    def _open_connection(self, database):
        cfg = dict(config)
        cfg["database"] = database
        self._conn = psycopg2.connect(**cfg)
        self._conn.autocommit = True
        self._cursor = self._conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    def _close_connection(self):
        self._conn.close()

    def _create_database(self, database):
        self.execute(f"CREATE DATABASE {database}")

    def _init_database(self):
        sqlStatements = re.split(";\n", DatabaseClient.INIT_SQL.read_text())
        for statement in sqlStatements:
            if statement != "":
                self.execute(statement)

    def _create_procedures(self):
        sqlFiles = [child for child in DatabaseClient.PROCEDURE_DIR.iterdir() if str(child).endswith(".sql")]
        for file in sqlFiles:
            sqlData = file.read_text()
            statements = sqlData.split("---")
            self._execute_stored_procedure(statements)

    def _execute_stored_procedure(self, sqlStatements):
        for statement in sqlStatements:
            statement = statement.strip()
            statement = statement.replace(r"(\/\*(.|\n)*?\*\/|^--.*\n|\t|\n)", " ") # Remove tabs and spaces
            statement = statement.strip()
            self._cursor.execute(statement)
        
    def _drop_database(self, database):
        self.execute(f"DROP DATABASE IF EXISTS {database}")
