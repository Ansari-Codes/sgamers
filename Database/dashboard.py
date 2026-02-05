from MODELS import Response
from .helpers import escapeSQL
from DB import USERS, GAMES, SQL

# Last 5 Games with likes, plays
# Total Games, Total Likes, Total Plays
# Graph: y = [likes, plays], x = [games]

async def getUser(item, by='id'):
    res = Response()
    try:
        itm = escapeSQL(f"{item}") if isinstance(item, str) else item
        resp = await SQL(f"SELECT * FROM {USERS} WHERE {by} = {itm}", True)
    except Exception as e:
        res.errors['user'] = str(e)
        return res
    res.data = resp[0] if resp else {}
    return res

async def getGames(owner, limit=5):
    res = Response()
    try:
        resp = await SQL(f"SELECT * FROM {GAMES} WHERE owner={owner} ORDER BY updated_at DESC LIMIT {limit};", to_fetch=True)
    except Exception as e:
        res.errors['games'] = str(e)
        return res
    res.data = resp
    return res

async def getCounts(item, by='owner'):
    res = Response()
    try:
        itm = escapeSQL(f"{item}") if isinstance(item, str) else item
        query = f"""
            SELECT 
                COUNT(*) AS total,
                SUM(likes) AS lks,
                SUM(plays) AS pls
            FROM {GAMES}
            WHERE {by} = {itm};
        """
        resp = await SQL(query, to_fetch=True)
    except Exception as e:
        res.errors['user'] = f"Cannot fetch data: {e}"
        return res
    if resp and len(resp) > 0:
        row = resp[0]
        res.data = {
            "games": row.get("total", 0),
            "likes": row.get("lks", 0),
            "plays": row.get("pls", 0),
        }
    else:
        res.data = {"games": 0, "likes": 0, "plays": 0}
    return res

async def getGraph(item: int | str | None, by="owner"):
    res = Response()
    if not item:
        res.errors['games'] = "No identifier provided!"
        return res
    value = item if isinstance(item, (float, int)) else escapeSQL(item)
    where_clause = f"{by} = {value}"
    query = f"SELECT * FROM {GAMES} WHERE {where_clause}"
    query += ";"
    try:
        games = await SQL(query, to_fetch=True)
    except Exception as e:
        res.errors['games'] = "Cannot fetch games!"
        print(e)
        return res
    res.data = games
    return res
