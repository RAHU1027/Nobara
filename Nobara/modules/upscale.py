import os
from pyrogram import filters
from Nobara import app
from Nobara.helper.upscale_helper import getFile, UpscaleImages
import config 
from Nobara.decorator.save import save 
from Nobara.decorator.errors import error

@app.on_message(filters.command(["upscale" , "enhance" , config.config.CMD_STARTERS]))
@error
@save
async def upscaleImages(_, message):

    file = await getFile(message)
    if file is None:
        return await message.reply_text("𝖱𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺𝗇 𝗂𝗆𝖺𝗀𝖾 𝗍𝗈 𝗎𝗉𝗌𝖼𝖺𝗅𝖾 𝗂𝗍.")
    
    msg = await message.reply("𝖴𝗉𝗌𝖼𝖺𝗅𝗂𝗇𝗀 𝗒𝗈𝗎𝗋 𝗂𝗆𝖺𝗀𝖾...")

    with open(file, "rb") as f:
        imageBytes = f.read()
    os.remove(file)
    
    try:
        upscaledImage = await UpscaleImages(imageBytes)
        await message.reply_document(open(upscaledImage, "rb"), caption=f"ɪᴍᴀɢᴇ ᴜᴘꜱᴄᴀʟᴇᴅ ꜱᴜᴄᴄᴇꜱꜰᴜʟʟʏ")
        await msg.delete()
        os.remove(upscaledImage)
    except Exception as e:
        await msg.edit(f"𝖥𝖺𝗂𝗅𝖾𝖽 𝗍𝗈 𝗎𝗉𝗌𝖼𝖺𝗅𝖾 𝗍𝗁𝖾 𝗂𝗆𝖺𝗀𝖾: {e}")

__module__ = "𝖴𝗉𝗌𝖼𝖺𝗅𝖾"


__help__ = """- **𝖢𝗈𝗆𝗆𝖺𝗇𝖽**:***
  ✧ `/upscale or /enhance <reply>` **:** 𝖱𝖾𝗉𝗅𝗒 𝖳𝗈 𝖠𝗇 𝖨𝗆𝖺𝗀𝖾 𝖶𝗂𝗍𝗁 𝖳𝗁𝗂𝗌 𝖢𝗆𝖽 𝖳𝗈 𝖤𝗇𝗁𝖺𝗇𝖼𝖾.
 """