from flask import Flask, Response, request, jsonify, send_from_directory
import tgbot, logging

logging.basicConfig(
    # filename="logs.txt",
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s: %(message)s",
)

app = Flask(__name__)


@app.route("/")
def index():
    return "ok", 200


@app.route("/privacy_policy")
def privacy_policy():
    return send_from_directory("static", "privacy_policy.html")


@app.route("/webhook", methods=["POST"])
def handle_webhook():
    update = tgbot.Update.from_array(request.json)
    tgbot.handle_update(update)
    return Response()


@app.route("/monthlyRewards")
def handle_monthly_rewards():
    total_users = tgbot.handle_monthly_rewards()
    return jsonify(ok=True, total=total_users)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
