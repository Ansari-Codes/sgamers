'''### ROUTES.py

This file defines routes for the application.
'''

# ROUTES
HOME = '/'
DOCS = '/docs'
DASHBOARD = '/dashboard'
LOGIN = '/login'
SIGNUP = '/signup'
LOGIN_RT = lambda rt='/': '/login' + f'?returnTo={rt}'
SIGNUP_RT = lambda rt='/': '/login' + f'?returnTo={rt}'
EXPLORE = '/explore'
PLAY_GAME = '/play/{game_id}'
PLAY_GAME_P = lambda game_id: f'/play/{game_id}'

# IMPORTS
from Pages.PageDashboard import create as create_dashboard
from Pages.PageDocs import create as create_docs
from Pages.PageExplore import create as create_explorer
from Pages.PageGameViewer import create as create_viewer
from Pages.PageHome import create as create_home
from Pages.PageLogin import create as create_login
from Pages.PageSignup import create as create_signup

# Route Defs


