from DB import SQL, GAMES
from .helpers import isUnique, escapeSQL
from MODELS import Response
from typing import Literal

ALLOWED_IN_S = ['title', 'description', 'url', 'img_url']
NUM_COLS = ['id', 'owner', 'likes', 'plays']

async def getGames(
    owner: int,
    page=1,
    ppage=50,
    s_string="",
    s_in: None | list = None,
    order_by: Literal["updated_at", "created_at", "alphabets", "likes", "plays"] = "updated_at",
    asc: bool = False
):
    res = Response()

    query = "SELECT * FROM games"
    conditions = []

    # Always filter by owner
    conditions.append(f"owner = {owner}")

    # Search filters
    if s_string:
        esc = escapeSQL(s_string)
        like_clause = f"'%{esc}%'"

        if not s_in:
            s_in = ALLOWED_IN_S

        or_parts = []
        for col in s_in:
            if col in ALLOWED_IN_S:
                or_parts.append(f"{col} LIKE {like_clause}")

        if or_parts:
            conditions.append("(" + " OR ".join(or_parts) + ")")

    # WHERE clause
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # ORDER BY
    if order_by == "alphabets":
        query += " ORDER BY title"
    else:
        query += f" ORDER BY {order_by}"

    query += " ASC" if asc else " DESC"

    # --- Correct pagination ---
    offset = (page - 1) * ppage
    query += f" LIMIT {ppage} OFFSET {offset};"

    # Execute
    try:
        rows = await SQL(query, to_fetch=True)
        res.data = rows
    except Exception as e:
        res.errors["error"] = str(e)

    return res

async def addGame(
    owner: int,
    title: str,
    description: str,
    url: str,
    img_url: str
):
    res = Response()

    esc_title = escapeSQL(title)
    esc_desc = escapeSQL(description)
    esc_url = escapeSQL(url)
    esc_img = escapeSQL(img_url)

    query = f"""
        INSERT INTO games (owner, title, description, url, img_url)
        VALUES ({owner}, '{esc_title}', '{esc_desc}', '{esc_url}', '{esc_img}');
    """

    try:await SQL(query)
    except Exception as e:
        res.errors["error"] = str(e)
    return res
