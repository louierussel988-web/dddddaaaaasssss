import os
import sys
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
SESSION_STR = os.getenv('SESSION_STRING')

async def main():
    if len(sys.argv) < 2:
        print("DEBUG: No argument received in sys.argv")
        return

    link = sys.argv[1]
    print(f"DEBUG: Processing link: {link}")
    parts = link.strip().split('/')
    
    try:
        if "/c/" in link:
            channel = int(f"-100{parts[4]}")
            msg_id = int(parts[5])
        else:
            channel = parts[3]
            msg_id = int(parts[4])
        
        print(f"DEBUG: Parsed Channel ID: {channel}, Message ID: {msg_id}")

        client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)
        
        async with client:
            print("DEBUG: Client connected. Fetching message...")
            message = await client.get_messages(channel, ids=msg_id)
            
            if message is None:
                print("DEBUG: Message not found. Are you sure you are a member of this channel?")
                return

            if message.media:
                print(f"DEBUG: Media found: {type(message.media).__name__}")
                path = await message.download_media()
                print(f"DONE: Downloaded to {path}")
            else:
                print("DEBUG: Message exists but contains no media.")
                
    except Exception as e:
        print(f"ERROR: {type(e).__name__} - {str(e)}")
        sys.exit(1) # This forces the GitHub Action to show the failure

if __name__ == "__main__":
    asyncio.run(main())
