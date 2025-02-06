from pyrogram import Client, filters
import time
from dotenv import load_dotenv
import os
import threading
#from flask import Flask
from flask import Flask, request, send_file
import qrcode
import io
import requests
from PIL import Image, ImageDraw
from flask import Flask, request, jsonify
import g4f
# Telegram API credentials
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
image_url = os.getenv("IMAGE_URL")

flask_app = Flask(__name__)

@flask_app.route('/aichat/', methods=['GET'])
def ai_chat():
    model = request.args.get('model', 'gpt-4o-mini')  # Default model
    message = request.args.get('message', '')

    if not message:
        return jsonify({"error": "Message parameter is required."}), 400

    client = Client()
    
    try:
        # Make the API call
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            web_search=False
        )
        
        # Extract the AI response from the structure
        ai_response = response.choices[0].message.content
        
    except Exception as e:
        return jsonify({"error": "Failed to generate response", "details": str(e)}), 500

    return jsonify({"response": ai_response})
"""
@flask_app.route('/aichat/', methods=['GET'])
def ai_chat():
    # Get model and message from request parameters
    model = request.args.get('model', 'default')
    message = request.args.get('message', '')
    
    if not message:
        return jsonify({"error": "Message parameter is required."}), 400
    
    # Generate response using g4f
    try:
        response = g4f.ChatCompletion.create(
            model=model,  # Specify the model if needed
            messages=[{"role": "user", "content": message}]
        )
        ai_response = response['choices'][0]['message']['content']
    except Exception as e:
        return jsonify({"error": "Failed to generate response", "details": str(e)}), 500
    
    # Return AI response in JSON format
    return jsonify({"response": ai_response})
"""

@flask_app.route('/create-qr-code/', methods=['GET'])
def create_qr_code():
    # Step 1: Get user parameters from GET request
    logo_url = request.args.get('logo', '')  # Logo URL
    size = request.args.get('size', '300×300')  # Size of QR Code (default 300x300)
    colour = request.args.get('colour', 'black')  # Colour of QR Code (default black)
    data = request.args.get('data', '')  # Data to encode in QR Code
    back_colour = request.args.get('back_colour', 'white')
    # Step 2: Parse the size parameter (width, height)
    width, height = map(int, size.split('×'))

    # Step 3: Generate the QR code using qrcode library
    qr = qrcode.QRCode(
        version=1,  # Size of the QR Code (1 is smallest, 40 is largest)
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction level
        box_size=10,  # Box size of each QR block
        border=4,  # Border thickness
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Step 4: Create the QR Code image with the given colour
    qr_img = qr.make_image(fill_color=colour, back_color=back_colour).convert('RGBA')
    #qr_img = qr.make_image(fill_color=colour, back_color='white')

    # Step 5: Add logo if provided
    if logo_url:
        # Step 5.1: Download the logo image from the URL
        response = requests.get(logo_url)
        if response.status_code == 200:
            logo = Image.open(io.BytesIO(response.content)).convert("RGBA")

            # Make logo circular
            logo = make_circle_logo(logo)

            # Resize the logo to 1/8th of QR code size for a smaller logo
            qr_width, qr_height = qr_img.size
            logo_size = qr_width // 8
            logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)

            # Place the logo at the center of the QR code
            logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            qr_img.paste(logo, logo_position, mask=logo)
        else:
            return "Logo could not be fetched, please check the URL", 400

    # Step 6: Save the image to a bytes buffer
    img_io = io.BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)

    # Step 7: Return the image as response
    return send_file(img_io, mimetype='image/png')

def make_circle_logo(logo):
    """Convert the logo to a circular image."""
    big_size = (logo.size[0] * 3, logo.size[1] * 3)
    mask = Image.new("L", big_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + big_size, fill=255)
    mask = mask.resize(logo.size, Image.ANTIALIAS)
    logo.putalpha(mask)
    return logo
"""
@flask_app.route('/create-qr-code/', methods=['GET'])
def create_qr_code():
    # Step 1: Get user parameters from GET request
    logo_url = request.args.get('logo', '')  # Logo URL
    size = request.args.get('size', '300×300')  # Size of QR Code (default 300x300)
    colour = request.args.get('colour', 'black')  # Colour of QR Code (default black)
    data = request.args.get('data', '')  # Data to encode in QR Code

    # Step 2: Parse the size parameter (width, height)
    width, height = map(int, size.split('×'))

    # Step 3: Generate the QR code using segno library
    qr = segno.make(data)

    # Step 4: Create the QR Code image with the given colour
    qr_img = qr.to_pil()  # Generate the QR code as a PIL image
    qr_img = qr_img.convert('RGBA')  # Convert to RGBA to handle transparency for logo

    # Step 5: Add logo if provided
    if logo_url:
        # Step 5.1: Download the logo image from the URL
        response = requests.get(logo_url)
        if response.status_code == 200:
            logo = Image.open(io.BytesIO(response.content))  # Load image from byte stream

            # Step 5.2: Resize the logo to fit inside the QR code (1/5th of the QR code size)
            qr_width, qr_height = qr_img.size
            logo_size = qr_width // 5  # Resize logo to 1/5th of QR code size
            logo = logo.resize((logo_size, logo_size))

            # Step 5.3: Position the logo in the center of the QR code
            logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

            # Step 5.4: Paste the logo on top of the QR code
            qr_img.paste(logo, logo_position, mask=logo.convert("RGBA").split()[3])  # Use alpha channel as mask
        else:
            return "Logo could not be fetched, please check the URL", 400

    # Step 6: Resize QR code image to match the requested size
    qr_img = qr_img.resize((width, height), Image.ANTIALIAS)

    # Step 7: Save the image to a bytes buffer
    img_io = io.BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)

    # Step 8: Return the image as response
    return send_file(img_io, mimetype='image/png')


@flask_app.route('/create-qr-code/', methods=['GET'])
def create_qr_code():
    # Step 1: Get user parameters from GET request
    logo_url = request.args.get('logo', '')  # Logo URL
    size = request.args.get('size', '300×300')  # Size of QR Code (default 300x300)
    colour = request.args.get('colour', 'black')  # Colour of QR Code (default black)
    data = request.args.get('data', '')  # Data to encode in QR Code

    # Step 2: Parse the size parameter (width, height)
    width, height = map(int, size.split('×'))

    # Step 3: Generate the QR code using qrcode library
    qr = qrcode.QRCode(
        version=1,  # Size of the QR Code (1 is smallest, 40 is largest)
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction level
        box_size=10,  # Box size of each QR block
        border=4,  # Border thickness
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Step 4: Create the QR Code image with the given colour
    qr_img = qr.make_image(fill=colour, back_color='white')

    # Step 5: Add logo if provided
    if logo_url:
        # Step 5.1: Download the logo image from the URL
        response = requests.get(logo_url)
        if response.status_code == 200:
            logo = Image.open(io.BytesIO(response.content))  # Load image from byte stream
            qr_width, qr_height = qr_img.size
            logo_size = qr_width // 5  # Resize the logo to 1/5th of QR code size
            logo = logo.resize((logo_size, logo_size))
            logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            qr_img.paste(logo, logo_position, mask=logo.convert("RGBA").split()[3])  # Use alpha channel as mask
        else:
            return "Logo could not be fetched, please check the URL", 400

    # Step 6: Save the image to a bytes buffer
    img_io = io.BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)

    # Step 7: Return the image as response
    return send_file(img_io, mimetype='image/png')


@flask_app.route('/create-qr-code/', methods=['GET'])
def create_qr_code():
    # Step 1: Get user parameters from GET request
    logo_url = request.args.get('logo', '')  # Logo URL
    size = request.args.get('size', '300x300')  # Size of QR Code (default 300x300)
    colour = request.args.get('colour', 'black')  # Colour of QR Code (default black)
    data = request.args.get('data', '')  # Data to encode in QR Code

    # Step 2: Parse the size parameter (width, height)
    width, height = map(int, size.split('×'))

    # Step 3: Generate the QR code using qrcode library
    qr = qrcode.QRCode(
        version=1,  # Size of the QR Code (1 is smallest, 40 is largest)
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction level
        box_size=10,  # Box size of each QR block
        border=4,  # Border thickness
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Step 4: Create the QR Code image with the given colour
    qr_img = qr.make_image(fill=colour, back_color='white')

    # Step 5: Add logo if provided
    if logo_url:
        logo = Image.open(logo_url)  # Open the logo image from URL or local path
        qr_width, qr_height = qr_img.size
        logo_size = qr_width // 5  # Resize the logo to 1/5th of QR code size
        logo = logo.resize((logo_size, logo_size))
        logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        qr_img.paste(logo, logo_position, mask=logo.convert("RGBA").split()[3])  # Use alpha channel as mask

    # Step 6: Save the image to a bytes buffer
    img_io = io.BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)

    # Step 7: Return the image as response
    return send_file(img_io, mimetype='image/png')
"""
    
@flask_app.route('/')
def home():
    return "Image Generater Bot is running."

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# उपयोगकर्ता का ट्रैक रखने के लिए डिक्शनरी

usertime = {}
# जब भी कोई मैसेज प्राप्त हो
# Start Command
@app.on_message(filters.command("start"))
async def start(client, message):
    first_name = message.from_user.first_name
    await message.reply_text(
        f"ʜᴇʏ {first_name}! ɪ ᴀᴍ ᴀɴ ᴀɪ ɪᴍᴀɢᴇ ɢᴇɴᴇʀᴀᴛᴏʀ.\n"
        "ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ʙʀɪɴɢ ʏᴏᴜʀ ɪᴅᴇᴀs ᴛᴏ ʟɪғᴇ ᴡɪᴛʜ ʙʀᴇᴀᴛʜᴛᴀᴋɪɴɢ ᴀʀᴛᴡᴏʀᴋ!\n"
        "ᴅᴇsᴄʀɪʙᴇ ᴀɴʏ sᴄᴇɴᴇ, ᴄʜᴀʀᴀᴄᴛᴇʀ, ᴏʀ ᴄᴏɴᴄᴇᴘᴛ ʏᴏᴜ ᴄᴀɴ ɪᴍᴀɢɪɴᴇ, "
        "ᴀɴᴅ ɪ'ʟʟ ᴛʀᴀɴsғᴏʀᴍ ɪᴛ ɪɴᴛᴏ ᴀᴍᴀᴢɪɴɢ ᴠɪsᴜᴀʟs.\n"
        "ʟᴇᴛ's ᴄʀᴇᴀᴛᴇ sᴏᴍᴇᴛʜɪɴɢ ᴇxᴛʀᴀᴏʀᴅɪɴᴀʀʏ ᴛᴏɢᴇᴛʜᴇʀ!"
    )
    
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
    usertime[user_id] = 45
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
