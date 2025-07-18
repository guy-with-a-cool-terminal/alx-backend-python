# Creates a simple report from the active users

def generate_report(active_users):
    names = [user["name"] for user in active_users]
    return f"Active Users: {', '.join(names)}"
