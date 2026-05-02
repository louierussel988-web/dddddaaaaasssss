import os
import sys
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# Environment variables from GitHub Secrets
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
SESSION_STR = os.getenv('SESSION_STRING')

async def main():
    if len(sys.argv) < 2:
        print("Error: No Telegram link provided.")
        return

    link = sys.argv[1]
    parts = link.strip().split('/')
    
    try:
        if "/c/" in link:
            channel = int(f"-100{parts[4]}")
            msg_id = int(parts[5])
        else:
            channel = parts[3]
            msg_id = int(parts[4])
    except (IndexError, ValueError):
        print(f"Error: Could not parse link format: {link}")
        return

    client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)
    
    async with client:
        print(f"Fetching message {msg_id} from {channel}...")
        message = await client.get_messages(channel, ids=msg_id)
        
        if message and message.media:
            print("Downloading media...")
            # Downloads to the current working directory
            path = await message.download_media()
            print(f"Successfully downloaded: {path}")
        else:
            print("No media found in that message.")

if __name__ == "__main__":
    asyncio.run(main())
