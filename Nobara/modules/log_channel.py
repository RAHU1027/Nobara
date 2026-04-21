from pyrogram import Client, filters
from pyrogram.types import Message
from Nobara.database.log_channel_db import set_log_channel, get_log_channel, remove_log_channel
from Nobara import app , LOG_GROUP , CHAT_MEMBER_LOG_GROUP
from Nobara.decorator.chatadmin import can_change_info
from Nobara.helper.log_helper import format_log
from pyrogram.types import ChatMemberUpdated
from pyrogram.enums import ChatMemberStatus
from config import config
from Nobara.decorator.save import save 
from Nobara.decorator.errors import error

logchannelsetting_state = {}

@app.on_message(filters.command("setlog" , prefixes=config.COMMAND_PREFIXES) & filters.group)
@can_change_info
@error
@save
async def set_log_channel_command(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check if a log channel is already set
    current_log_channel = await get_log_channel(chat_id)
    if current_log_channel:
        # Fetch the title of the current log channel
        log_channel_title = await get_chat_title(client, current_log_channel)
        await message.reply_text(
            f"𝖠 𝗅𝗈𝗀 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗂𝗌 𝖺𝗅𝗋𝖾𝖺𝖽𝗒 𝖼𝗈𝗇𝖿𝗂𝗀𝗎𝗋𝖾𝖽 𝖿𝗈𝗋 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉: **{log_channel_title}**.\n\n"
            f"𝖳𝗈 𝖼𝗁𝖺𝗇𝗀𝖾 𝗂𝗍, 𝗉𝗅𝖾𝖺𝗌𝖾 𝗋𝖾𝗌𝖾𝗍 𝗍𝗁𝖾 𝖼𝗎𝗋𝗋𝖾𝗇𝗍 𝗅𝗈𝗀 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗎𝗌𝗂𝗇𝗀 𝗍𝗁𝖾 /𝖼𝗅𝖾𝖺𝗋𝗅𝗈𝗀 𝖼𝗈𝗆𝗆𝖺𝗇𝖽."
        )
        return

    # Add user to log channel setup state
    logchannelsetting_state[(chat_id, user_id)] = True

    await message.reply_text(
        "𝖴𝗇𝖽𝖾𝗋𝗌𝗍𝗈𝗈𝖽! 𝖯𝗅𝖾𝖺𝗌𝖾 𝗆𝖺𝗄𝖾 𝗆𝖾 𝖺𝗇 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝖾 𝖽𝖾𝗌𝗂𝗋𝖾𝖽 𝗅𝗈𝗀 𝖼𝗁𝖺𝗇𝗇𝖾𝗅. 𝖮𝗇𝖼𝖾 𝖽𝗈𝗇𝖾,"
        "𝗌𝖾𝗇𝖽 𝖺𝗇𝗒 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗍𝗈 𝗍𝗁𝖺𝗍 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝖺𝗇𝖽 𝖿𝗈𝗋𝗐𝖺𝗋𝖽 𝗂𝗍 𝗁𝖾𝗋𝖾. 𝖳𝗁𝗂𝗌 𝗐𝗂𝗅𝗅 𝖺𝗅𝗅𝗈𝗐 𝗆𝖾 𝗍𝗈 𝗅𝗂𝗇𝗄 𝗍𝗁𝖾 𝗅𝗈𝗀 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗍𝗈 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉."
    )


async def get_chat_title(client: Client, chat_id: int) -> str:
    """Fetch and return the title of a chat."""
    try:
        chat = await client.get_chat(chat_id)
        return chat.title or "Unknown Chat"
    except Exception as e:
        return "Unknown Chat"


# Listener for forwarded messages to detect log channel
@app.on_message(filters.forwarded & filters.group , group=LOG_GROUP)
@error
@save
async def detect_log_channel(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not message.from_user :
        return

    # Check if the user is in log channel setting state
    if not logchannelsetting_state.get((chat_id, user_id)):
        return

    original_chat_id = message.forward_from_chat.id if message.forward_from_chat else None
    if not original_chat_id:
        await message.reply_text("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝗅𝗈𝗀 𝖼𝗁𝖺𝗇𝗇𝖾𝗅. 𝖯𝗅𝖾𝖺𝗌𝖾 𝗍𝗋𝗒 𝖺𝗀𝖺𝗂𝗇.")
        return

    # Verify bot is an admin in the channel
    try:
        member = await client.get_chat_member(original_chat_id, "me")
        if not member.privileges.can_post_messages:
            await message.reply_text(
                "𝖨 𝗇𝖾𝖾𝖽 𝗍𝗈 𝖻𝖾 𝖺𝗇 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝖾 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗐𝗂𝗍𝗁 𝗉𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇 𝗍𝗈 𝗉𝗈𝗌𝗍 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌."
            )
            return
    except Exception as e:
        await message.reply_text(f"Error: {e}")
        return

    # Save the log channel ID to the database
    await set_log_channel(chat_id, original_chat_id)
    del logchannelsetting_state[(chat_id, user_id)]  # Remove from state
    await message.reply_text(
        f"𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗌𝖾𝗍 𝗍𝗁𝖾 𝗅𝗈𝗀 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝖿𝗈𝗋 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗍 𝗍𝗈 {message.forward_from_chat.title}."
    )

# Command to clear log channel
@app.on_message(filters.command("clearlog" , prefixes=config.COMMAND_PREFIXES) & filters.group)
@can_change_info
@error
@save
async def clear_log_channel_command(client: Client, message: Message):
    chat_id = message.chat.id

    # Check if log channel is set
    current_log_channel = await get_log_channel(chat_id)
    if not current_log_channel:
        await message.reply_text("𝖭𝗈 𝗅𝗈𝗀 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗂𝗌 𝖼𝗎𝗋𝗋𝖾𝗇𝗍𝗅𝗒 𝗌𝖾𝗍 𝖿𝗈𝗋 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗍.")
        return

    # Clear the log channel
    await remove_log_channel(chat_id)
    await message.reply_text("𝖳𝗁𝖾 𝗅𝗈𝗀 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗁𝖺𝗌 𝖻𝖾𝖾𝗇 𝖼𝗅𝖾𝖺𝗋𝖾𝖽. 𝖸𝗈𝗎 𝖼𝖺𝗇 𝗌𝖾𝗍 𝖺 𝗇𝖾𝗐 𝗈𝗇𝖾 𝗎𝗌𝗂𝗇𝗀 /𝗌𝖾𝗍𝗅𝗈𝗀.")


@app.on_chat_member_updated(~filters.me,group=CHAT_MEMBER_LOG_GROUP)
@error
@save
async def log_chat_member_updates(client: Client, chat_member_updated: ChatMemberUpdated): 
    try :
            chat_id = chat_member_updated.chat.id
        
            # Get the log channel ID
            log_channel_id = await get_log_channel(chat_id)
            if not log_channel_id:
                return  # No log channel set, skip logging
        
            # Determine if the event is a join or leave
            old_status = chat_member_updated.old_chat_member.status if chat_member_updated.old_chat_member else None
            new_status = chat_member_updated.new_chat_member.status
        
            if old_status in {None, ChatMemberStatus.LEFT} and new_status == ChatMemberStatus.MEMBER:
                # User joined or rejoined the chat
                action = "Member Joined"
                user = chat_member_updated.new_chat_member.user
                log_message = await format_log(
                    action=action,
                    chat=chat_member_updated.chat.title or "Unknown Chat",
                    user=f"{user.first_name} {user.last_name or ''} (@{user.username or 'N/A'})"
                )
            
            elif old_status == ChatMemberStatus.MEMBER and new_status in {ChatMemberStatus.LEFT, None}:
                # User left the chat
                action = "Member Left"
                user = chat_member_updated.old_chat_member.user
                log_message = await format_log(
                    action=action,
                    chat=chat_member_updated.chat.title or "Unknown Chat",
                    user=f"{user.first_name} {user.last_name or ''} (@{user.username or 'N/A'})"
                )
            else:
                return  # No relevant status change, skip logging
        
            # Send the log message to the log channel
            try:
                await app.send_message(log_channel_id, log_message, disable_web_page_preview=True)
            except Exception as e:
                print(f"Error sending log: {e}")
    except Exception:
        return
    
__module__ = "𝖫𝗈𝗀 𝖢𝗁𝖺𝗇𝗇𝖾𝗅"


__help__ = """**𝖫𝗈𝗀 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖬𝖺𝗇𝖺𝗀𝖾𝗆𝖾𝗇𝗍 :**

- **𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌:**

 ✧ `/𝗌𝖾𝗍𝗅𝗈𝗀` : 𝖫𝗂𝗇𝗄 𝖺 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗍𝗈 𝗍𝗁𝖾 𝗀𝗋𝗈𝗎𝗉 𝖿𝗈𝗋 𝗅𝗈𝗀𝗀𝗂𝗇𝗀 𝗂𝗆𝗉𝗈𝗋𝗍𝖺𝗇𝗍 𝖾𝗏𝖾𝗇𝗍𝗌 𝗅𝗂𝗄𝖾 𝗆𝖾𝗆𝖻𝖾𝗋 𝗃𝗈𝗂𝗇𝗌, 𝗅𝖾𝖺𝗏𝖾𝗌, 𝖾𝗍𝖼.
     - 𝖳𝗁𝖾 𝖻𝗈𝗍 𝗐𝗂𝗅𝗅 𝗀𝗎𝗂𝖽𝖾 𝗒𝗈𝗎 𝗍𝗈 𝖿𝗈𝗋𝗐𝖺𝗋𝖽 𝖺 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝖿𝗋𝗈𝗆 𝗍𝗁𝖾 𝖽𝖾𝗌𝗂𝗋𝖾𝖽 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗍𝗈 𝗌𝖾𝗍 𝗂𝗍 𝗎𝗉.
     - 𝖤𝗇𝗌𝗎𝗋𝖾 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗁𝖺𝗌 𝖺𝖽𝗆𝗂𝗇 𝗋𝗂𝗀𝗁𝗍𝗌 𝗂𝗇 𝗍𝗁𝖾 𝗍𝖺𝗋𝗀𝖾𝗍 𝖼𝗁𝖺𝗇𝗇𝖾𝗅.
     
 ✧ `/𝖼𝗅𝖾𝖺𝗋𝗅𝗈𝗀` : 𝖴𝗇𝗅𝗂𝗇𝗄 𝗍𝗁𝖾 𝖼𝗎𝗋𝗋𝖾𝗇𝗍𝗅𝗒 𝗌𝖾𝗍 𝗅𝗈𝗀 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝖿𝗈𝗋 𝗍𝗁𝖾 𝗀𝗋𝗈𝗎𝗉.
 
- **𝖥𝗎𝗇𝖼𝗍𝗂𝗈𝗇𝖺𝗅𝗂𝗍𝗒:**

 ✧ 𝖮𝗇𝖼𝖾 𝖺 𝗅𝗈𝗀 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗂𝗌 𝗌𝖾𝗍, 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗐𝗂𝗅𝗅 𝗅𝗈𝗀 𝗄𝖾𝗒 𝖾𝗏𝖾𝗇𝗍𝗌 𝗂𝗇 𝗍𝗁𝖾 𝗀𝗋𝗈𝗎𝗉 𝗍𝗈 𝗍𝗁𝖾 𝗅𝗂𝗇𝗄𝖾𝖽 𝖼𝗁𝖺𝗇𝗇𝖾𝗅.
  ✧ 𝖫𝗈𝗀𝗀𝖾𝖽 𝖾𝗏𝖾𝗇𝗍𝗌 𝗂𝗇𝖼𝗅𝗎𝖽𝖾:
    - 𝖬𝖾𝗆𝖻𝖾𝗋𝗌 𝗃𝗈𝗂𝗇𝗂𝗇𝗀 𝗈𝗋 𝗅𝖾𝖺𝗏𝗂𝗇𝗀 𝗍𝗁𝖾 𝗀𝗋𝗈𝗎𝗉.
     - 𝖮𝗍𝗁𝖾𝗋 𝖺𝖽𝗆𝗂𝗇𝗂𝗌𝗍𝗋𝖺𝗍𝗂𝗏𝖾 𝖺𝖼𝗍𝗂𝗏𝗂𝗍𝗂𝖾𝗌 (𝗂𝖿 𝖼𝗈𝗇𝖿𝗂𝗀𝗎𝗋𝖾𝖽).
 """
