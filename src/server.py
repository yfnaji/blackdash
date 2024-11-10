from index import layout
from app import app

app.layout = layout
app.title = "BlackDash"

srv = app.server

if __name__ == "__main__":
    app.run_server(
        host='0.0.0.0',
        port=8000
    )
