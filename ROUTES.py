'''### ROUTES.py

This file defines routes for the application.
'''

# ROUTES
HOME = '/'
DOCS = '/docs'
DASHBOARD = '/dashboard'
LOGIN = '/login'
SIGNUP = '/signup'
EXPLORE = '/explore'
PLAY_GAME = '/play/{game_id}'
LOGIN_RT = lambda rt='/': '/login' + f'?returnTo={rt}'
SIGNUP_RT = lambda rt='/': '/login' + f'?returnTo={rt}'
PLAY_GAME_P = lambda game_id: f'/play/{game_id}'

# IMPORTS
from Pages.PageDashboard import create as create_dashboard
from Pages.PageDocs import create as create_docs
from Pages.PageExplore import create as create_explorer
from Pages.PageGameViewer import create as create_viewer
from Pages.PageHome import create as create_home
from Pages.PageLogin import create as create_login
from Pages.PageSignup import create as create_signup
from UI import navigate, INIT_THEME
from ENV import ui
from fastapi import Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from SESSION import saveCookie, uuid4, deleteCookie
from Database.dashboard import getUser

# Route Defs

@ui.page(HOME)
async def cw(request: Request): 
    token = request.cookies.get("auth_token")
    INIT_THEME()
    await create_home(token)

@ui.page(EXPLORE)
async def cb(): 
    INIT_THEME()
    await create_explorer()

@ui.page(SIGNUP)
async def css(redirectTo: str = '/dashboard', request: Request = None, res: Response = None): #type:ignore
    INIT_THEME()
    if request:
        token = request.cookies.get("auth_token")
    else:
        token = None
    if not token : await create_signup(redirectTo,response=res) #type:ignore
    else: navigate(redirectTo)

@ui.page(LOGIN)
async def csl(redirectTo: str = '/dashboard', request: Request = None, res: Response = None): #type:ignore
    INIT_THEME()
    if request:
        token = request.cookies.get("auth_token")
    else:
        token = None
    if not token : await create_login(redirectTo,response=res) #type:ignore
    else: navigate(redirectTo)

AGE = 15 * 60 * 60 * 24
def addCookie(res, key, value):
    res.set_cookie(
        key=key,
        value=value,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
        max_age=AGE
    )

@ui.page("/set-cookie/{id}")
async def set_cookie(id: int, redirectTo: str = '/dashboard'):
    INIT_THEME()
    res = RedirectResponse(redirectTo)
    id = int(id)
    value = uuid4().__str__()
    try:
        await saveCookie(value, id, AGE)
        uesrname = await getUser(id)
        if uesrname.success:
            name = uesrname.data.get("name")
        else:
            raise Exception("Cannot fetch username...")
    except Exception as e:
        return HTMLResponse(f"<span style='color: red;font-size:100px;'>An error occured!</span><br><span style='color: gray;font-size:15px;'>{e}</span>")
    addCookie(res, "auth_token", value)
    addCookie(res, "user_id", str(id))
    addCookie(res, "user_name", str(name))
    return res

@ui.page("/clear-cookie")
async def del_cookie(request:Request):
    INIT_THEME()
    res = RedirectResponse('/')
    value = request.cookies.get("auth_token")
    if value is None: return res
    try:
        await deleteCookie(value)
    except Exception as e:
        return HTMLResponse(f"<span style='color: red;font-size:100px;'>An error occured!</span><br><span style='color: gray;font-size:15px;'>{e}</span>")
    res.delete_cookie("auth_token")
    res.delete_cookie("user_id")
    res.delete_cookie("user_name")
    return res

@ui.page(DASHBOARD)
async def cd(request: Request):
    INIT_THEME()
    token = request.cookies.get("auth_token")
    id = request.cookies.get("user_id")
    name = request.cookies.get("user_name")
    if token: await create_dashboard(id, name)
    else: navigate("/login?redirectTo=/dashboard")

@ui.page(DOCS)
async def cdc():
    INIT_THEME()
    await create_docs()

@ui.page(PLAY_GAME)
async def cpg(game_id: int):
    INIT_THEME()
    await create_viewer(game_id)
