from ENV import app, client
from fastapi.responses import Response
from fastapi.requests import Request
from uuid import uuid4
from DB import SQL, SESSIONS
from Database.dashboard import getUser
import time

async def saveCookie(value, userId, max_age):
    expires_at = (time.time() + max_age)
    try:
        query = f"""INSERT INTO {SESSIONS} (session_token, user, expires_at)
                    VALUES ('{value}', {userId}, {expires_at});"""
        res = await SQL(query)
        print("Query executed successfully:", query)
        print("Result:", res)
        return True
    except Exception as e:
        print("Error saving cookie:", str(e))
        return False

async def deleteCookie(value):
    try:
        query = f"""DELETE FROM {SESSIONS} WHERE session_token='{value}';"""
        res = await SQL(query)
        return True
    except Exception as e:
        return False

async def getCookie(token: str):
    try:
        res = await SQL(
            f"SELECT * FROM {SESSIONS} WHERE session_token='{token}';",
        )
        print("GetCookie: \n", res)
        if res and res[0]:
            expires_at = float(res[0]['expires_at'])
            if time.time() > expires_at:
                await SQL(f"DELETE FROM {SESSIONS} WHERE session_token='{token}';")
                return None, {}
            user = await getUser(res[0]['user'])
            if user.success:
                user = user.data
                return True, user[0]
            else:
                return False, {}
        return False, {}
    except Exception as e:
        return False, {"error": str(e)}

def getUserStorage() -> dict:
    response = client.get("/get/cookie")
    if response.status_code == 200:
        return response.json()
    return {}
def updateUserStorage(data: dict, clear=False) -> dict:
    user_id = data.get("id")
    if not user_id:
        raise ValueError("User ID is required to update storage.")
    response = client.post(f"/set/cookie/{user_id}")
    if response.status_code == 200:
        return {"success": True}
    return {"success": False, "error": response.text}
def clearUserStorage():updateUserStorage({},True)
def userID(): return getUserStorage().get("id")
def isAuth(): return getUserStorage().get("auth")
def getTabStorage()->dict:return app.storage.tab
def updateTabStorage(data: dict, clear=False)->dict:
    tab = getTabStorage()
    if clear:tab.clear()
    tab.update(data)
    return tab
