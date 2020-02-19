import mysql.connector
import os
from pathlib import Path
import re
from .config import config

class DatabaseClient(object):
    class ErrorCodes:
        USER_DEFINED_EXCEPTION = 1644
    DATABASE_NAME = "rr_test"
    INIT_SQL = Path(".").resolve().parent.joinpath("sql/mysql/common/init.sql")
    PROCEDURE_DIR = Path(".").resolve().parent.joinpath("sql/mysql/common/procedures")

    def __init__(self):
        self.__connect()
        self.__create_database()
        self.__create_procedures()

    def __del__(self):
        self.__disconnect()

    def __connect(self):
        self.testdb = mysql.connector.connect(**config)
        self.testcursor = self.testdb.cursor()

    def call_procedure(self, procedureName, args):
        if not isinstance(procedureName, str):
            raise TypeError("Argument 'procedureName' must be of type 'string'.")
        if not isinstance(args, list):
            raise TypeError("Argument 'args' must be of type 'list'.")

        self.testcursor.callproc(procedureName, args)

    def execute(self, query):
        self.testcursor.execute(query)

    def fetchone(self):
        return self.testcursor.fetchone()

    def fetchall(self):
        return self.testcursor.fetchall()

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
            self.testcursor.execute(statement)
        
    def __drop_database(self):
        self.testcursor.execute(f"DROP DATABASE IF EXISTS {DatabaseClient.DATABASE_NAME}")

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