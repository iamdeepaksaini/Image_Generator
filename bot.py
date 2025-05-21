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
from g4f.client import Client
import pollinations
import uuid
import json
# Telegram API credentials
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
image_url = os.getenv("IMAGE_URL")
"""
###########№#№#######################№########₹@÷№
# Load Stable Diffusion model
from flask import Flask, request, send_file
import torch
from diffusers import StableDiffusionPipeline
import requests
from PIL import Image
from io import BytesIO

pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

# Helper function to download image from URL
def download_image1(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        return None

@app.route('/ai-image-editor', methods=['GET'])
def ai_image_editor():
    image_url = request.args.get('image_url')
    prompt = request.args.get('prompt', "enhance background and add more pixels")

    if not image_url:
        return {"error": "Image URL is required"}, 400

    image = download_image1(image_url)
    if image is None:
        return {"error": "Failed to download image"}, 400

    result = pipe(prompt, image=image).images[0]

    # Save processed image to BytesIO
    img_io = BytesIO()
    result.save(img_io, 'PNG')
    img_io.seek(0)

    # Return image as response
    return send_file(img_io, mimetype='image/png')

#########################
"""
def senderror(ERROR_MESSAGE):
        # Replace these with your actual bot token and chat ID
        OKEN123 = "7657950840:AAFycxq_WLI4SwKe_0Oz4r9JW1Tp4PZFLiE"
        CHAT_ID123 = "6150091802"  # Your chat ID or group ID
        url = f"https://api.telegram.org/bot{OKEN123}/sendMessage"
        payload = {
            "chat_id": CHAT_ID123,
            "text": ERROR_MESSAGE
        }
        response = requests.post(url, data=payload)
        return 

flask_app = Flask(__name__)

@flask_app.route('/result')
def get_result():
    roll_no = request.args.get('roll_no')
    url = request.args.get('url')
    if not roll_no:
        return "Error: roll_no parameter missing.", 400

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://rajeduboard.rajasthan.gov.in/RESULT2022/SEV/SEVROLL_INPUT.ASP',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36'
    }
    data = {
        'roll_no': roll_no
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}", 500

@flask_app.route("/ai-image/", methods=["GET"])
def generate_image():
    try:
        # Query parameters लेना
        prompt = request.args.get("prompt", default="Mr. Singodiya name Logo.")
        model = request.args.get("model", default="flux")
        seed = request.args.get("seed", default="1245")
        height = int(request.args.get("height", default=1024))
        width = int(request.args.get("width", default=1024))
        enhance = request.args.get("enhance", default="false").lower() == "true"
        safe = request.args.get("safe", default="true")

        # Pollinations API से इमेज जनरेट करना
        image_model = pollinations.Image(
            model=pollinations.Image.flux(),  # सही मॉडल का उपयोग
            seed=seed,
            width=width,
            height=height,
            enhance=enhance,
            nologo=True,
            private=True,
            safe=safe,
            referrer="pollinations.py"
        )

        # इमेज को जनरेट करें
        generated_image = image_model(prompt=prompt)

        # Correct File Path (absolute path for Termux)
        temp_file = f"/tmp/generated_image_{prompt.replace(' ', '_')}.png"  # Render uses /tmp for temporary files
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(temp_file), exist_ok=True)

        # इमेज को local file system पर सेव करना (temporary file)
        generated_image.save(file=temp_file)

        # इमेज को HTTP response के रूप में भेजना
        response = send_file(
            temp_file,
            mimetype='image/png',
            as_attachment=False,
            download_name=f"{prompt.replace(' ', '_')}.png"
        )

        # इमेज को भेजने के बाद उसे delete करना
        os.remove(temp_file)

        return response
    
    except Exception as e:
        ERROR_MESSAGE= f"Error With = flask_app.route(\"/ai-image/\", methods=[\"GET\"]) : {str(e)}"
        senderror(ERROR_MESSAGE)
        return "Error: server busy please change your model", 500


@flask_app.route('/aichat/', methods=['GET'])
def aichai():
    try:
        model = request.args.get('model', 'openai')
        prompt = request.args.get('prompt', '')
        seed = request.args.get('seed', '42')
        system = request.args.get('system', 'Your Name is Kitti. You are an AI assistant of Mr. Singodiya. You are developed by Mr. Singodiya. Your owner is Mr. Singodiya.')
        messages = request.args.get('messages', '[]')

        # Parse messages safely
        try:
            messages = json.loads(messages)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON format in 'messages'"}), 400

        # Format messages for pollinations
        formatted_messages = [
            pollinations.Text.Message(role=msg.get('role', ''), content=msg.get('content', ''))
            for msg in messages if isinstance(msg, dict)
        ]

        # Create pollinations text model
        text_model = pollinations.Text(
            model=eval(f"pollinations.Text.{model}"),
            system=system,
            contextual=True,
            messages=formatted_messages,
            seed=seed,
            jsonMode=False,
            referrer="pollinations.py"
        )

        # Determine user message
        user_message = prompt if prompt else (messages[-1].get('content', 'No content provided') if messages else 'No content provided')

        response = text_model(
            prompt=(prompt, user_message),
            display=True,
            encode=True
        )

        return response.response , 200

    except Exception as e:
        ERROR_MESSAGE= f"Error with  app.route('/aichat/', methods=['GET']) : {str(e)}"
        senderror(ERROR_MESSAGE)
        #return f"Error: server busy please change your model", 500
        return jsonify({"error": "Server Busy"}), 500
  
  

@flask_app.route('/aichat/', methods=['POST'])
def aichatpost():
    try:
        model = request.args.get('model', 'openai')
        prompt = request.args.get('prompt', '')
        seed = request.args.get('seed', '42')
        system = request.args.get('system','Your Name is Kitti. You are an AI assistant of Mr. Singodiya. You are developed by Mr. Singodiya. Your owner is Mr. Singodiya.')
        
        # Parse messages from JSON request
        messages = request.json.get('messages', [])
        if not isinstance(messages, list):
            return jsonify({"error": "Invalid JSON format for 'messages'. It should be a list."}), 400

        # Format messages for pollinations
        formatted_messages = [
            pollinations.Text.Message(role=msg['role'], content=msg['content'])
            for msg in messages if 'role' in msg and 'content' in msg
        ]

        text_model = pollinations.Text(
            model=eval(f"pollinations.Text.{model}"),
            system=system,
            contextual=True,
            messages=formatted_messages,
            seed=seed,
            jsonMode=False,
            referrer="pollinations.py"
        )

        # Determine the user message
        user_message = prompt or (messages[-1].get('content') if messages else 'No content provided')

        # Generate response
        response = text_model(
            prompt=user_message,
            display=False,
            encode=True
        )

        return response.response, 200

    except Exception as e:
        ERROR_MESSAGE= f"app.route('/aichat/', methods=['POST']) {str(e)}"
        senderror(ERROR_MESSAGE)
       # return f"Error: server busy please change your model", 
        return jsonify({"error": "server busy"}), 500


@flask_app.route('/aichat/v2', methods=['POST'])
def aichai_post():
    try:
        # Extract the JSON payload
        data = request.json
        model = data.get('model', 'llama')
        seed = data.get('seed', 'random')
        system = data.get('System', 'Your Name is Kitti.You are a ai assistant of Mr. Singodiya.You are Developed by Mr. Singodiya.Your owner is Mr. Singodiya.')
        messages = data.get('messages', [])
        images = data.get('Images', [])
        
        # Download all images from the provided URLs
        image_paths = []
        for image_url in images:
            image_paths.append(download_image(image_url))

        # Convert messages to pollinations format
        formatted_messages = [
            pollinations.Text.Message(role=msg['role'], content=msg['content'])
            for msg in messages
        ]

        # Create pollinations text request
        user_message = messages[-1].get('content', 'No content provided')
        text_request = pollinations.Text.Request(
            model=eval(f"pollinations.Text.{model}"),  # Convert string to actual model object
            prompt=user_message,
            system=system,
            contextual=True,
            messages=formatted_messages,
            images=[pollinations.Text.Message.image(path) for path in image_paths],
            seed=seed,
            jsonMode=False,
            referrer="pollinations.py"
        )

        # Get the response
        response = text_request(encode=True)

        # Clean up the downloaded images
        for image_path in image_paths:
            if image_path and os.path.exists(image_path):
                os.remove(image_path)

        # Return the response as JSON
        return response, 200

    except Exception as e:
        ERROR_MESSAGE= f" Error With flask_app.route('/aichat/v2', methods=['POST']) {str(e)}"
        senderror(ERROR_MESSAGE)
      #  return f"Error: server busy please change your model", 500
        return jsonify({"error": "server busy please try with a different model"}), 500
  # For generating unique filenames

def download_image(image_url):
    """Download the image from the provided URL and return the local file path."""
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Generate a unique filename
        file_name = f"{uuid.uuid4()}.jpg"
        file_path = os.path.join("/tmp/", file_name)
        
        # Save the image content
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        return file_path
    except Exception as e:
        raise Exception(f"Failed to open image from : {str(e)}")




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
    
@flask_app.route('/')
def home():
    return "Apis Are Working Well"


from pyrogram import Client, filters

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# उपयोगकर्ता का ट्रैक रखने के लिए डिक्शनरी

usertime = {}
# जब भी कोई मैसेज प्राप्त हो
# Start Command
@app.on_message(filters.command("start") & ~filters.me)
async def start(client, message):
    first_name = message.from_user.first_name
    await message.reply_text(
        f"ʜᴇʏ {first_name}! ɪ ᴀᴍ ᴀɴ ᴀɪ ɪᴍᴀɢᴇ ɢᴇɴᴇʀᴀᴛᴏʀ.\n"
        "ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ʙʀɪɴɢ ʏᴏᴜʀ ɪᴅᴇᴀs ᴛᴏ ʟɪғᴇ ᴡɪᴛʜ ʙʀᴇᴀᴛʜᴛᴀᴋɪɴɢ ᴀʀᴛᴡᴏʀᴋ!\n"
        "ᴅᴇsᴄʀɪʙᴇ ᴀɴʏ sᴄᴇɴᴇ, ᴄʜᴀʀᴀᴄᴛᴇʀ, ᴏʀ ᴄᴏɴᴄᴇᴘᴛ ʏᴏᴜ ᴄᴀɴ ɪᴍᴀɢɪɴᴇ, "
        "ᴀɴᴅ ɪ'ʟʟ ᴛʀᴀɴsғᴏʀᴍ ɪᴛ ɪɴᴛᴏ ᴀᴍᴀᴢɪɴɢ ᴠɪsᴜᴀʟs.\n"
        "ʟᴇᴛ's ᴄʀᴇᴀᴛᴇ sᴏᴍᴇᴛʜɪɴɢ ᴇxᴛʀᴀᴏʀᴅɪɴᴀʀʏ ᴛᴏɢᴇᴛʜᴇʀ!"
    )
    
@app.on_message(filters.text & ~filters.me)
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
