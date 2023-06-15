from index import layout
from app import app


app.layout = layout
srv = app.server
app.title = "BlackDash"

if __name__ == "__main__":
    app.run_server(host='0.0.0.0')
