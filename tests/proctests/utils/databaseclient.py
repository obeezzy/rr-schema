import mysqlx
from mysqlx.result import SqlResult, RowResult, Result
from pathlib import Path
import re
from datetime import datetime
from decimal import Decimal
import logging
import os

try:
    from .config import config
except ImportError:
    config = {
        "user": os.environ["MYSQL_USER"],
        "password": os.environ["MYSQL_PASSWORD"],
        "host": "localhost",
        "port": 33060,
        "ssl-mode": mysqlx.SSLMode.DISABLED
    }

class DatabaseErrorCodes:
    USER_DEFINED_EXCEPTION = 1644
    DUPLICATE_ENTRY_ERROR = 1136

class DatabaseClient(object):
    DATABASE_NAME = "rr_test"
    INIT_SQL = Path(".").resolve().parent.joinpath("sql/mysql/common/init.sql")
    PROCEDURE_DIR = Path(".").resolve().parent.joinpath("sql/mysql/common/procedures")

    def __init__(self):
        self.session = mysqlx.get_session(**config)
        self.__drop_database()
        self.__create_database()
        self.__create_procedures()

    def __del__(self):
        self.session.close()

    @property
    def schema(self):
        return self.session.get_schema(DatabaseClient.DATABASE_NAME)

    def call_procedure(self, procedure, args=()):
        if not isinstance(procedure, str):
            raise TypeError("Argument 'procedure' must be of type 'string'.")
        if not isinstance(args, tuple):
            raise TypeError("Argument 'args' must be of type 'tuple'.")

        argsAsString = ""
        for i, arg in enumerate(args):
            if arg is None:
                argsAsString += "NULL"
            elif isinstance(arg, datetime):
                argsAsString += arg.isoformat()
            elif isinstance(arg, bool):
                argsAsString += "TRUE" if arg else "FALSE"
            elif isinstance(arg, int):
                argsAsString += f"'{str(arg)}'"
            else:
                argsAsString += f"'{arg}'"
            if i < len(args) - 1:
                argsAsString += ", "

        effectiveProcedureCall = f"CALL {procedure}({argsAsString})"
        logging.debug(f"Effective procedure call: {effectiveProcedureCall}")
        sqlResult = self.session.sql(effectiveProcedureCall) \
                                .execute()
        return sqlResult

    def __create_database(self):
        self.session.sql(f"CREATE DATABASE IF NOT EXISTS {DatabaseClient.DATABASE_NAME}") \
            .execute()
        sqlStatements = re.split(";\n", DatabaseClient.INIT_SQL.read_text())
        for statement in sqlStatements:
            statement = statement.replace("###DATABASENAME###",
                                            DatabaseClient.DATABASE_NAME)
            if statement != "":
                self.session.sql(statement).execute()

    def __create_procedures(self):
        sqlFiles = [child for child in DatabaseClient.PROCEDURE_DIR.iterdir() if str(child).endswith(".sql")]
        for file in sqlFiles:
            sqlData = file.read_text().replace("###DATABASENAME###",
                                                DatabaseClient.DATABASE_NAME)
            statements = sqlData.split("---")
            self.__execute_stored_procedure(statements)

    def __execute_stored_procedure(self, sqlStatements):
        for statement in sqlStatements:
            statement = statement.strip()
            statement = statement.replace("(\/\*(.|\n)*?\*\/|^--.*\n|\t|\n)", " ") # Remove tabs and spaces
            statement = statement.strip()
            self.session.sql(statement).execute()
        
    def __drop_database(self):
        self.session.sql(f"DROP DATABASE IF EXISTS {DatabaseClient.DATABASE_NAME}") \
            .execute()

    def __drop_all_tables(self):
        tables = self.schema.get_tables()
        for table in tables:
            self.session.sql("DROP TABLE :table") \
                .bind(":table", table) \
                .execute()

class DatabaseResult(object):
    def __init__(self, result):
        self.sqlResult = None
        self.rowResult = None
        self.result = None
        if isinstance(result, SqlResult):
            self.sqlResult = result
        elif isinstance(result, RowResult):
            self.rowResult = result
        elif isinstance(result, Result):
            self.result = result
        else:
            raise TypeError("Argument 'result' must be of type 'SqlResult' or 'RowResult'.")

    def fetch_all(self):
        if self.sqlResult is not None:
            return self.__fetch_all_for_sql_result()
        elif self.rowResult is not None:
            return self.__fetch_all_for_row_result()
        elif self.result is not None:
            raise ValueError("Result objects only return one result. Call DatabaseResult.fetch_one().")
        else:
            raise ValueError("No result set.")

    def fetch_one(self, columnLabel=""):
        if self.sqlResult is not None:
            return self.__fetch_one_for_sql_result()
        elif self.rowResult is not None:
            return self.__fetch_one_for_row_result()
        elif self.result is not None:
            if columnLabel == "":
                raise ValueError("Column label must be set for results of type 'mysqlx.Result'.")
            return {columnLabel: self.result.get_autoincrement_value()}
        else:
            raise ValueError("No result set.")

    def __fetch_all_for_sql_result(self):
        rowsAsList = []
        if self.sqlResult.has_data():
            fetchedRows = self.sqlResult.fetch_all()
            for row in fetchedRows:
                rowAsDict = {}
                for column in self.sqlResult.columns:
                    if row is None:
                        rowAsDict[column.column_label] = None
                    elif isinstance(row[column.column_label], datetime):
                        rowAsDict[column.column_label] = DatabaseDateTime(row[column.column_label]).iso_format
                    elif isinstance(row[column.column_label], tuple): # Doubles return as tuples for some reason
                        rowAsDict[column.column_label] = row[column.column_label][0]
                    elif isinstance(row[column.column_label], Decimal): # Decimal to float
                        rowAsDict[column.column_label] = round(float(row[column.column_label]), 2)
                    else:
                        rowAsDict[column.column_label] = row[column.column_label]

                rowsAsList.append(rowAsDict)

        return rowsAsList

    def __fetch_all_for_row_result(self):
        rowsAsList = []
        fetchedRows = self.rowResult.fetch_all()
        for row in fetchedRows:
            rowAsDict = {}
            for column in self.rowResult.columns:
                if row is None:
                    rowAsDict[column.column_label] = None
                elif isinstance(row[column.column_label], datetime):
                    rowAsDict[column.column_label] = DatabaseDateTime(row[column.column_label]).iso_format
                elif isinstance(row[column.column_label], tuple): # Doubles return as tuples for some reason
                    rowAsDict[column.column_label] = row[column.column_label][0]
                elif isinstance(row[column.column_label], Decimal): # Decimal to float
                    rowAsDict[column.column_label] = round(float(row[column.column_label]), 2)
                else:
                    rowAsDict[column.column_label] = row[column.column_label]

            rowsAsList.append(rowAsDict)

        return rowsAsList

    def __fetch_one_for_sql_result(self):
        rowAsDict = {}
        if self.sqlResult.has_data():
            row = self.sqlResult.fetch_one()
            for column in self.sqlResult.columns:
                if row is None:
                    rowAsDict[column.column_label] = None
                elif isinstance(row[column.column_label], datetime):
                    rowAsDict[column.column_label] = DatabaseDateTime(row[column.column_label]).iso_format
                elif isinstance(row[column.column_label], tuple): # Doubles return as tuples for some reason
                    rowAsDict[column.column_label] = row[column.column_label][0]
                elif isinstance(row[column.column_label], Decimal): # Decimal to float
                    rowAsDict[column.column_label] = round(float(row[column.column_label]), 2)
                else:
                    rowAsDict[column.column_label] = row[column.column_label]

        return rowAsDict

    def __fetch_one_for_row_result(self):
        rowAsDict = {}
        row = self.rowResult.fetch_one()
        for column in self.rowResult.columns:
            if row is None:
                rowAsDict[column.column_label] = None
            elif isinstance(row[column.column_label], datetime):
                rowAsDict[column.column_label] = DatabaseDateTime(row[column.column_label]).iso_format
            elif isinstance(row[column.column_label], tuple): # Doubles return as tuples for some reason
                rowAsDict[column.column_label] = row[column.column_label][0]
            elif isinstance(row[column.column_label], Decimal): # Decimal to float
                rowAsDict[column.column_label] = round(float(row[column.column_label]), 2)
            else:
                rowAsDict[column.column_label] = row[column.column_label]

        return rowAsDict

class DatabaseDateTime(datetime):
    def __new__(cls, dt):
        if isinstance(dt, datetime):
            return super().__new__(cls, dt.year,
                                        dt.month,
                                        dt.day,
                                        dt.hour,
                                        dt.minute,
                                        dt.day)
        else:
            s1, s2 = dt.split(' ')
            v = map(int, s1.split('-') + s2.split(':'))
            return datetime.__new__(cls, *v)

    @staticmethod
    def from_iso_format(dateTimeString):
        return datetime.strptime(dateTimeString, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def to_iso_format(dateTime):
        return dateTime.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def iso_format(self):
        return DatabaseDateTime.to_iso_format(self)