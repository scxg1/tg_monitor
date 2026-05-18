import asyncio, requests, os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import UserStatusOnline

API_ID    = 37040646
API_HASH  = "8a94d0fe746a23fe32a4cf1940c55520"
BOT_TOKEN = "7894776342:AAHqDfLZA_YrEOKiZx46NWatC1dwiq1FxcE"
CHAT_ID   = "7452499721"
SESSION   = os.environ.get("SESSION_STRING", "")
TARGETS   = ["markgaza", "dr_gaza1"]

def notify(username):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": f"🟢 @{username} متصل الآن!"}
    )

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
target_ids = {}

@client.on(events.Raw)
async def handler(update):
    if not hasattr(update, 'user_id') or not hasattr(update, 'status'):
        return
    for username, uid in target_ids.items():
        if update.user_id == uid:
            if isinstance(update.status, UserStatusOnline):
                notify(username)

async def main():
    await client.start()
    for username in TARGETS:
        entity = await client.get_entity(username)
        target_ids[username] = entity.id
        print(f"✅ مراقبة: @{username}")
    print("🚀 البوت شغال...")
    await client.run_until_disconnected()

asyncio.run(main())
