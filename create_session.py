import consts
import os

from telethon import TelegramClient

phone_number = input('Please enter the Telegram phone number with prefix e.g. +393492617322: ')
phone_number = "".join(phone_number.strip().split())

phone_number_session_file_name = "{}.session".format(phone_number)
session_path = consts.SESSION_FILE_PATH.format(phone_number_session_file_name)

print(f"The session will be saved at the following path: {session_path}")

api_id = consts.API_ID
api_hash = consts.API_HASH

client = TelegramClient(session_path, api_id, api_hash)

async def main():    
    print("Sessions created successfully!")
    me = await client.get_me()

    print("Retrieved account details:")
    print(me.stringify())


print("Starting the Telegram client...")

try:
    client.start(phone_number)
except Exception as e:
    print("The Telegram session cannot be created\nerror: {}".format(e))
    os.remove(session_path) 

with client:
    client.loop.run_until_complete(main())