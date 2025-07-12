import seed

# processing data in batches using generators
def stream_users_in_batches(batch_size):
    ''' yield user rows in batches of given size '''
    conn = seed.connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")
    
    # fetch rows in batches
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch
    cursor.close()
    conn.close()

# process each batch and filter users over 25
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if int(user['age']) > 25:
                print(user)