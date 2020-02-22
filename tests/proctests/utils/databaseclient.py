import mysql.connector
import os
from pathlib import Path
import re
from .config import config

class DatabaseClient(object):
    class ErrorCodes:
        USER_DEFINED_EXCEPTION = 1644
        DUPLICATE_ENTRY_ERROR = 1136
    DATABASE_NAME = "rr_test"
    INIT_SQL = Path(".").resolve().parent.joinpath("sql/mysql/common/init.sql")
    PROCEDURE_DIR = Path(".").resolve().parent.joinpath("sql/mysql/common/procedures")

    def __init__(self):
        self.__connectAsAdmin()
        self.__create_database()
        self.__create_procedures()
        self.__disconnect()
        self.__connect()

    def __del__(self):
        self.__disconnect()

    def __connectAsAdmin(self):
        self.testdb = mysql.connector.connect(**config)
        self.testcursor = self.testdb.cursor()

    def __connect(self):
        testConfig = dict(config)
        testConfig["database"] = DatabaseClient.DATABASE_NAME
        self.testdb = mysql.connector.connect(**testConfig)
        self.testcursor = self.testdb.cursor()

    def call_procedure(self, procedure, args):
        if not isinstance(procedure, str):
            raise TypeError("Argument 'procedure' must be of type 'string'.")
        if not isinstance(args, list):
            raise TypeError("Argument 'args' must be of type 'list'.")

        self.testcursor.callproc(procedure, args)
        results = [storedResult for storedResult in self.testcursor.stored_results()]
        if results is not None and len(results) > 0:
            return dict(zip(self.testcursor.description, results[0].fetchall()))

        return results

    def execute(self, query, insertValues=None):
        self.testcursor.execute(query, insertValues)
        results = self.testcursor.fetchone()
        if results is not None:
            return dict(zip(self.testcursor.column_names, results))

        return results

    def __create_database(self):
        self.testcursor.execute(f"CREATE DATABASE IF NOT EXISTS {DatabaseClient.DATABASE_NAME}")
        sqlStatements = re.split(";\n", DatabaseClient.INIT_SQL.read_text())
        for statement in sqlStatements:
            statement = statement.replace("###DATABASENAME###", DatabaseClient.DATABASE_NAME)
            if statement != "":
                statement = self.testcursor.execute(statement)

    def __create_procedures(self):
        sqlFiles = [child for child in DatabaseClient.PROCEDURE_DIR.iterdir() if str(child).endswith(".sql")]
        for file in sqlFiles:
            sqlData = file.read_text().replace("###DATABASENAME###", DatabaseClient.DATABASE_NAME)
            statements = sqlData.split("---")
            self.__execute_stored_procedure(statements)

    def __execute_stored_procedure(self, sqlStatements):
        for statement in sqlStatements:
            statement = statement.strip()
            statement = statement.replace("(\/\*(.|\n)*?\*\/|^--.*\n|\t|\n)", " ") # Remove tabs and spaces
            statement = statement.strip()
            self.execute(statement)
        
    def __drop_database(self):
        self.execute(f"DROP DATABASE IF EXISTS {DatabaseClient.DATABASE_NAME}")

    def create_user(self):
        pass

    def drop_user(self):
        pass

    def insert(self, table, args):
        pass

    def __disconnect(self):
        self.testcursor.close()
        self.testdb.close()

    def cleanup(self):
        self.__drop_database()
        self.__disconnect()