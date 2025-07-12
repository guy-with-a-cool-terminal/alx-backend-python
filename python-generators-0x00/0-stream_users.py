import seed

# stream users one by one (generators challenge)
def stream_users():
    ''' yield user rows one by one as dictionaries '''
    conn = seed.connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")
    
    # yield rows one at a time
    for row in cursor:
        yield row
    cursor.close()
    conn.close()