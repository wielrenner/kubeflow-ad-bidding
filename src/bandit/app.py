import yaml
import os

from flask import Flask, jsonify, request
from redis import Redis

from .casino import Casino, BaseBandit


# state the bandit settings for the app
bandits = {
    "bandit0": BaseBandit({"a": 0.035, "b": 0.06, "c": 0.04}),
}

# open the config file for the app
with open('config.yml') as f:
    config = yaml.load(f)

# make the global state object for the app
redis = Redis(host=os.environ['redis-IP'], decode_responses=True)
casino = Casino(
    bandits=bandits,
    passwords=config["passwords"],
    start_amount=config["coins"],
    redis=redis,
)

app = Flask(__name__)
for u, p in config["passwords"].items():
    print(f"added user {u} with password {p}")


@app.route("/")
def index():
    return jsonify(
        {name: bandit.options for name, bandit in casino.bandits.items()}
    )


@app.route("/reset")
def reset():
    casino.reset()
    return "ok"


@app.route("/state", methods=["GET"])
def state():
    return jsonify(casino.state)


@app.route("/pull/<bandit>/<arm>", methods=["POST"])
def pull(bandit, arm):
    json_data = request.json
    password = json_data["password"]
    user = json_data["user"]
    response = casino.call(user, password, bandit, arm)
    app.logger.info(f"{user} pulled {bandit} with arm {arm}")
    return jsonify(response)


@app.route("/health")
def health():
    return "alive"


if __name__ == "__main__":
    app.run(debug=False, threaded=True, host="0.0.0.0")
