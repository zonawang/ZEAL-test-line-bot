# ZEAL 測試 Bot｜一次從建立帳號到收到回覆的實測紀錄

stoday 告訴我 [ZEAL](https://github.com/stoday/ZEAL) 是受到我分享咖啡廳 Bot 的經驗啟發時，我很開心，也想親自把整個設定流程走一遍。這個 repo 放的是那次測試產生的 Flask 回聲 Bot，並記下實際結果和遇到的卡點，方便作者對照。

> 這是一次性的本機測試紀錄，不是持續運作的線上服務。測試結束後，Bot 和 ngrok 都已停止。

## 測試範圍

| 項目 | 本次使用方式 |
| --- | --- |
| 日期 | 2026-10-02 |
| ZEAL | 0.5.3，從 GitHub 原始碼 checkout（`37d654a`）安裝；未另外驗證 PyPI 發行包 |
| 環境 | macOS Apple Silicon、Python 3.12、ngrok 3.39.11 |
| 帳號 | 新建立的測試 LINE 官方帳號 |
| 連線 | ngrok 公開 HTTPS 網址，轉送到本機 8000 埠 |
| Bot | ZEAL 產生的 Flask 回聲 Bot，接收 `POST /callback` |

測試目標是走完「建立官方帳號 → 取得 Messaging API 憑證 → 設定並驗證 Webhook → 用手機傳訊息收到回覆」。我沒有測試長時間運作、部署到雲端，或重開電腦後自動恢復服務。

## 實際操作與結果

1. 執行 ZEAL 的 `line-bot setup`，選擇 ngrok 與「建立新的官方帳號」，填入測試帳號資料和 LINE 業種分類。LINE 要求 CAPTCHA 時，由我在 ZEAL 開啟的瀏覽器完成人類驗證。
2. ZEAL 確認測試官方帳號，接續 Messaging API 設定。這一步遇到頁面辨識問題，處理方式記在下方。
3. ZEAL 讀取 Channel 憑證並寫入本機 `.env`，終端沒有印出密鑰。產生的專案包含 `app.py`、`requirements.txt`、`.env.example` 與 `.gitignore`。
4. ZEAL 建立 ngrok 公開網址、啟動本機 Bot，LINE 的 Webhook Verify 成功；`Use webhook` 也確認啟用。預設自動回覆已關閉，避免和測試 Bot 同時回覆。
5. 我用手機加入測試官方帳號，傳送「測試」，實際收到「你說的是：測試」。這是本次端到端測試的確認結果。

設定時，LINE Console 的 Webhook 開關沒有立即回報成功；ZEAL 自動改由 LINE Official Account Manager 啟用並重新確認。這個接續流程最後有成功，不需要從頭再做一次。

## 這次遇到的兩個卡點

### 重跑時再次詢問 ngrok Authtoken

第一次設定 ngrok 後，我中斷並重跑 `setup`。雖然 ngrok 設定檔中已有 Authtoken、`ngrok config check` 也通過，ZEAL 還是再次要求輸入。我重新輸入後可以繼續。這是這次環境中的觀察；希望之後重跑時能直接沿用已存在的設定。

### Messaging API 已有 Channel，但 ZEAL 找不到啟用按鈕

建立帳號後，ZEAL 一度顯示找不到「Enable Messaging API」。我切到瀏覽器的 Messaging API 頁面，已經看得到 Channel ID 和 Channel secret；回到終端選「在目前瀏覽器手動處理後重新辨識」後，ZEAL 判定 Channel 已啟用並順利往下走。這個恢復選項很有用，也提供了一個可檢查的頁面辨識情境。

## Repo 裡有什麼

| 檔案 | 用途 |
| --- | --- |
| `app.py` | ZEAL 產生的 Flask Bot；驗證 LINE 簽章，對文字訊息回覆「你說的是：…」 |
| `requirements.txt` | Bot 執行所需的 Python 套件 |
| `.env.example` | 需要設定的環境變數範例，只有佔位值 |
| `.gitignore` | 排除 `.env`、虛擬環境和 Python 快取 |

ZEAL 原本將專案產生在 `line-bot-<帳號名稱>/`；為了讓這個測試 repo 打開就看得到 Bot，我在測試結束後把產生的檔案移到 repo 根目錄。Bot 程式本身沒有修改。

## 在本機重新執行

需要 Python 3.11 以上、這個 Channel 的憑證，以及能轉送到本機 8000 埠的公開 HTTPS 網址。先複製 `.env.example` 成 `.env`，填入自己的 `LINE_CHANNEL_SECRET` 和 `LINE_CHANNEL_ACCESS_TOKEN`。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

事先在本機設定好 ngrok Authtoken，再於另一個終端啟動 ngrok：

```bash
ngrok http 8000
```

把 LINE Developers Console 的 Webhook URL 更新為 ngrok 顯示的 HTTPS 網址加上 `/callback`，按 Verify，並確認 `Use webhook` 已啟用。ngrok 免費網址可能在重啟後改變；這次測試使用的網址已停止服務。

`.env`、LINE 登入資料與 ngrok Authtoken 都沒有提交到此 repo。請勿把真實憑證加入 Git。
