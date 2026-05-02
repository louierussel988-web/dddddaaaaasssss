import os
import sys
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# Force stdout to flush immediately so logs appear in GitHub Actions
import functools
print = functools.partial(print, flush=True)

async def main():
    print("--- STARTING DOWNLOAD SCRIPT ---")
    
    # 1. Capture Input
    if len(sys.argv) < 2:
        print("!! ERROR: No link found in sys.argv")
        sys.exit(1)
    
    link = sys.argv[1].strip()
    print(f"Target Link: {link}")

    # 2. Load Env
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    session_str = os.getenv('SESSION_STRING')

    if not api_id or not api_hash or not session_str:
        print(f"!! ERROR: Missing Secrets. ID: {bool(api_id)}, Hash: {bool(api_hash)}, Session: {bool(session_str)}")
        sys.exit(1)

    # 3. Parse Link
    try:
        parts = link.split('/')
        if "/c/" in link:
            channel = int(f"-100{parts[4]}")
            msg_id = int(parts[5])
        else:
            channel = parts[3]
            msg_id = int(parts[4])
        print(f"Parsed: Channel {channel}, Message {msg_id}")
    except Exception as e:
        print(f"!! ERROR: Parsing failed: {e}")
        sys.exit(1)

    # 4. Telethon Logic
    client = TelegramClient(StringSession(session_str), int(api_id), api_hash)
    
    try:
        await client.connect()
        if not await client.is_user_authorized():
            print("!! ERROR: Session string is invalid/expired.")
            sys.exit(1)

        print("Logged in successfully. Fetching message...")
        message = await client.get_messages(channel, ids=msg_id)

        if message and message.media:
            print(f"Media found! Downloading...")
            path = await message.download_media()
            print(f"--- DONE: Saved to {path} ---")
        else:
            print("!! ERROR: Message has no media or is restricted.")
            
    except Exception as e:
        print(f"!! CRITICAL ERROR: {e}")
        sys.exit(1)
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
