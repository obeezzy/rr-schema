import mysqlx
import os

config = {
    "user": os.environ["MYSQL_USER"],
    "password": os.environ["MYSQL_PASSWORD"],
    "host": "localhost",
    "port": 33060
}