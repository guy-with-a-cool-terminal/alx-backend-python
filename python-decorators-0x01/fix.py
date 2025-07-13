import sqlite3
import functools

# ✅ Simple in-memory cache
query_cache = {}

# ✅ Connection decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# ✅ Caching decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else '')
        if query in query_cache:
            print("[CACHE] Returning cached result.")
            return query_cache[query]
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# ✅ Run it
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# ✅ Second call (cached)
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
