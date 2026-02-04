from DB import SQL, USERS
from MODELS import Response
from .helpers import escapeSQL

async def getUser(item, by='id'):
    res = Response()
    try:
        itm = escapeSQL(f"{item}") if isinstance(item, str) else item
        resp = await SQL(f"SELECT * FROM {USERS} WHERE {by} = {itm}", True)
    except Exception as e:
        res.errors['user'] = e
        return res
    res.data = resp[0] if resp else {}
    return res
