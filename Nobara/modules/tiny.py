import os
import cv2
from PIL import Image
from pyrogram import filters
from Nobara import app
from config import config
from Nobara.decorator.save import save 
from Nobara.decorator.errors import error

@app.on_message(filters.command("tiny" , prefixes=config.COMMAND_PREFIXES) & filters.reply)
@error
@save
async def tiny_command(client, message):
    reply = message.reply_to_message

    if not reply.media:
        await message.reply("`𝖯𝗅𝖾𝖺𝗌𝖾 𝗋𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺 𝗌𝗍𝗂𝖼𝗄𝖾𝗋, 𝗂𝗆𝖺𝗀𝖾, 𝗈𝗋 𝗏𝗂𝖽𝖾𝗈.`")
        return

    processing_message = await message.reply("`Processing tiny...`")
    file_path = await client.download_media(reply)
    im1 = Image.open("Nobara/resources/transparent.png")  # Background image for final output

    try:
        # Determine file extension
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()

        # Set output file name dynamically
        output_file = f"result{file_extension}"

        if file_extension == ".tgs":
            os.system(f"lottie_convert.py {file_path} json.json")
            with open("json.json", "r") as json_file:
                json_data = json_file.read()
            json_data = json_data.replace("512", "2000")
            with open("json.json", "w") as json_file:
                json_file.write(json_data)
            os.system("lottie_convert.py json.json result.tgs")
            output_file = "result.tgs"
            os.remove("json.json")
        elif file_extension in [".gif", ".mp4"]:
            cap = cv2.VideoCapture(file_path)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite("frame.png", frame)
            cap.release()
            image_file = "frame.png"
        else:
            image_file = file_path

        # Resize image and paste onto background
        im = Image.open(image_file)
        width, height = im.size
        if width == height:
            new_width, new_height = 200, 200
        else:
            total = width + height
            width_ratio = width / total
            height_ratio = height / total
            new_width = int(200 + 5 * ((width_ratio * 100) - 50))
            new_height = int(200 + 5 * ((height_ratio * 100) - 50))
        
        resized_image = im.resize((new_width, new_height))
        resized_image.save("resized.png", format="PNG", optimize=True)
        im2 = Image.open("resized.png")

        back_im = im1.copy()
        back_im.paste(im2, (150, 0))  # Paste resized image onto background
        output_file = "result.webp"
        back_im.save(output_file, "WEBP", quality=95)

        # Send the processed file
        await client.send_document(
            chat_id=message.chat.id,
            document=output_file,
            reply_to_message_id=reply.id
        )
    finally:
        # Cleanup temporary files
        os.remove(file_path)
        if os.path.exists("frame.png"):
            os.remove("frame.png")
        if os.path.exists("resized.png"):
            os.remove("resized.png")
        if os.path.exists("result.webp"):
            os.remove("result.webp")
        if os.path.exists("result.tgs"):
            os.remove("result.tgs")

    await processing_message.delete()


__module__ = "𝖳𝗂𝗇𝗒"


__help__ = """ ✧ `/tiny` (𝗋𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺 𝗌𝗍𝗂𝖼𝗄𝖾𝗋 , 𝗏𝗂𝖽𝖾𝗈 𝗈𝗋 𝗂𝗆𝖺𝗀𝖾) *:* 𝖢𝗈𝗇𝗏𝖾𝗋𝗍𝗌 𝖳𝗁𝖺𝗍 𝖲𝗍𝗂𝖼𝗄𝖾𝗋 , 𝖵𝗂𝖽𝖾𝗈 𝖮𝗋 𝖨𝗆𝖺𝗀𝖾 𝖳𝗈 𝖳𝗂𝗇𝗒 𝖲𝗂𝗓𝖾.
 """