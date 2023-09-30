from flask import Flask, Response, request, jsonify, send_from_directory
from creds import VERIFICATION_TOKEN

import tgbot, json, time, logging, asyncio
from tgbot import Update, BOT_TOKEN
from threading import Thread

logging.basicConfig(
    filename="logs.txt",
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


@app.route("/{}".format(BOT_TOKEN), methods=["POST"])
def handle_webhook():
    update = Update.from_array(request.json)
    tgbot.handle_update(update)
    return Response()


@app.route("/monthlyRewards")
def handle_monthly_rewards():
    total_users = tgbot.handle_monthly_rewards()
    return jsonify(ok=True, total=total_users)


async def listen_to_updates():
    offset = 0
    with open("info.json", "r") as f:
        info = json.load(f)
        offset = info["offset"]
        f.close()

    while True:
        try:
            updates = await tgbot.get_updates(offset=offset)
            if len(updates) > 0:
                print("Got {} updates".format(len(updates)))
                for update in updates:
                    asyncio.create_task(tgbot.handle_update(update))
                offset = updates[-1].update_id + 1
                with open("info.json", "w") as f:
                    json.dump({"offset": offset}, f)
                    f.close()

        except Exception as e:
            logging.error("Error while getting updates! {}".format(e))

        time.sleep(2)


if __name__ == "__main__":
    t = Thread(target=app.run, kwargs={"host": "0.0.0.0"})
    asyncio.run(listen_to_updates())
