from pyrogram import Client, filters
import time
from dotenv import load_dotenv
import os
import threading
from flask import Flask
# Telegram API credentials
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
image_url = os.getenv("IMAGE_URL")

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Image Generater Bot is running."

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# उपयोगकर्ता का ट्रैक रखने के लिए डिक्शनरी

usertime = {}
# जब भी कोई मैसेज प्राप्त हो
@app.on_message(filters.text)
def reply(client, message):
    user_id = message.from_user.id
    if user_id in usertime:
       if usertime[user_id] < 46:
            waitmsg = message.reply_text(f"𝐏𝐥𝐞𝐚𝐬𝐞 𝐖𝐚𝐢𝐭 𝐅𝐨𝐫 {usertime[user_id]} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬 𝐁𝐞𝐟𝐨𝐫𝐞 𝐍𝐞𝐱𝐭  𝐑𝐞𝐪𝐮𝐞𝐬𝐭...")
            message.delete()
            time.sleep(usertime[user_id])
            waitmsg.edit_text("𝐍𝐎𝐖 𝐘𝐎𝐔 𝐂𝐀𝐍 𝐆𝐄𝐍𝐄𝐑𝐀𝐓𝐄 𝐀 𝐍𝐄𝐖 𝐈𝐌𝐀𝐆𝐄...")
            
            time.sleep(1)
            waitmsg.delete()
            return

    # समय अपडेट करें

    # प्रोसेसिंग
    msg = message.text
    god = msg.replace(' ', '%20')
    s = message.reply_text(f"𝐏𝐋𝐄𝐀𝐒𝐄 𝐖𝐀𝐈𝐓 ...\n\n 𝑮𝑬𝑵𝑬𝑹𝑨𝑻𝑰𝑵𝑮 𝑰𝑴𝑨𝑮𝑬 𝑭𝑶𝑹 ✵{msg}✵")
    image_url1 = f"{image_url}{god}"
    a = message.reply_photo(photo=image_url1, caption=f"𝒀𝑶𝑼𝑹 𝑹𝑬𝑸𝑼𝑬𝑺𝑻𝑬𝑫 𝑰𝑴𝑨𝑮𝑬 𝑭𝑶𝑹:\n✫ {msg} ✫\n\n𝐍𝐎𝐓𝐄 ☞ THIS IMAGE WILL BE DELETED IN 5 MINUTES PLEASE SAVE THIS IMAGE IN ANY OTHER CHAT.\n\n    ʙʏ ➳ 𝐌𝐑. 𝐒𝐈𝐍𝐆𝐎𝐃𝐈𝐘𝐀")
    s.delete()
    waitmsg = message.reply_text("𝐏𝐥𝐞𝐚𝐬𝐞 𝐖𝐚𝐢𝐭 𝐅𝐨𝐫 45 𝐒𝐞𝐜𝐨𝐧𝐝𝐬 𝐁𝐞𝐟𝐨𝐫𝐞 𝐍𝐞𝐱𝐭  𝐑𝐞𝐪𝐮𝐞𝐬𝐭...")
    usertime[user_id] = 45
    time.sleep(15)
    usertime[user_id] = 30
    time.sleep(5)
    usertime[user_id] = 25
    time.sleep(10)
    usertime[user_id] = 20
    time.sleep(5)
    waitmsg.edit_text("𝐏𝐥𝐞𝐚𝐬𝐞 𝐖𝐚𝐢𝐭 𝐅𝐨𝐫 15 𝐒𝐞𝐜𝐨𝐧𝐝𝐬 𝐁𝐞𝐟𝐨𝐫𝐞 𝐍𝐞𝐱𝐭  𝐑𝐞𝐪𝐮𝐞𝐬𝐭...")
    usertime[user_id] = 15
    time.sleep(5)
    usertime[user_id] = 10
    time.sleep(5)
    usertime[user_id] = 5
    time.sleep(2)
    waitmsg.edit_text("𝐏𝐥𝐞𝐚𝐬𝐞 𝐖𝐚𝐢𝐭 𝐅𝐨𝐫 3 𝐒𝐞𝐜𝐨𝐧𝐝𝐬 𝐁𝐞𝐟𝐨𝐫𝐞 𝐍𝐞𝐱𝐭  𝐑𝐞𝐪𝐮𝐞𝐬𝐭...")
    usertime[user_id] = 3
    time.sleep(3)
    waitmsg.edit_text("𝐍𝐎𝐖 𝐘𝐎𝐔 𝐂𝐀𝐍 𝐆𝐄𝐍𝐄𝐑𝐀𝐓𝐄 𝐀 𝐍𝐄𝐖 𝐈𝐌𝐀𝐆𝐄...")
    del usertime[user_id]
    time.sleep(255)
    a.delete()
   # message.delete()
    waitmsg.delete()

def run_flask():
    flask_app.run(host="0.0.0.0", port=5000)
    
def run_bot():
    print("Bot is running...By Mr. Singodiya")
    app.run()
# बॉट रन करें

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    run_bot()
