# 🤖 AutoCaption Bot

A simple Telegram bot that **automatically edits captions** of media sent in a channel using [Pyrogram v2.x](https://docs.pyrogram.org/).

---

## ✨ Features

- ✅ Cleans and formats media captions in Telegram channels  
- ✅ Removes unwanted spammy keywords and tags  
- ✅ Custom caption formatting (`{file_caption}`)  
- ✅ Simple message queue system  
- ✅ `/start`, `/help`, and `/status` commands  

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/autocaption-bot.git
cd autocaption-bot
2. Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
3. Create a config.py File
python
Copy
Edit
# config.py
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
CUSTOM_CAPTION = "🎬 {file_caption}"
Get your API credentials from my.telegram.org

4. Run the Bot Locally
bash
Copy
Edit
python main.py
☁️ Deploy to Koyeb
1. Create a New App on Koyeb
Choose "GitHub" as your deployment source

Select your forked repo

Choose "Python" as the environment

Set the run command to:

bash
Copy
Edit
python main.py
2. Add Environment Variables on Koyeb
Instead of using config.py, you can modify your code to read from environment variables or use .env with python-dotenv.

Add these vars in Koyeb dashboard:

API_ID

API_HASH

BOT_TOKEN

CUSTOM_CAPTION

✅ Tip: Use os.environ.get("API_ID") etc. in your config.py to load these.

🛠 Deploy to Heroku (Optional)
Make sure you have a Procfile:

makefile
Copy
Edit
worker: python main.py
Then push to your Heroku app using Git or the Heroku CLI.

🧹 How Caption Cleaning Works
The bot removes keywords like:

text
Copy
Edit
"join", "t.me", "moviesmod", "mkvcinemas", "Bollywood", "movie", "Hollywood", etc.
And also removes unwanted characters like |, ~, [], etc.

Customize the list in main.py under REMOVE_WORDS.

📦 Commands
/start – Greet the user

/help – Shows usage

/status – Shows queue size (admin only)
