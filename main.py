import asyncio
import re
from pyrogram import Client, filters, idle
from pyrogram.errors import FloodWait, MessageNotModified
from config import API_ID, API_HASH, BOT_TOKEN, CUSTOM_CAPTION, ADMINS

app = Client(
    "autocaption-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

message_queue = []

LANG_KEYWORDS = {
    "hindi": "Hindi",
    "english": "English",
    "tamil": "Tamil",
    "telugu": "Telugu",
    "malayalam": "Malayalam",
    "kannada": "Kannada",
    "bengali": "Bengali",
    "marathi": "Marathi",
    "punjabi": "Punjabi",
    "gujarati": "Gujarati",
    "urdu": "Urdu",
    "korean": "Korean",
    "japanese": "Japanese",
    "chinese": "Chinese",
    "arabic": "Arabic",
    "spanish": "Spanish",
    "french": "French",
    "german": "German",
    "italian": "Italian",
    "portuguese": "Portuguese",
    "russian": "Russian",
    "thai": "Thai",
    "turkish": "Turkish",
    "indonesian": "Indonesian",
    "vietnamese": "Vietnamese"
}

REMOVE_WORDS = [
    "dual", "audio", "aac", "ddp", "hevc", "x265", "web", "dl",
    "esub", "subs", "sub", "amzn", "nf", "hdrip", "bluray",
    "join", "telegram", "t.me", "@m2links"
]

def infer_languages_from_caption(caption: str) -> str:
    if not caption:
        return ""
    text = caption.lower()
    langs = set()
    for key, value in LANG_KEYWORDS.items():
        if key in text:
            langs.add(value)
    return ", ".join(sorted(langs))

def clean_caption(caption: str) -> str:
    caption = re.sub(r'\b(mkv|mp4)\b', '', caption, flags=re.IGNORECASE)
    for word in REMOVE_WORDS:
        caption = re.sub(rf"\b{re.escape(word)}\b", "", caption, flags=re.IGNORECASE)
    caption = re.sub(r'[_\-\|\+\[\]\{\}~#$&]', ' ', caption)
    caption = caption.replace('.', ' ')
    return ' '.join(caption.split())

@app.on_message(filters.channel)
async def queue_message(_, message):
    if not (message.video or message.document):
        return
    message_queue.append(message)

async def process_queue():
    while True:
        if message_queue:
            msg = message_queue.pop(0)

            # 🔑 STEP 1: detect languages from ORIGINAL caption
            languages = infer_languages_from_caption(msg.caption or "")

            # 🔑 STEP 2: clean title separately
            cleaned_title = clean_caption(msg.caption or "")

            if languages:
                final_caption = CUSTOM_CAPTION.format(
                    file_caption=cleaned_title,
                    languages=languages
                )
            else:
                final_caption = CUSTOM_CAPTION.replace(
                    "\n<b>Audio : {languages}</b>", ""
                ).format(file_caption=cleaned_title)

            try:
                await app.edit_message_caption(
                    chat_id=msg.chat.id,
                    message_id=msg.id,
                    caption=final_caption
                )
            except MessageNotModified:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                message_queue.insert(0, msg)
            except Exception as e:
                print(f"[ERROR] {e}")

        await asyncio.sleep(1)

@app.on_message(filters.command("status") & filters.user(ADMINS))
async def status(_, message):
    await message.reply_text(f"📦 Messages in queue: {len(message_queue)}")

def main():
    async def runner():
        await app.start()
        asyncio.create_task(process_queue())
        await idle()
        await app.stop()
    app.run(runner())

if __name__ == "__main__":
    main()
