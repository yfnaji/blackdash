from index import layout
from app import app
from os.path import exists
import sys

debug = True if len(sys.argv) > 1 and sys.argv[1] == "--debug" else False

app.layout = layout
srv = app.server
app.title = "BlackDash"

ssl_paths = "certs/fullchain.pem", "certs/privkey.pem"
ssl_context = ssl_paths if all(exists(path) for path in ssl_paths) else None

if __name__ == "__main__":
    app.run_server(
        host='0.0.0.0',
        port=443,
        ssl_context=ssl_context,
        debug=debug
    )
