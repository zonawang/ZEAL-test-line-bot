# ZEAL 測試 Bot

這是使用 [ZEAL](https://github.com/stoday/ZEAL) 0.5.3 建立的 LINE Messaging API 回聲 Bot。已實際完成官方帳號建立、Webhook 驗證，並以 LINE 訊息確認回覆功能。

## 本機執行

需要 Python 3.11 以上。先依 `.env.example` 建立自己的 `.env`，填入該 LINE Channel 的 secret 和 access token，再執行：

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Bot 會在本機 8000 埠接收 `/callback` 的 Webhook。LINE 需要公開的 HTTPS 網址才能連到本機；啟動 ngrok 等轉送工具後，請將 LINE Developers Console 的 Webhook URL 更新為新的公開網址加上 `/callback`，按 Verify，並確認 Use webhook 已啟用。ngrok 免費方案的網址可能在重新啟動後改變。

`.env` 含憑證，已列入 `.gitignore`，請勿提交或分享。
