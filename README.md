# 🤖 AutoCaption Bot

A simple Telegram bot that **automatically edits captions** of media sent in a channel.

---

## ✨ Features

- ✅ Cleans and formats media captions in Telegram channels  
- ✅ Removes unwanted spammy keywords and tags  
- ✅ Custom caption formatting (`{file_caption}`)  
- ✅ Simple message queue system  
- ✅ `/start`, `/help`, and `/status` commands  

---

## 🚀 Vps/Local Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/PrinceStarLord/AutoCaptionBot.git
```
```
cd autocaption-bot
```
2. Install Requirements
```bash
pip3 install -r requirements.txt
```
3. Edit a config.py File
#### config.py
### API_ID = "your_api_id"

### API_HASH = "your_api_hash"

### BOT_TOKEN = "your_bot_token"

### ADMIN = "admin_id"

### CUSTOM_CAPTION = "🎬 {file_caption}"

4. Run the Bot Locally
```bash
python3 main.py
```
---
## ☁️ Deploy to Koyeb
1. Create a New App on Koyeb
Choose "GitHub" as your deployment source

2. Paste your repo link into Public GitHub repository
3. Under Environment variables add all below Vars
```bash
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
ADMIN = "admin_id"
CUSTOM_CAPTION = "🎬 {file_caption}"
```
4. Under Builder - add this run command ```gunicorn app:app & python3 main.py```
5. Save & Deploy.

Customize the list in main.py under REMOVE_WORDS.

## 📦 Commands
/start – Greet the user
/help – Shows usage
/status – Shows queue messages (admin only)
