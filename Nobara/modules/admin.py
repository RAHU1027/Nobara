from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message , CallbackQuery , ChatPrivileges
from Nobara.decorator.chatadmin import fetch_admin_privileges ,  chatadmin , can_pin_messages , can_delete_messages , can_promote_members
from pyrogram.enums import ChatMembersFilter , ChatMemberStatus , ChatType , ParseMode
from config import config as c
import time
import re
from Nobara import app , admin_cache , admin_cache_reload , log
from pyrogram.errors import ChatAdminRequired, ChatInvalid , MessageDeleteForbidden , RPCError , UserNotParticipant
from Nobara.helper.user import resolve_user , LOWPROMOTE , PROMOTE , FULLPROMOTE , UNMUTE , MUTE
from Nobara.database.rules_db import get_rules , set_rules ,  clear_rules
import os , asyncio
from Nobara.helper.log_helper import send_log, format_log
from Nobara.decorator.errors import error 
from Nobara.decorator.save import save 
from Nobara.yumeko import CHAT_ADMIN_REQUIRED , USER_ALREADY_PROMOTED , USER_ALREADY_DEMOTED , USER_IS_OWNER 

@app.on_message(filters.command(["reload" , "admincache"] , prefixes=c.COMMAND_PREFIXES) & filters.group)
@chatadmin
@error
@save
async def update_all_admin_cache(client, message: Message):
    chat_id = message.chat.id
    chat_name = message.chat.title
    current_time = time.time()
    if chat_id in admin_cache_reload:
        time_diff = current_time - admin_cache_reload[chat_id]
        if time_diff < 600:
            await message.reply(f"𝖯𝗅𝖾𝖺𝗌𝖾 𝖶𝖺𝗂𝗍 {int(600 - time_diff)} 𝖲𝖾𝖼𝗈𝗇𝖽𝗌 𝖡𝖾𝖿𝗈𝗋𝖾 𝖱𝖾𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝖳𝗁𝖾 𝖠𝖽𝗆𝗂𝗇 𝖢𝖺𝖼𝗁𝖾 𝖠𝗀𝖺𝗂𝗇.")
            return
    try:
        admins = [admin async for admin in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS)]
        for admin in admins:
            user_id = admin.user.id
            privileges = {
                "is_admin": admin.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER],
                "is_owner": admin.status == ChatMemberStatus.OWNER,
                "privileges": admin.privileges if admin.privileges else None,
            }
            admin_cache[(chat_id, user_id)] = privileges
        admin_cache_reload[chat_id] = current_time
        await message.reply(f"𝖨 𝖧𝖺𝗏𝖾 U𝗉𝖽𝖺𝗍𝖾𝖽 𝖬𝗒 𝖠𝖽𝗆𝗂𝗇 𝖢𝖺𝖼𝗁𝖾 𝖥𝗈𝗋 {chat_name}.")
        await send_log(chat_id, await format_log(action="Admin Cache Reloaded", chat=chat_name, admin=message.from_user.first_name))
    except ChatAdminRequired:
        await message.reply(CHAT_ADMIN_REQUIRED)

@app.on_message(filters.command("pin", prefixes=c.COMMAND_PREFIXES) & filters.group)
@app.on_message(filters.regex(r"^Pin It$", flags=re.IGNORECASE) & filters.group & filters.reply)
@can_pin_messages
@error
@save
async def pin_message(client, message: Message):
    try:
        if message.reply_to_message:
            await app.pin_chat_message(chat_id=message.chat.id, message_id=message.reply_to_message.id)
            await message.reply_text("𝖯𝗂𝗇𝗇𝖾𝖽 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒!")
        elif len(message.command) > 1:
            msg_text = message.text.split(None, 1)[1]
            sent_message = await message.reply(msg_text)
            await message.delete()
            await app.pin_chat_message(chat_id=sent_message.chat.id, message_id=sent_message.id)
            await message.reply_text("𝖯𝗂𝗇𝗇𝖾𝖽 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒!")
    except Exception as e:
        print(f"Error: {e}")

@app.on_message(filters.command("unpin" , prefixes=c.COMMAND_PREFIXES) & filters.group)
@app.on_message(filters.regex(r"^Unpin It$", flags=re.IGNORECASE) & filters.group & filters.reply)
@can_pin_messages
@error
@save
async def unpin_message(client, message: Message):
    if message.reply_to_message:
        await app.unpin_chat_message(chat_id=message.chat.id, message_id=message.reply_to_message.id)
        await message.reply_text("𝖬𝖾𝗌𝗌𝖺𝗀𝖾 𝖴𝗇𝗉𝗂𝗇𝗇𝖾𝖽!")

@app.on_message(filters.command(["del" , "delete"] , prefixes=c.COMMAND_PREFIXES) & filters.group)
@app.on_message(filters.regex(r"^(del|delete)$", flags=re.IGNORECASE) & filters.group & filters.reply)
@can_delete_messages
@error
@save
async def delete_message(client, message: Message):
    if message.reply_to_message:
        await message.delete()
        await message.reply_to_message.delete()

@app.on_message(filters.command(["promote" , "makeadmin"], prefixes=c.COMMAND_PREFIXES) & filters.group)
@app.on_message(filters.regex(r"^Promote (him|her)$", flags=re.IGNORECASE) & filters.group & filters.reply)
@can_promote_members
@error
@save
async def promote_user(client, message: Message):
    target_user = await resolve_user(client, message)
    if target_user:
        await app.promote_chat_member(message.chat.id, target_user.id, privileges=PROMOTE)
        await message.reply(f"𝖯𝗋𝗈𝗆𝗈𝗍𝖾𝖽 {target_user.mention}!")

__module__ = "𝖠𝖽𝗆𝗂𝗇"
