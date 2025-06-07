from flask import Flask, render_template
from scraper import get_transfer_updates

app = Flask(__name__)

@app.route("/")
def index():
    updates = get_transfer_updates()
    return render_template("index.html", updates=updates)

if __name__ == "__main__":
    app.run(debug=True)
