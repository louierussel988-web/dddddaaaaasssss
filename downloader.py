from telethon import TelegramClient
from telethon.sessions import StringSession
import os
import sys

# Get secrets from GitHub Environment
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
session_str = os.getenv('SESSION_STRING') # You'll need to add this secret

# Use StringSession to bypass interactive login
client = TelegramClient(StringSession(session_str), api_id, api_hash)

async def download_media():
    if len(sys.argv) < 2:
        print("No link provided.")
        return

    link = sys.argv[1]
    parts = link.split('/')
    
    try:
        # Simplified parsing logic
        if "/c/" in link:
            channel = int(f"-100{parts[4]}")
            message_id = int(parts[5])
        else:
            channel = parts[3]
            message_id = int(parts[4])

        await client.start()
        message = await client.get_messages(channel, ids=message_id)

        if message and message.media:
            path = await message.download_media()
            print(f"Downloaded to: {path}")
        else:
            print("No media found.")
            
    except Exception as e:
        print(f"Error: {e}")

with client:
    client.loop.run_until_complete(download_media())
