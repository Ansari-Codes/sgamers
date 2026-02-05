from UI import Label, Card, RawCol, RawRow, Html, Icon, Notify, ui, AddSpace, navigate
from Database.dashboard import getCounts, getGames, getGraph
from loading import showLoading
from plotly.graph_objects import Figure, Scatter
from MODELS import Response

async def dashboard(area, user_id, name):
    area.clear()
    loading = showLoading("Dashboard", True).classes("w-full h-full")
    pr = (await getCounts(user_id))
    p = pr.data
    games = p.get("games","N/A") or "0"
    likes = p.get("likes", "N/A") or "0"
    plays = p.get("plays", "N/A") or "0"
    if games not in ['N/A', '0']:
        latest = await getGames(user_id)
        gamess = await getGraph(user_id)
    else:
        latest = Response()
        latest.data = {}
        gamess = Response()
        gamess.data = [] # type:ignore
    errors = {**pr.errors, **latest.errors}
    if errors:
        for name, e in errors.items():
            Notify(str(name) + ": " + str(e), type='negative')
    try:
        Html(f"Hi, <span class='text-primary'>{name.title()}!</span>").classes("w-full text-5xl font-bold mb-2")
        with RawRow().classes("w-full p-2 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 xl:grid-cols-5 2xl:grid-cols-5 gap-2", remove='flex flex-row'):
            with Card().classes("h-fit"): 
                with RawCol().classes("w-full gap-1"):
                    Label(f"Total Games").classes("text-lg font-bold")
                    with RawRow().classes("w-full gap-1 text-secondary items-center"):
                        Icon("code", "lg");AddSpace()
                        Label(games).classes("text-4xl font-extrabold")
            with Card().classes("h-fit"):
                with RawCol().classes("w-full gap-1"):
                    Label(f"Total Likes").classes("text-lg font-bold")
                    with RawRow().classes("w-full gap-1 text-blue-500 dark:text-blue-400 items-center"):
                        Icon("thumb_up", "lg");AddSpace()
                        Label(likes).classes("text-4xl font-extrabold")
            with Card().classes("h-fit"):
                with RawCol().classes("w-full gap-1"):
                    Label(f"Times Played").classes("text-lg font-bold")
                    with RawRow().classes("w-full gap-1 text-red-500 items-center"):
                        Icon("gamepad", "lg");AddSpace()
                        Label(plays).classes("text-4xl font-extrabold")
        if latest.data:
            with RawRow().classes("w-full h-full"):
                with RawCol().classes("w-full sm:w-full md:w-[30%] gap-2 p-1"):
                    Label("Some latest games...").classes("text-lg font-semibold italic")
                    for game in latest.data:
                        with Card():
                            with RawRow().classes("w-full gap-1"):
                                Label(game.get("title","").title()).classes("text-lg font-semibold max-w-[50%] truncate")
                                AddSpace()
                                Icon("open_in_new", 'sm'
                                    ).classes("p-1 bg-primary rounded-sm cursor-pointer text-sm"
                                    ).on('click', lambda _,s=game.get("id"):(navigate(f"/game/{s}",True) if s else None))
                x_data = [p.get("title", "").title() for p in gamess.data]
                y_data = [p.get("likes", 0) for p in gamess.data]
                fig = Figure(
                    Scatter(
                        x=x_data,
                        y=y_data,
                        mode='lines+markers',
                        marker=dict(
                            size=8,
                            color="#2E8D36",
                            line=dict(width=1, color='white')
                        ),
                        line=dict(
                            width=3,
                            color="#2E8D36"
                        )
                    )
                )
                max_y = max(y_data) if y_data else 1
                fig.update_layout(
                    title="Likes per Game",
                    title_x=0.02,
                    margin=dict(l=0, r=0, t=40, b=0),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter, sans-serif", weight="bold", size=13, color="#2A2A2A"),
                    xaxis=dict(
                        showgrid=False,
                        zeroline=False,
                        showline=True,
                        linewidth=1,
                        linecolor="#D0D3DC",
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor="#E5E7EF",
                        zeroline=False,
                        showline=True,
                        linewidth=1,
                        linecolor="#D0D3DC",
                    ),
                    yaxis_range=[0, max_y+1],
                    hovermode="x unified",
                    autosize=True,
                )
                fig_dict = fig.to_dict()
                fig_dict['config'] = {
                    "displayModeBar": False,
                    "displaylogo": False,
                }
                ui.plotly(fig_dict).classes(
                    "w-full sm:w-[60%] h-96 bg-card-l dark:bg-card-d rounded-xl shadow-md p-4 mt-4 sm:ml-4"
                )
    except Exception as e:
        print(e)
        Label(f"Error Occured!").classes("text-2xl text-red p-2")
    loading.delete()