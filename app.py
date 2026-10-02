import base64
import hashlib
import hmac
import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from flask import Flask, abort, request

load_dotenv()

app = Flask(__name__)
CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]


def log_event(message: str) -> None:
    print(f"[{datetime.now().astimezone():%Y-%m-%d %H:%M:%S%z}] {message}", flush=True)


def valid_signature(body: bytes, signature: str) -> bool:
    digest = hmac.new(
        CHANNEL_SECRET.encode("utf-8"), body, hashlib.sha256
    ).digest()
    expected = base64.b64encode(digest).decode("utf-8")
    return hmac.compare_digest(expected, signature)


def reply(reply_token: str, text: str) -> None:
    response = requests.post(
        "https://api.line.me/v2/bot/message/reply",
        headers={
            "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        },
        json={
            "replyToken": reply_token,
            "messages": [{"type": "text", "text": text}],
        },
        timeout=10,
    )
    response.raise_for_status()


@app.post("/callback")
def callback():
    raw_body = request.get_data()
    signature = request.headers.get("X-Line-Signature", "")
    if not valid_signature(raw_body, signature):
        log_event("拒絕 Webhook：簽章驗證失敗")
        abort(400)

    events = (request.get_json(silent=True) or {}).get("events", [])
    if not events:
        log_event("收到 LINE Webhook 驗證請求，沒有訊息事件")
    for event in events:
        if event.get("type") != "message":
            log_event("略過非訊息事件")
            continue
        if event.get("message", {}).get("type") != "text":
            log_event("略過非文字訊息")
            continue
        log_event("收到文字訊息，正在回覆")
        try:
            reply(event["replyToken"], f"你說的是：{event['message']['text']}")
        except requests.RequestException:
            log_event("回覆 LINE API 失敗，請查看下方錯誤")
            raise
        log_event("已送出文字回覆")

    return "OK", 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    log_event(f"Bot 已啟動，等待 LINE Webhook（port {port}）")
    app.run(host="0.0.0.0", port=port)
