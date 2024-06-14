import os
import json
from pyrogram import Client, filters
from flask import Flask
from dotenv import load_dotenv
from refar import referral_handler

# Load environment variables from .env file
load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
bot_user = os.getenv("bot_user")
domain_app = os.getenv("domain")

print(api_id)
print(api_hash)
print(bot_user)
print(domain_app)

# Load user data from a JSON file
def load_data():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user data to a JSON file
def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file)

data = load_data()

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = str(message.from_user.id)
    referral_code = message.text.split('=')[-1] if '=' in message.text else None
    if user_id not in data:
        data[user_id] = {
            "coins": 0,
            "referrals": 0
        }
        save_data(data)
        if referral_code:
            referral_handler(referral_code, user_id, data)
            save_data(data)
    await message.reply(f"Hello! Welcome to the interactive bot. You have {data[user_id]['coins']} coins. Tap to earn coins and more!")

@app.on_message(filters.command("play"))
async def play(client, message):
    user_id = str(message.from_user.id)
    game_url = f"{domain_app}/play/{user_id}"
    await message.reply(f"Click [here]({game_url}) to start playing!", disable_web_page_preview=True)

@app.on_message(filters.command("referral"))
async def referral(client, message):
    user_id = str(message.from_user.id)
    referral_link = f"https://t.me/{bot_user}?start={user_id}"
    await message.reply(f"Share this link to refer others: {referral_link}")

if __name__ == "__main__":
    app.start()
    from game import web_app

    # Start the Flask web app in a separate thread
    import threading
    threading.Thread(target=lambda: web_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5002)))).start()

    
