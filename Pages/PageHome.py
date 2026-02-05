from Comps import Complayout
from Database.session import getCurrentUser
from UI import Button, ui, Link

async def create(token):
    def addButtons():
        auth = res.success and res.data
        if not auth:
            with d:
                Button("LogIn", link="/login")
                Button("SignUp", link="/signup")
            with m:
                Button("LogIn", link="/login")
                Button("SignUp", link="/signup")
        else:
            with d: Button("Dashboard", link="/dashboard")
            with m: Button("Dashboard", link="/dashboard")
        d.update()
        m.update()
        with f:
            if auth:
                Link("Dashboard", "/dashboard")
            else:
                Link("LogIn", "/login")
                Link("SignUp", "/signup")
    await ui.context.client.connected()
    _,_, d, m = await Complayout.CompHeader()
    await Complayout.CompHero()
    f = await Complayout.CompFooter()
    res = await getCurrentUser(token)
    addButtons()