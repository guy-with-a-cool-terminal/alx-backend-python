#!/usr/bin/python3
"""
Stream user ages using generator and calculate average
"""

import seed


def stream_user_ages():
    """
    Generator that yields one age at a time
    """
    conn = seed.connect_to_prodev()
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data;")
    
    for (age,) in cursor:
        yield int(age)

    cursor.close()
    conn.close()


def average_age():
    """
    Calculate average age using stream_user_ages generator
    """
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1

    if count > 0:
        print(f"Average age of users: {total / count:.2f}")
    else:
        print("No users found.")
