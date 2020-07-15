import os

config = {
    "user": os.environ["POSTGRES_USER"],
    "password": os.environ["POSTGRES_PASSWORD"],
    "host": "localhost",
    "port": 5432,
    "database": "rr_test"
}
