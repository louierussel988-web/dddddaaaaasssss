from telethon import TelegramClient
import asyncio
import os
import sys

# 1. Corrected environment variable fetching (needs quotes)
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
session_name = 'me'

# 2. You need to define 'link' and 'link_type' or get them from arguments
if len(sys.argv) < 2:
    print("Usage: python script.py <telegram_link>")
    sys.exit(1)

link = sys.argv[1]

parts = link.split('/')

# 3. Logic to parse the ID and Message ID
try:
    if "https://t.me/c/" in link:
        channel = int(f"-100{parts[4]}")
        message_id = int(parts[5])
    else:
        # For public links like t.me/channel/123
        channel = parts[3]
        message_id = int(parts[4])
except (IndexError, ValueError):
    print("Invalid Link Format")
    sys.exit(1)

client = TelegramClient(session_name, api_id, api_hash)

async def download_media():
    await client.start()
    message = await client.get_messages(channel, ids=message_id)

    if message and message.media:
        print("Downloading media...")
        path = await message.download_media()
        print(f"Downloaded to: {path}")
    else:
        print("No media found in this message.")

with client:
    client.loop.run_until_complete(download_media())
