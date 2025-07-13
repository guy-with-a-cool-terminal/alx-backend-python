import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect("test.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            return results

async def async_fetch_older_users():
    async with aiosqlite.connect("test.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            return results

async def fetch_concurrently():
    all_users_task = async_fetch_users()
    older_users_task = async_fetch_older_users()

    all_users, older_users = await asyncio.gather(all_users_task, older_users_task)
    
    print("All Users:")
    for user in all_users:
        print(user)
    
    print("\nUsers older than 40:")
    for user in older_users:
        print(user)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())  