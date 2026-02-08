from Comps import Complayout
from Database.session import getCurrentUser
from UI import Button, ui, Link, Notify, Label

async def create(token):
    def addButtons():
        auth = res.data
        if res.success:
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
        else:
            errs = res.errors
            for e in errs:
                Notify(str(res.errors[e]), position='bottom', type="negative", close_button=None, timeout=10000) # type:ignore
        d.update()
        m.update()
        with f:
            if res.success:
                if auth:
                    Link("Dashboard", "/dashboard")
                else:
                    Link("LogIn", "/login")
                    Link("SignUp", "/signup")
            else:
                Label("Error!")
    await ui.context.client.connected()
    _,_, d, m = await Complayout.CompHeader()
    await Complayout.CompHero()
    f = await Complayout.CompFooter()
    res = await getCurrentUser(token)
    addButtons()