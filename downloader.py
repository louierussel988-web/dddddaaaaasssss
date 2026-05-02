import os
import sys
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
import functools

# Force stdout to flush immediately
print = functools.partial(print, flush=True)

async def main():
    print("--- STARTING DOWNLOAD SCRIPT ---")
    
    if len(sys.argv) < 2:
        print("!! ERROR: No link found in sys.argv")
        sys.exit(1)
    
    link = sys.argv[1].strip()
    
    # NEW: Set up download directory
    download_dir = "downloads"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    session_str = os.getenv('SESSION_STRING')

    if not api_id or not api_hash or not session_str:
        print("!! ERROR: Missing Secrets.")
        sys.exit(1)

    try:
        parts = link.split('/')
        if "/c/" in link:
            channel = int(f"-100{parts[4]}")
            msg_id = int(parts[5])
        else:
            channel = parts[3]
            msg_id = int(parts[4])
    except Exception as e:
        print(f"!! ERROR: Parsing failed: {e}")
        sys.exit(1)

    client = TelegramClient(StringSession(session_str), int(api_id), api_hash)
    
    try:
        await client.connect()
        if not await client.is_user_authorized():
            print("!! ERROR: Session invalid.")
            sys.exit(1)

        message = await client.get_messages(channel, ids=msg_id)

        if message and message.media:
            print(f"Media found! Downloading to {download_dir}...")
            # MODIFIED: Added file=download_dir to target the folder
            path = await message.download_media(file=download_dir)
            print(f"--- DONE: Saved to {path} ---")
        else:
            print("!! ERROR: No media found.")
            
    except Exception as e:
        print(f"!! CRITICAL ERROR: {e}")
        sys.exit(1)
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
