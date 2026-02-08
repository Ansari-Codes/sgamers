import ROUTES, ENV, SESSION
ENV.ui.run(
    host=ENV.HOST, 
    port=ENV.PORT, 
    title=ENV.NAME, 
    favicon=ENV.ICON, 
    storage_secret=ENV.SECRET,
    # on_air=True,
    reload=ENV.RELOAD
)