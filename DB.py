import httpx
from ENV import API_URL,PASSWORD

q = 0

USERS = "users"
SESSIONS = "sessions"
GAMES = "games"
COMMENTS = "comments"
LIKES = "likes"
PLAYS = "plays"

tables = [USERS, SESSIONS, GAMES, COMMENTS, LIKES, PLAYS]
name = "games"

async def SQL(query: str, to_fetch: bool = False):
    global q
    payload = {"query": query, "to_fetch": to_fetch, "name": name, "password":PASSWORD, "purpose":"db"}
    q += 1
    print(f"DB: {q}: Running\n\t", query)
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(API_URL, json=payload)
            response.raise_for_status()
            res = response.json()
            if res.get("success"): return res.get("data", None)
            else: raise Exception(res.get("error"))
    finally: print(f"DB: {q}: Query ran!")

async def CLEAR():
    tables = await SQL("""
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%';
    """, to_fetch=True)
    for table in tables:
        await SQL(f"DELETE FROM `{table.get('name')}`;")

async def DROP():
    print("cli.py: Dropping tables...")
    drop = '\n'.join([
        f"DROP TABLE IF EXISTS {t};" for t in tables
    ])
    await SQL(drop)
    print("cli.py: All tables dropped successfully!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(DROP())