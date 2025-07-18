# Filters only active users

def filter_active_users(users):
    return [user for user in users if user["active"]]
