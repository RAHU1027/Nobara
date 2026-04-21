from pyrogram import Client, filters
from pyrogram.types import Message , InlineKeyboardButton , InlineKeyboardMarkup ,  CallbackQuery
from Nobara.database.filtersdb import remove_filter, get_filters, filter_collection , add_filter , get_filter
from Nobara import app , FILTERS_GROUP
import re
from pyrogram.enums import ParseMode
from Nobara.decorator.chatadmin import chatadmin , chatowner
from config import config
from Nobara.decorator.save import save 
from Nobara.decorator.errors import error


# /filter command
@app.on_message(filters.command("filter" , config.COMMAND_PREFIXES) & filters.group)
@chatadmin
@error
@save
async def filter_command(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("𝖴𝗌𝖺𝗀𝖾:\n`/𝖿𝗂𝗅𝗍𝖾𝗋 𝗍𝗋𝗂𝗀𝗀𝖾𝗋 𝗋𝖾𝗌𝗉𝗈𝗇𝗌𝖾`\n𝖮𝖱\𝗇𝖱𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺 𝗆𝖾𝖽𝗂𝖺 𝗐𝗂𝗍𝗁 `/𝖿𝗂𝗅𝗍𝖾𝗋 𝗍𝗋𝗂𝗀𝗀𝖾𝗋`")
        return

    trigger = message.command[1].lower()

    # Check if message is a reply
    if message.reply_to_message:
        # Handle replied message for saving filter
        if message.reply_to_message.text:
            response = {"type": "text", "content": message.reply_to_message.text}
        elif message.reply_to_message.photo:
            response = {"type": "photo", "file_id": message.reply_to_message.photo.file_id}
        elif message.reply_to_message.video:
            response = {"type": "video", "file_id": message.reply_to_message.video.file_id}
        elif message.reply_to_message.audio:
            response = {"type": "audio", "file_id": message.reply_to_message.audio.file_id}
        elif message.reply_to_message.sticker:
            response = {"type": "sticker", "file_id": message.reply_to_message.sticker.file_id}
        elif message.reply_to_message.animation:
            response = {"type": "animation", "file_id": message.reply_to_message.animation.file_id}
        elif message.reply_to_message.video_note:
            response = {"type": "video_note", "file_id": message.reply_to_message.video_note.file_id}
        elif message.reply_to_message.voice:
            response = {"type": "voice", "file_id": message.reply_to_message.voice.file_id}
        else:
            await message.reply("𝖴𝗇𝗌𝗎𝗉𝗉𝗈𝗋𝗍𝖾𝖽 𝗆𝖾𝖽𝗂𝖺 𝗍𝗒𝗉𝖾. 𝖯𝗅𝖾𝖺𝗌𝖾 𝗎𝗌𝖾 𝗍𝖾𝗑𝗍, 𝗉𝗁𝗈𝗍𝗈, 𝗏𝗂𝖽𝖾𝗈, 𝖺𝗎𝖽𝗂𝗈, 𝗌𝗍𝗂𝖼𝗄𝖾𝗋, 𝗈𝗋 𝖺𝗇𝗂𝗆𝖺𝗍𝗂𝗈𝗇.")
            return

        await add_filter(message.chat.id, [trigger], response)
        await message.reply(f"𝖲𝖺𝗏𝖾𝖽 𝟣 𝖭𝖾𝗐 𝖥𝗂𝗅𝗍𝖾𝗋 𝖨𝗇 {message.chat.title} :\n- `{trigger}`")
    else:
        # Handle command input without reply
        if len(message.command) < 3:
            await message.reply("𝖴𝗌𝖺𝗀𝖾:\n`/𝖿𝗂𝗅𝗍𝖾𝗋 𝗍𝗋𝗂𝗀𝗀𝖾𝗋 𝗋𝖾𝗌𝗉𝗈𝗇𝗌𝖾`")
            return

        response_text = " ".join(message.command[2:])
        response = {"type": "text", "content": response_text}

        await add_filter(message.chat.id, [trigger], response)
        await message.reply(f"𝖲𝖺𝗏𝖾𝖽 𝟣 𝖭𝖾𝗐 𝖥𝗂𝗅𝗍𝖾𝗋 𝖨𝗇 {message.chat.title} :\n- `{trigger}`")


# /stop command
@app.on_message(filters.command("stop" , config.COMMAND_PREFIXES) & filters.group)
@chatadmin
@error
@save
async def stop_filter(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("𝖴𝗌𝖺𝗀𝖾: `/𝗌𝗍𝗈𝗉 𝗍𝗋𝗂𝗀𝗀𝖾𝗋` 𝗍𝗈 𝗋𝖾𝗆𝗈𝗏𝖾 𝖺 𝗌𝗉𝖾𝖼𝗂𝖿𝗂𝖼 𝖿𝗂𝗅𝗍𝖾𝗋.", parse_mode=ParseMode.MARKDOWN)
        return

    trigger = message.command[1].lower()
    chat_id = message.chat.id

    # Check if the trigger exists
    existing_filter = await get_filter(chat_id, trigger)
    if not existing_filter:
        await message.reply(f"𝖭𝗈 𝖿𝗂𝗅𝗍𝖾𝗋 𝖿𝗈𝗎𝗇𝖽 𝖿𝗈𝗋 `{trigger}` 𝗂𝗇 {message.chat.title}.", parse_mode=ParseMode.MARKDOWN)
        return

    # Remove the filter
    await remove_filter(chat_id, trigger)
    await message.reply(f"𝖱𝖾𝗆𝗈𝗏𝖾𝖽 𝟣 𝖥𝗂𝗅𝗍𝖾𝗋 𝖨𝗇 {message.chat.title} :\n- `{trigger}`", parse_mode=ParseMode.MARKDOWN)


# /filters command
@app.on_message(filters.command("filters" , config.COMMAND_PREFIXES) & filters.group)
@chatadmin
@error
@save
async def list_filters(client: Client, message: Message):
    chat_id = message.chat.id

    # Get all filters for the chat
    chat_filters = await get_filters(chat_id)
    if not chat_filters:
        await message.reply(f"𝖫𝗈𝗈𝗄𝗌 𝖫𝗂𝗄𝖾 𝖳𝗁𝖾𝗋𝖾 𝖨𝗌 𝖭𝗈 𝖥𝗂𝗅𝗍𝖾𝗋 𝖲𝖾𝗍 𝖨𝗇 {message.chat.title}")
        return

    # List all filters
    filter_list = "\n".join([f"`{filter_data['triggers'][0]}`" for filter_data in chat_filters])
    await message.reply(f"**𝖠𝗅𝗅 𝖥𝗂𝗅𝗍𝖾𝗋𝗌 𝖲𝖾𝗍 𝖨𝗇 {message.chat.title}:**\n{filter_list}", parse_mode=ParseMode.MARKDOWN)


@app.on_message(filters.command("stopall" , config.COMMAND_PREFIXES) & filters.group)
@chatowner
@error
@save
async def stop_all_filters(client: Client, message: Message):
    chat_id = message.chat.id

    # Send confirmation message with an inline button
    confirmation_buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("𝖢𝗈𝗇𝖿𝗂𝗋𝗆 𝖱𝖾𝗆𝗈𝗏𝖾 𝖠𝗅𝗅 𝖥𝗂𝗅𝗍𝖾𝗋𝗌", callback_data=f"confirm_remove_filters")],
            [InlineKeyboardButton("🗑️", callback_data="cancel")],
        ]
    )
    await message.reply(
        f"𝖠𝗋𝖾 𝗒𝗈𝗎 𝗌𝗎𝗋𝖾 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝗋𝖾𝗆𝗈𝗏𝖾 𝖺𝗅𝗅 𝖿𝗂𝗅𝗍𝖾𝗋𝗌 𝖿𝗋𝗈𝗆 {message.chat.title}?",
        reply_markup=confirmation_buttons,
    )


# CallbackQuery handler for confirming the removal of all filters
@app.on_callback_query(filters.regex("^confirm_remove_filters"))
@chatowner
@error
async def confirm_remove_all(client: Client, callback_query: CallbackQuery):
    try:
        # Extract chat_id from callback_data
        chat_id = callback_query.message.chat.id

        # Remove all filters for the chat
        result = await filter_collection.update_one({"chat_id": chat_id}, {"$unset": {"filters": ""}})
        
        if result.modified_count > 0:
            await callback_query.message.edit_text(f"𝖠𝗅𝗅 𝖿𝗂𝗅𝗍𝖾𝗋𝗌 𝗁𝖺𝗏𝖾 𝖻𝖾𝖾𝗇 𝗋𝖾𝗆𝗈𝗏𝖾𝖽 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖿𝗋𝗈𝗆 {callback_query.message.chat.title}!")
        else:
            await callback_query.message.edit_text(f"𝖭𝗈 𝖿𝗂𝗅𝗍𝖾𝗋𝗌 𝖿𝗈𝗎𝗇𝖽 𝗍𝗈 𝗋𝖾𝗆𝗈𝗏𝖾 𝗂𝗇 {callback_query.message.chat.title}.")

        # Acknowledge the callback
        await callback_query.answer("All filters removed!", show_alert=False)
    except Exception as e:
        # Handle any errors gracefully
        print(f"Error during callback processing: {e}")
        await callback_query.message.edit_text("𝖠𝗇 𝖾𝗋𝗋𝗈𝗋 𝗈𝖼𝖼𝗎𝗋𝗋𝖾𝖽 𝗐𝗁𝗂𝗅𝖾 𝗋𝖾𝗆𝗈𝗏𝗂𝗇𝗀 𝖿𝗂𝗅𝗍𝖾𝗋𝗌.")
        await callback_query.answer("Error occurred!", show_alert=True)

# /mfilter command
@app.on_message(filters.command("mfilter" , config.COMMAND_PREFIXES) & filters.group)
@chatadmin
@error
@save
async def markdown_filter_command(client: Client, message: Message):
    if len(message.command) < 3:
        await message.reply(
            "𝖴𝗌𝖺𝗀𝖾:\n`/𝗆𝖿𝗂𝗅𝗍𝖾𝗋 𝗍𝗋𝗂𝗀𝗀𝖾𝗋 𝗋𝖾𝗌𝗉𝗈𝗇𝗌𝖾_𝗍𝖾𝗆𝗉𝗅𝖺𝗍𝖾`\n\n𝖠𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝗉𝗅𝖺𝖼𝖾𝗁𝗈𝗅𝖽𝖾𝗋𝗌:\n- `{username}`\n- `{first_name}`\n- `{last_name}`\n- `{user_id}`\n- `{mention}`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    trigger = message.command[1].lower()
    response_template = " ".join(message.command[2:])

    response = {"type": "dynamic", "content": response_template}
    await add_filter(message.chat.id, [trigger], response)
    await message.reply(f"𝖲𝖺𝗏𝖾𝖽 𝟣 𝖭𝖾𝗐 𝖥𝗂𝗅𝗍𝖾𝗋 𝖨𝗇 {message.chat.title} :\n- `{trigger}`", parse_mode=ParseMode.MARKDOWN)

# Updated filter response handler
@app.on_message(filters.group & ~ filters.command(["filter" , "mfilter"]), group=FILTERS_GROUP)
@error
@save
async def filter_response(client: Client, message: Message):
    chat_id = message.chat.id
    text = message.text.lower() if message.text else None
    if not text:
        return

    # Split the text into words
    words = re.findall(r'\b\w+\b', text)

    for word in words:
        # Check if the word is a trigger
        filter_response = await get_filter(chat_id, word)
        if filter_response:
            response = filter_response["response"]

            if response["type"] == "text":
                await message.reply(response["content"])
            elif response["type"] == "photo":
                await message.reply_photo(response["file_id"])
            elif response["type"] == "video":
                await message.reply_video(response["file_id"])
            elif response["type"] == "audio":
                await message.reply_audio(response["file_id"])
            elif response["type"] == "sticker":
                await message.reply_sticker(response["file_id"])
            elif response["type"] == "animation":
                await message.reply_animation(response["file_id"])
            elif response["type"] == "voice":
                await message.reply_voice(response["file_id"])
            elif response["type"] == "video_note":
                await message.reply_video_note(response["file_id"])
            elif response["type"] == "markdown":
                await message.reply(response["content"], parse_mode=ParseMode.MARKDOWN)
            elif response["type"] == "dynamic":
                user = message.from_user
                dynamic_content = response["content"].format(
                    username=user.username or "User",
                    first_name=user.first_name or "First Name",
                    last_name=user.last_name or "Last Name",
                    user_id=user.id,
                    mention=user.mention or "User"
                )
                await message.reply(dynamic_content, parse_mode=ParseMode.HTML)
            return  


__module__ = "𝖥𝗂𝗅𝗍𝖾𝗋𝗌"


__help__ = """**𝖴𝗌𝖾𝗋 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌:**
   ✧ `/𝖿𝗂𝗅𝗍𝖾𝗋 <𝗄𝖾𝗒𝗐𝗈𝗋𝖽> <𝗋𝖾𝗉𝗅𝗒 𝗆𝖾𝗌𝗌𝖺𝗀𝖾>`**:** 𝖲𝖾𝗍𝗌 𝖺 𝖿𝗂𝗅𝗍𝖾𝗋 𝗐𝗂𝗍𝗁 𝗍𝗁𝖾 𝗀𝗂𝗏𝖾𝗇 𝗄𝖾𝗒𝗐𝗈𝗋𝖽 𝖺𝗇𝖽 𝗋𝖾𝗉𝗅𝗒 𝗆𝖾𝗌𝗌𝖺𝗀𝖾.
   ✧ `/𝗆𝖿𝗂𝗅𝗍𝖾𝗋 <𝗄𝖾𝗒𝗐𝗈𝗋𝖽> <𝗋𝖾𝗉𝗅𝗒 𝗆𝖾𝗌𝗌𝖺𝗀𝖾>`**:** 𝖲𝖾𝗍𝗌 𝖺 𝖬𝖺𝗋𝗄𝖽𝗈𝗐𝗇 𝖿𝗂𝗅𝗍𝖾𝗋 𝗍𝗁𝖺𝗍 𝗌𝗎𝗉𝗉𝗈𝗋𝗍𝗌 𝖽𝗒𝗇𝖺𝗆𝗂𝖼 𝗉𝗅𝖺𝖼𝖾𝗁𝗈𝗅𝖽𝖾𝗋𝗌.
   ✧ `/𝗌𝗍𝗈𝗉 <𝖿𝗂𝗅𝗍𝖾𝗋 𝗄𝖾𝗒𝗐𝗈𝗋𝖽>`**:** 𝖱𝖾𝗆𝗈𝗏𝖾𝗌 𝗍𝗁𝖾 𝖿𝗂𝗅𝗍𝖾𝗋 𝖺𝗌𝗌𝗈𝖼𝗂𝖺𝗍𝖾𝖽 𝗐𝗂𝗍𝗁 𝗍𝗁𝖾 𝗀𝗂𝗏𝖾𝗇 𝗄𝖾𝗒𝗐𝗈𝗋𝖽.
   ✧ `/𝖿𝗂𝗅𝗍𝖾𝗋𝗌`**:** 𝖫𝗂𝗌𝗍𝗌 𝖺𝗅𝗅 𝖺𝖼𝗍𝗂𝗏𝖾 𝖿𝗂𝗅𝗍𝖾𝗋𝗌 𝗂𝗇 𝗍𝗁𝖾 𝖼𝗁𝖺𝗍.
 
**𝖢𝗁𝖺𝗍 𝖮𝗐𝗇𝖾𝗋 𝗈𝗇𝗅𝗒:**
   ✧ `/𝗌𝗍𝗈𝗉𝖺𝗅𝗅`**:** 𝖱𝖾𝗆𝗈𝗏𝖾𝗌 𝖺𝗅𝗅 𝖿𝗂𝗅𝗍𝖾𝗋𝗌 𝗂𝗇 𝗍𝗁𝖾 𝖼𝗁𝖺𝗍.
 
**𝖣𝗒𝗇𝖺𝗆𝗂𝖼 𝖯𝗅𝖺𝖼𝖾𝗁𝗈𝗅𝖽𝖾𝗋𝗌 𝖿𝗈𝗋 𝖬𝖺𝗋𝗄𝖽𝗈𝗐𝗇 𝖥𝗂𝗅𝗍𝖾𝗋𝗌:**
   - `(𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾)`: 𝖳𝗁𝖾 𝗎𝗌𝖾𝗋'𝗌 𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾.
   - `(𝖿𝗂𝗋𝗌𝗍_𝗇𝖺𝗆𝖾)`: 𝖳𝗁𝖾 𝗎𝗌𝖾𝗋'𝗌 𝖿𝗂𝗋𝗌𝗍 𝗇𝖺𝗆𝖾.
   - `(𝗅𝖺𝗌𝗍_𝗇𝖺𝗆𝖾)`: 𝖳𝗁𝖾 𝗎𝗌𝖾𝗋'𝗌 𝗅𝖺𝗌𝗍 𝗇𝖺𝗆𝖾.
   - `(𝗆𝖾𝗇𝗍𝗂𝗈𝗇)`: 𝖬𝖾𝗇𝗍𝗂𝗈𝗇 𝗍𝗁𝖾 𝗎𝗌𝖾𝗋 𝗐𝗂𝗍𝗁 𝗍𝗁𝖾𝗂𝗋 𝖿𝗂𝗋𝗌𝗍 𝗇𝖺𝗆𝖾.
   - `(𝗎𝗌𝖾𝗋_𝗂𝖽)`: 𝖳𝗁𝖾 𝗎𝗌𝖾𝗋'𝗌 𝗎𝗇𝗂𝗊𝗎𝖾 𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 𝖨𝖣.

 
𝖠𝖽𝗆𝗂𝗇𝗌 𝖺𝗇𝖽 𝗍𝗁𝖾 𝖼𝗁𝖺𝗍 𝗈𝗐𝗇𝖾𝗋 𝖼𝖺𝗇 𝗆𝖺𝗇𝖺𝗀𝖾 𝗍𝗁𝖾𝗌𝖾 𝖿𝗂𝗅𝗍𝖾𝗋𝗌 𝗍𝗈 𝖼𝗈𝗇𝗍𝗋𝗈𝗅 𝖺𝗇𝖽 𝖺𝗎𝗍𝗈𝗆𝖺𝗍𝖾 𝗋𝖾𝗌𝗉𝗈𝗇𝗌𝖾𝗌 𝗂𝗇 𝗍𝗁𝖾 𝖼𝗁𝖺𝗍.
 """