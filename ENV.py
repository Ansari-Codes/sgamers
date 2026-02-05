from dotenv import load_dotenv
import os
from nicegui import ui, app, events, context
from fastapi.testclient import TestClient

load_dotenv()  

API_URL = os.getenv("API_URL","").strip()
PASSWORD = os.getenv("PASSWORD","").strip()
if not (API_URL or PASSWORD):
    raise Exception("API_URL Or PASSWORD didn't load!")

RELOAD = True
HOST = '0.0.0.0'
PORT = int(os.environ.get("PORT", 9000))
SECRET = os.getenv("SECRET", "my-very=very!secret~token@though$you&can(*read::;")
client = TestClient(app, f"http://localhost:{PORT}")

NAME = "Sgamer"
ICON = "🎮"
