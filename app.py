from flask import Flask, send_from_directory

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True

@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def assets(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')
