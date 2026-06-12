from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from Nobara.decorator.chatadmin import can_restrict_members
from pyrogram.enums import ChatMemberStatus
from config import config as c
from Nobara import app 
from pyrogram.errors import ChatAdminRequired, UserNotParticipant
from Nobara.helper.user import resolve_user
from datetime import datetime, timedelta
from Nobara.helper.log_helper import send_log, format_log
from Nobara.decorator.errors import error 
from Nobara.decorator.save import save
from Nobara.yumeko import CHAT_ADMIN_REQUIRED, USER_ALREADY_BANNED, USER_NOT_BANNED, USER_IS_ADMIN, USER_IS_OWNER
import json
import re

def load_sudoers():
    with open("sudoers.json", "r") as f:
        return json.load(f)

def get_privileged_users():
    sudoers = load_sudoers()
    return (
        sudoers.get("Hokages", []) +
        sudoers.get("Jonins", []) +
        sudoers.get("Chunins", [])
    )

@app.on_message(filters.command(["ban", "fuck"], prefixes=c.COMMAND_PREFIXES) & filters.group)
@app.on_message(filters.regex(r"^(Ban|Fuck) (him|her)$", flags=re.IGNORECASE) & filters.group & filters.reply)
@can_restrict_members
@error
@save
async def ban_user(client: app, message: Message):
    chat_id = message.chat.id
    if not message.from_user: return
    target_user = None
    reason = None

    if message.reply_to_message:
        target_user = await resolve_user(client, message)
        args = message.text.split(maxsplit=1)
        if len(args) > 1: reason = args[1]
    else:
        args = message.text.split(maxsplit=2)
        if len(args) > 1: target_user = await resolve_user(client, message)
        if len(args) > 2: reason = args[2]

    if not target_user:
        await message.reply("𝖴𝗇𝖺𝖻𝗅𝖾 𝗍𝗈 𝖿𝗂𝗇𝖽 𝗍𝗁𝖾 𝗌𝗉𝖾𝖼𝗂𝖿𝗂𝖾𝖽 𝗎𝗌𝖾𝗋.")
        return

    try:
        x = await app.get_chat_member(chat_id, target_user.id)
        if x.status == ChatMemberStatus.OWNER: await message.reply(USER_IS_OWNER); return
        if x.status == ChatMemberStatus.ADMINISTRATOR: await message.reply(USER_IS_ADMIN); return
        if x.status == ChatMemberStatus.BANNED: await message.reply(USER_ALREADY_BANNED); return
        if target_user.id in get_privileged_users(): return

        await app.ban_chat_member(chat_id=chat_id, user_id=target_user.id)
        msg = f"✪ **𝖡𝖺𝗇 𝖤𝖵𝖤𝖭𝖳**\n\n👤 **𝖴𝗌𝖾𝗋:** {target_user.mention()}\n⬆️ **𝖡𝖺𝗇𝗇𝖾𝖽 𝖡𝗒:** {message.from_user.mention()}"
        if reason: msg += f"\n📝 **𝖱𝖾𝖺𝗌𝗈𝗇:** {reason}"
        
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("𝖴𝗇𝖻𝖺𝗇", callback_data=f"unban:{target_user.id}")], [InlineKeyboardButton("🗑️", callback_data="delete")]])
        await message.reply(msg, reply_markup=buttons)
        await send_log(chat_id, await format_log(action="Ban", chat=message.chat.title, admin=message.from_user.mention(), user=target_user.mention()))
    except Exception as e:
        await message.reply(f"𝖤𝗋𝗋𝗈𝗋: {e}")

@app.on_callback_query(filters.regex(r"^unban:(\d+)$"))
@can_restrict_members
@error
async def unban_callback(client: app, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split(":")[1])
    chat_id = callback_query.message.chat.id
    await app.unban_chat_member(chat_id, user_id)
    await callback_query.answer("𝖴𝗇𝖻𝖺𝗇𝗇𝖾𝖽!")
    await callback_query.message.edit_text("𝖴𝗌𝖾𝗋 𝖴𝗇𝖻𝖺𝗇𝗇𝖾𝖽.")

@app.on_message(filters.command("unban", prefixes=c.COMMAND_PREFIXES) & filters.group)
@app.on_message(filters.regex(r"^Unban (him|her)$", flags=re.IGNORECASE) & filters.group & filters.reply)
@can_restrict_members
@error
@save
async def unban_user(client: app, message: Message):
    target_user = await resolve_user(client, message)
    if not target_user: return
    await app.unban_chat_member(message.chat.id, target_user.id)
    await message.reply(f"𝖴𝗇𝖻𝖺𝗇𝗇𝖾𝖽 {target_user.mention}!")

@app.on_message(filters.command(["kickme", "banme"], prefixes=c.COMMAND_PREFIXES) & filters.group)
@error
@save
async def self_ban(client: app, message: Message):
    await app.ban_chat_member(message.chat.id, message.from_user.id)
    await message.reply("𝖮𝗄𝖺𝗒 𝖥𝗎𝖼𝗄 𝖮𝖿𝖿 !!")

@app.on_message(filters.command("sban", prefixes=c.COMMAND_PREFIXES) & filters.group)
@can_restrict_members
@error
@save
async def silent_ban(client: app, message: Message):
    target = await resolve_user(client, message)
    if target: 
        await app.ban_chat_member(message.chat.id, target.id)
        await message.delete()

@app.on_message(filters.command(["dban", "dfuck"], prefixes=c.COMMAND_PREFIXES) & filters.group)
@can_restrict_members
@error
@save
async def dban(client: app, message: Message):
    target = await resolve_user(client, message)
    if target:
        await app.ban_chat_member(message.chat.id, target.id)
        await message.reply_to_message.delete()
        await message.reply(f"𝖡𝖺𝗇𝗇𝖾𝖽 {target.mention}!")
