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

def infer_languages_from_caption(caption: str) -> str:
    if not caption:
        return ""
    text = caption.lower()
    langs = set()
    for key, value in LANG_KEYWORDS.items():
        if key in text:
            langs.add(value)
    return ", ".join(sorted(langs))

@app.on_message(filters.channel)
async def queue_message(_, message):
    if not (message.video or message.document or message.audio):
        return
    message_queue.append(message)

async def process_queue():
    while True:
        if message_queue:
            msg = message_queue.pop(0)

            original_caption = msg.caption or ""
            languages = infer_languages_from_caption(original_caption)

            if languages:
                final_caption = CUSTOM_CAPTION.format(
                    file_caption=original_caption,
                    languages=languages
                )
            else:
                final_caption = CUSTOM_CAPTION.replace(
                    "\n<b>Audio : {languages}</b>", ""
                ).format(file_caption=original_caption)

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
