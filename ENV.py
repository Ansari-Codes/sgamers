from dotenv import load_dotenv
import os
from nicegui import ui, app, events
from fastapi.testclient import TestClient

load_dotenv()  

API_URL = os.getenv("API_URL","").strip()
PASSWORD = os.getenv("PASSWORD","").strip()
if not (API_URL or PASSWORD):
    raise Exception("API_URL Or PASSWORD didn't load!")

RELOAD = True
HOST = '0.0.0.0'
PORT = int(os.environ.get("PORT", 8000))
SECRET = os.getenv("SECRET", "my-very=very!secret~token@though$you&can(*read::;")
client = TestClient(app, f"http://localhost:{PORT}")

NAME = "Sgamer"
ICON = "🎮"

THEME = {
    "primary": "#000000",  
    "secondary": "#505050",
    "accent": "#5400D1",   
    "dark": "#000000",     
    "positive": "#02A002", 
    "negative": "#A80000", 
    "info": "#017CBA",     
    "warning": "#FFB900",  
    "debug": "#6C757D",    
    "btn-l": "#9600DC",    
    "btn-d": "#420083",    
    "card-l": "#9F9F9F",   
    "card-d": "#383838",   
}