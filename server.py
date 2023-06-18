from index import layout
from app import app
import sys

try:
    if sys.argv[1] == "debug":
        print(f"arg {sys.argv[1]}")
        debug = True
    else:
        debug = False
except IndexError:
    debug = False

app.layout = layout
srv = app.server
app.title = "BlackDash"

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=debug)
