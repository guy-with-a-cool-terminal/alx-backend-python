#!/usr/bin/python3
"""
Master script to run project parts by argument:
  0 = setup DB (seed.py)
  1 = stream_users()
  2 = batch_processing()
  3 = lazy_pagination()
  4 = average_age()
"""

import sys
import importlib.util
from itertools import islice


def import_from(filename, func_name):
    """
    Dynamically import a function from a file
    (e.g. import_from('0-stream_users.py', 'stream_users'))
    """
    spec = importlib.util.spec_from_file_location("mod", filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, func_name)


def run_seed():
    import seed
    connection = seed.connect_db()
    if connection:
        seed.create_database()
        connection.close()
        print("✅ DB connection successful, database created")

        connection = seed.connect_to_prodev()
        if connection:
            seed.create_table()
            seed.insert_data('user_data.csv')

            cursor = connection.cursor()
            cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
            if cursor.fetchone():
                print("✅ Database ALX_prodev is present")

            cursor.execute("SELECT * FROM user_data LIMIT 5;")
            for row in cursor.fetchall():
                print(row)

            cursor.close()
            connection.close()


def run_stream_users():
    stream_users = import_from("0-stream_users.py", "stream_users")
    for user in islice(stream_users(), 6):
        print(user)


def run_batch_processing():
    batch_processing = import_from("1-batch_processing.py", "batch_processing")
    try:
        batch_processing(50)
    except BrokenPipeError:
        sys.stderr.close()


def run_lazy_pagination():
    lazy_pagination = import_from("2-lazy_paginate.py", "lazy_pagination")
    try:
        for page in lazy_pagination(100):
            for user in page:
                print(user)
    except BrokenPipeError:
        sys.stderr.close()


def run_average_age():
    average_age = import_from("4-stream_ages.py", "average_age")
    average_age()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py [0-4]")
        sys.exit(1)

    option = sys.argv[1]

    match option:
        case '0':
            run_seed()
        case '1':
            run_stream_users()
        case '2':
            run_batch_processing()
        case '3':
            run_lazy_pagination()
        case '4':
            run_average_age()
        case _:
            print("❌ Invalid option. Use 0 to 4.")
