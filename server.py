from index import layout
from app import app
import sys

app.layout = layout
srv = app.server
app.title = "BlackDash"

if __name__ == "__main__":
    app.run_server(
        host='0.0.0.0',
        port=443,
        ssl_context=(
            "certs/fullchain.pem",
            "certs/privkey.pem"
        )
    )
