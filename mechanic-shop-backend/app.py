import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "🔧 Mechanic Shop API is alive!"

if __name__ == "__main__":
    # Only needed if you run `python app.py`
    app.run(debug=True)
