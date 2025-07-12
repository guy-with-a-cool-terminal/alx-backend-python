''' Lazily paginate users using a generator '''
import seed

def paginate_users(page_size, offset):
    """Fetch a single page of users from the database"""
    conn = seed.connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s;", (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def lazy_pagination(page_size):
    """Generator that yields one page of users at a time"""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
