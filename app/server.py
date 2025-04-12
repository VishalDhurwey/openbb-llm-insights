from flask import Flask
from scheduler import run

app = Flask(__name__)

@app.route("/run", methods=["GET"])
def manual_trigger():
    run()
    return "✅ Pipeline ran successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
