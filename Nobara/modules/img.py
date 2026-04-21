from pyrogram import filters
from Nobara.imgloader import downloader
import os
import shutil
from Nobara import app
from pyrogram.enums import ParseMode
from pyrogram.types import InputMediaPhoto , Message
from config import config 
from Nobara.decorator.save import save 
from Nobara.decorator.errors import error


# Command to download images
@app.on_message(filters.command("img" , prefixes=config.COMMAND_PREFIXES))
@error
@save
async def download_images(client, message : Message):
    if len(message.command) < 2:
        await message.reply("𝖴𝗌𝖺𝗀𝖾: `/𝗂𝗆𝗀 <𝗊𝗎𝖾𝗋𝗒>`\𝗇𝖤𝗑𝖺𝗆𝗉𝗅𝖾: `/𝗂𝗆𝗀 𝖼𝖺𝗍𝗌`", parse_mode=ParseMode.MARKDOWN)
        return
    
    query = " ".join(message.command[1:])
    limit = 8  # Set the limit of images to download
    output_dir = "downloads"

    a = await message.reply_text("🔎")
    
    # Download images
    try:
        downloader.download(
            query=query,  # Corrected from query to keyword
            limit=limit,
            output_dir=output_dir,
            adult_filter_off=True,
            force_replace=True,
            timeout=60,
            verbose=True
        )

        # Prepare to send images as an album
        folder_path = os.path.join(output_dir, query)
        image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith((".jpg", ".png"))]

        if image_files:
            media_group = [
                InputMediaPhoto(media=open(img_path, "rb")) for img_path in image_files
            ]

            # Send images as a media group (album)
            await a.delete()
            await message.reply_media_group(media=media_group)
        else:
            await message.reply("𝖭𝗈 𝗂𝗆𝖺𝗀𝖾𝗌 𝗐𝖾𝗋𝖾 𝖿𝗈𝗎𝗇𝖽 𝗍𝗈 𝗌𝖾𝗇𝖽.")

        # Cleanup after sending
        shutil.rmtree(output_dir)

    except Exception as e:
        await message.reply(f"𝖠𝗇 𝖾𝗋𝗋𝗈𝗋 𝗈𝖼𝖼𝗎𝗋𝗋𝖾𝖽 : {e}")


__module__ = "𝖨𝗆𝖺𝗀𝖾"


__help__ = """**𝖴𝗌𝖾𝗋 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌:**
  ✧ `/𝗂𝗆𝗀` (𝗊𝗎𝖾𝗋𝗒) **:** 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽𝗌 𝖺𝗇𝖽 𝗌𝖾𝗇𝖽𝗌 𝗂𝗆𝖺𝗀𝖾𝗌 𝖿𝗋𝗈𝗆 𝖡𝗂𝗇𝗀 𝖿𝗈𝗋 𝗍𝗁𝖾 𝗀𝗂𝗏𝖾𝗇 𝗊𝗎𝖾𝗋𝗒.
 
*𝖤𝗑𝖺𝗆𝗉𝗅𝖾𝗌:*
  ✧ `/𝗂𝗆𝗀 𝖼𝖺𝗍𝗌` **:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝗂𝗆𝖺𝗀𝖾𝗌 𝗈𝖿 𝖼𝖺𝗍𝗌.
   ✧ `/𝗂𝗆𝗀 𝗌𝗎𝗇𝗌𝖾𝗍` **:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝗂𝗆𝖺𝗀𝖾𝗌 𝗈𝖿 𝗌𝗎𝗇𝗌𝖾𝗍𝗌.
 """