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

LANG_MAP = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "ml": "Malayalam",
    "kn": "Kannada",
    "bn": "Bengali",
    "mr": "Marathi",
    "pa": "Punjabi",
    "gu": "Gujarati",
    "ur": "Urdu",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese"
}

REMOVE_WORDS = [
    'R∆G∆ ', 'AnimeKaizoku', 'join', 'Toonworld4all', 'psa', 'https', 'http',
    'Full Bollywood Movie', 'Bollywood', 'ViSTA', 'MoviesMod',
    '(Mᴏᴏɴ Kɴɪɢʜᴛ)', 'L3G3N7', 'telegram', 'm2links', "join us", "Join Us",
    "t.me", "mkvcinemas", "moviesmod", "moviesflix", "Desiremovies",
    "mkvc", "cinevood", "@m2links", "skymovieshd", "(dedsincebirth)",
    "Full", "MoviesUP", "B∆TM∆N", "K☈N", "SANKET", "ExtraFlix",
    "MoviezVerse.net", "MoviesVerse", "Hollywood", "4kHdHub",
    "CrickeTLoveRR", "HDHub4u", "PrimeFix", "email"
]

def clean_caption(caption: str) -> str:
    if not caption:
        return ""
    match = re.search(r"(.*?\b(?:mkv|mp4)\b)", caption, re.IGNORECASE)
    if match:
        caption = match.group(1)
    caption = re.sub(r'\b(mkv|mp4)\b', '', caption, flags=re.IGNORECASE)
    for word in REMOVE_WORDS:
        caption = re.sub(re.escape(word), '', caption, flags=re.IGNORECASE)
    caption = re.sub(r'[_\-\|\+\[\]\{\}~#$]', ' ', caption)
    caption = caption.replace('.', ' ')
    return ' '.join(caption.split())

def infer_languages_from_caption(caption: str) -> str:
    if not caption:
        return ""
    text = caption.lower()
    langs = set()

    if "hindi" in text:
        langs.add("Hindi")
    if "english" in text:
        langs.add("English")
    if "tamil" in text:
        langs.add("Tamil")
    if "telugu" in text:
        langs.add("Telugu")
    if "malayalam" in text:
        langs.add("Malayalam")
    if "kannada" in text:
        langs.add("Kannada")

    if "dual audio" in text or "dual-audio" in text:
        if not langs:
            langs.update(["Hindi", "English"])

    if "multi audio" in text or "multi-audio" in text:
        langs.add("Multi Audio")

    return ", ".join(sorted(langs))

def get_audio_languages(message) -> str:
    media = message.video or message.document or message.audio
    if media:
        tg_langs = getattr(media, "audio_languages", None)
        if tg_langs:
            return ", ".join(LANG_MAP.get(l, l.upper()) for l in tg_langs)
    return infer_languages_from_caption(message.caption or "")

@app.on_message(filters.private & filters.command("start"))
async def start(_, message):
    await message.reply_text(
        f"<b>Hello {message.from_user.mention},</b>\n\n<b>I am an AutoCaption Bot 🤖</b>"
    )

@app.on_message(filters.private & filters.command("help"))
async def help_cmd(_, message):
    await message.reply_text(
        "<b>Send media to a channel and I will edit the caption automatically.</b>"
    )

@app.on_message(filters.channel)
async def queue_message(_, message):
    if not (message.video or message.document or message.audio):
        return
    message_queue.append(message)

async def process_queue():
    while True:
        if message_queue:
            msg = message_queue.pop(0)
            cleaned = clean_caption(msg.caption or "")
            languages = get_audio_languages(msg)

            final_caption = CUSTOM_CAPTION.format(file_caption=cleaned)
            if languages:
                final_caption += f"\n<b>🔊 Audio:</b> {languages}"

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
                print(f"[ERROR] {e} | Msg ID: {msg.id}")

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
