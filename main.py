from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageNotModified
import asyncio
from pyrogram import idle
import re
from config import API_ID, API_HASH, BOT_TOKEN, CUSTOM_CAPTION

app = Client(
    session_name=None,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

message_queue = []

REMOVE_WORDS = [
    'R∆G∆ ', 'join', 'psa', 'https', 'http', 'Full Bollywood Movie', 'Bollywood', 'ViSTA', 'MoviesMod',
    '(Mᴏᴏɴ Kɴɪɢʜᴛ)', 'L3G3N7', 'telegram', 'm2links', "join us", "Join Us", "t.me", "mkvcinemas", "movies",
    "moviesmod", "moviesflix", "Desiremovies", "mkvc", "cinevood", "@m2links", "skymovieshd", "(dedsincebirth)","Full", "movie","MoviesUP","Hollywood"
]

def clean_caption(caption: str) -> str:
    match = re.search(r"(.*?\b(?:mkv|mp4)\b)", caption, re.IGNORECASE)
    if match:
        caption = match.group(1)
    else:
        match = re.search(r"(.*?\b(?:esub|esubs|msub|msubs)\b)", caption, re.IGNORECASE)
        if match:
            caption = match.group(1)
    caption = re.sub(r'\b(mkv|mp4)\b', '', caption, flags=re.IGNORECASE)
    for word in REMOVE_WORDS:
        caption = re.sub(re.escape(word), '', caption, flags=re.IGNORECASE)
    caption = re.sub(r'[_\-\|\+\[\]\{\}~#$]', ' ', caption)
    caption = caption.replace('.', ' ')
    return ' '.join(caption.split())

@app.on_message(filters.private & filters.command(["start"]))
async def start_command(_, message):
    await message.reply_text(f"<b>Hello {message.from_user.mention},</b>\n\n<b>I am an AutoCaption Bot 🤖</b>")

@app.on_message(filters.private & filters.command(["help"]))
async def help_command(_, message):
    await message.reply_text("<b>Send media to a channel and I will edit the caption automatically.</b>")

@app.on_message(filters.channel)
async def queue_message(_, message):
    message_queue.append({
        "chat_id": message.chat.id,
        "message_id": message.id,
        "caption": message.caption or ""
    })

async def process_queue():
    while True:
        if message_queue:
            msg = message_queue.pop(0)
            cleaned = clean_caption(msg["caption"])
            final_caption = CUSTOM_CAPTION.format(file_caption=cleaned)
            try:
                await app.edit_message_caption(
                    chat_id=msg["chat_id"],
                    message_id=msg["message_id"],
                    caption=final_caption
                )
                print(f"[✅ Edited] {msg['message_id']}")
            except MessageNotModified:
                print(f"[⚠️ Already Clean] Message {msg['message_id']}")
            except FloodWait as e:
                print(f"[⏳ FloodWait] Waiting {e.value} sec...")
                await asyncio.sleep(e.value + 1)
                message_queue.insert(0, msg)
            except Exception as e:
                print(f"[❌ ERROR] {e} | Msg ID: {msg['message_id']}")
        await asyncio.sleep(1)

@app.on_message(filters.command("status") & filters.user(6167872503))
async def queue_status(_, message):
    await message.reply_text(f"📦 Messages in queue: {len(message_queue)}")

async def main():
    print("Bot is running...")
    await app.start()
    asyncio.create_task(process_queue())
    await idle()
    await app.stop()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
