from UI import Label, Button, RawCol, RawRow, Row, Col, Card, ui, Image, Icon, delete, Input, AddSpace, Select, IconBtn, Notify
from Database.games import getGames, addGame
from loading import showLoading
from MODELS import Variable

def IconedLabel(icon, label, *, icon_config=None, label_config=None):
    label_config = label_config or {}
    icon_config = icon_config or {}
    with RawRow() as li:
        Icon(icon, **icon_config)
        Label(label, **label_config)
    return li

def LabeledInput(label, lbl_config:dict|None=None, inp_config:dict|None=None):
    with RawCol().classes("gap-1") as c:
        Label(label, **(lbl_config or {})).classes("w-full h-fit")
        inp = Input(**(inp_config or {})).classes("w-full h-fit")
    return c, inp

async def addgame(owner, title, url, img_url, desc):
    title = str(title).strip()
    url = str(url).strip()
    img_url = str(img_url).strip()
    desc = str(desc).strip()
    g = await addGame(owner, title, desc, url, img_url)
    return g

def add_game(dialog, game_area, user_id, updater=None):
    dialog.clear()
    async def add():
        title = inp_title.value
        url = inp_url.value
        img = inp_img.value
        des = inp_des.value
        if not url:
            Notify("URL of game is needed! It should be a github page...", type="negative", position="center")
            return
        g = await addgame(user_id, title, url, img, des)
        dialog.close()
        if g.success:
            ... # game(g.data).move(game_area, 0)
            if updater:await updater()
        else:
            for e,s in g.errors.items(): Notify(f"{e}: {s}", type='negative', positiion="bottom")
    with dialog.classes("w-fit h-fit"), Card().classes("w-[95vw] md:w-[60vw] lg:w-[50vw] h-[90vh] md:h-[80vh] lg:h-[70vh] overflow-x-hidden gap-1 p-2"):
        with RawRow().classes("w-full h-fit rounded-sm p-1 gap-2"):
            IconedLabel("add", "New Game").classes("text-xl w-fit")
            AddSpace()
            check_btn = IconBtn("check", add, config={"color":"positive"})
            IconBtn("close", dialog.close, config={"color":"negative"})
        with RawCol().classes("w-full p-1 gap-2"):
            _1, inp_title = LabeledInput("Game Title")
            _2, inp_url = LabeledInput("Game URL")
            _3, inp_img = LabeledInput("Thumbnail URL")
            _4, inp_des = LabeledInput("Description/README-URL")
            for _ in _1, _2, _3, _4:_.classes("w-full h-fit")

def gameDialog(data):
    pass

def game(data):
    title = data.get("title")
    description = data.get("description")
    created_at = data.get("created_at")
    updated_at = data.get("updated_at")
    img_url = data.get("img_url")
    url = data.get("url")
    likes = data.get("likes")
    plays = data.get("plays")
    id = data.get("id")
    with Card().classes("w-full h-full") as c, Col().classes("w-full h-full"):
        Label(title).classes("w-full font-semibold border-b-[1px]")
        Image(img_url).classes("w-[200px] aspect-square")
        with ui.element().classes("border-t-[1px] grd w-full h-fit grid grid-cols-3 gap-2 pt-1"):
            IconedLabel('favorite', str(likes)).tooltip(f"Total Likes: {likes}").classes("w-fit h-full")
            IconedLabel('games', str(plays)).tooltip(f"Total times Played: {plays}").classes("w-fit h-full")
            IconedLabel('update', str(updated_at)).tooltip(f"Last Update: {updated_at}").classes("w-fit h-full")
    return c

async def games(area,user_id):
    page = Variable(1) # type: ignore
    per_page = Variable(50) # type: ignore
    dialog = ui.dialog().props('persistent transition-show="slide-down" transition-hide="slide-down"')
    async def update_games_area(filters=None):
        for _ in __w: _.set_enabled(False)
        try:
            filters = filters or {}
            games_area.clear()
            loading = showLoading("Games", child=True)
            loading.move(games_area)
            user_games = await getGames(user_id, page=page.get(), ppage=per_page.get(), **filters) # type:ignore
            delete(loading)
            print(user_games)
            if user_games.success:
                with games_area:
                    if user_games.data: 
                        for gam in user_games.data: game(gam)
                    else: Label("No games yet!").classes("text-lg")
            else:
                with games_area:
                    for e,msg in user_games.errors.items():
                        Label(f"{e.title()}: {msg}").classes("text-lg font-semibold text-red-400")
        finally:
            for _ in __w: _.set_enabled(True)
    __w = []
    with RawRow().classes("w-full gap-1 sm:gap-2"):
        with RawRow().classes("w-full sm:w-fit"):
            async def search(s):
                page.set(1)
                await update_games_area({"s_string":s.value.__str__()})
            sq = Input().classes(
                "transition-all duration-300 ease-in-out "
                "w-[80%] "
                "sm:w-[200px] ",
            ).props("input-class='rounded-r-0'")
            sq_btn = Button(config=dict(icon="search"), on_click=lambda s=sq:search(s)).props("unelevated", remove="push").classes("rounded-l-0 w-[18%]")
        __w.extend([sq, sq_btn])
        def add():
            add_game(dialog, games_area, user_id, update_games_area)
            dialog.open()
        new = Button(config={"icon":"add"}, on_click=add)
        ref = Button(on_click=update_games_area, config={"icon":"refresh"})
        AddSpace()
        with RawRow().classes("w-fit h-fit gap-1 justify-center items-center"):
            Label("Per Page: ").classes("text-xl font-semibold")
            ppg = Select(value=per_page.value, options=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        async def pppg(p):
            per_page.value = int(p.value) if p.value and p.value > 10 else 10
            page.value = 1
            await update_games_area()
        ppg.on_value_change(pppg)
        __w.append(ref)
        __w.append(new)
        __w.append(ppg)
    games_area = RawCol().classes("w-full h-fit max-h-[78vh] mt-2 justify-center items-center grid grid-cols-5")
    await update_games_area()
