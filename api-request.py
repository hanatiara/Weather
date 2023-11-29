from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello"

@app.route("/get-data/<string:message>", methods=["GET"])
def send_request(message):
    data = [
        {
            "date" : time.time(),
            "message" : message
        }
    ]
    return jsonify({"data" : data})

if __name__ == "__main__":
    # with app.app_context():
    #     send_request("wwww")
    app.run()