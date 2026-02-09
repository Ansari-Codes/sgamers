from UI import Label, Button, RawCol, RawRow, Row, Col, Card, ui, Image, Icon, delete, Input, AddSpace, Select
from Database.games import getGames
from loading import showLoading
from MODELS import Variable

def IconedLabel(icon, label, *, icon_config=None, label_config=None):
    label_config = label_config or {}
    icon_config = icon_config or {}
    with RawRow().classes("w-fit h-full") as li:
        Icon(icon, **icon_config)
        Label(label, **label_config)
    return li

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
    with Card().classes("w-full h-full"), Col().classes("w-full h-full"):
        Label(title).classes("w-full font-semibold border-b-[1px]")
        Image(img_url).classes("w-[200px] aspect-square")
        with ui.element().classes("border-t-[1px] grd w-full h-fit grid grid-cols-3 gap-2 pt-1"):
            IconedLabel('favorite', str(likes)).tooltip(f"Total Likes: {likes}")
            IconedLabel('games', str(plays)).tooltip(f"Total times Played: {plays}")
            IconedLabel('update', str(updated_at)).tooltip(f"Last Update: {updated_at}")

async def games(area,user_id):
    page = Variable(1) # type: ignore
    per_page = Variable(50) # type: ignore
    async def update_games_area(filters=None):
        filters = filters or {}
        games_area.clear()
        loading = showLoading("Games", child=True)
        loading.move(games_area)
        user_games = await getGames(user_id, page=page.get(), ppage=per_page.get(), **filters) # type:ignore
        delete(loading)
        if user_games.success:
            with games_area:
                if user_games.data: 
                    for gam in user_games.data: game(gam)
                else: Label("No games yet!").classes("text-lg")
        else:
            for e,msg in user_games.errors.items():
                Label(f"{e.title()}: {msg}").classes("text-lg font-semibold text-red-400")
    __w = []
    with RawRow().classes("w-full gap-1 sm:gap-2"):
        with RawRow().classes("w-full sm:w-fit"):
            async def search(s):
                page.set(1)
                await update_games_area({"s_string":s.value.__str__()})
            sq = Input(on_change=search).classes(
                "transition-all duration-300 ease-in-out "
                "w-[80%] "
                "sm:w-[200px] ",
            ).props("input-class='rounded-r-0'")
            Button(config=dict(icon="search"), on_click=lambda s=sq:search(s)).props("unelevated", remove="push").classes("rounded-l-0 w-[18%]")
        new = Button(config={"icon":"add"})
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
    games_area = RawCol().classes("w-full h-fit max-h-[78vh] mt-2 justify-center items-center grid grid-cols-5")
    await update_games_area()
