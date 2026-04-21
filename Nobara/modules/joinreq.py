from pyrogram import filters , Client
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.types import CallbackQuery, ChatJoinRequest
from pyrogram.types import InlineKeyboardButton as ikb
from pyrogram.types import InlineKeyboardMarkup as ikm
from Nobara import app , JOIN_UPDATE_GROUP


@app.on_chat_join_request(group=JOIN_UPDATE_GROUP)
async def join_request_handler(c: Client, j: ChatJoinRequest):
    user = j.from_user.id
    userr = j.from_user
    chat = j.chat.id

    txt = "New join request is available\n**USER's INFO**\n"
    txt += f"Name: {userr.full_name}\n"
    txt += f"Mention: {userr.mention}\n"
    txt += f"Id: {user}\n"
    txt += f"Scam: {'True' if userr.is_scam else 'False'}\n"
    if userr.username:
        txt += f"Username: @{userr.username}\n"
    kb = [
        [
            ikb("Accept", f"accept_joinreq_uest_{user}"),
            ikb("Decline", f"decline_joinreq_uest_{user}")
        ]
    ]
    await c.send_message(chat, txt, reply_markup=ikm(kb))
    return


@app.on_callback_query(filters.regex("^accept_joinreq_uest_") | filters.regex("^decline_joinreq_uest_"))
async def accept_decline_request(c: Client, q: CallbackQuery):
    user_id = q.from_user.id
    chat = q.message.chat.id
    try:
        user_status = (await q.message.chat.get_member(user_id)).status
        if user_status not in {CMS.OWNER, CMS.ADMINISTRATOR}:
            await q.answer(
                "You're not even an admin, don't try this explosive shit!",
                show_alert=True,
            )
            return
    except Exception:
        await q.answer("Unknow error occured. You are not admin or owner")
        return
    split = q.data.split("_")
    chat = q.message.chat.id
    user = int(split[-1])
    data = split[0]
    try:
        userr = await c.get_users(user)
    except Exception:
        userr = None
    if data == "accept":
        try:
            await c.approve_chat_join_request(chat, user)
            await q.answer(f"Accepted join request of the {userr.mention if userr else user}", True)
            await q.edit_message_text(f"{q.from_user.mention} accepted join request of {userr.mention if userr else user}")
        except Exception :
            return
    elif data == "decline":
        try:
            await c.decline_chat_join_request(chat, user)
            await q.answer(f"DECLINED: {user}")
            await q.edit_message_text(f"{q.from_user.mention} declined join request of {userr.mention if userr else user}")
        except Exception :
            return
    return


__module__ = "𝖩𝗈𝗂𝗇 𝖱𝖾𝗊𝗎𝖾𝗌𝗍"


__help__ = """**𝖩𝗈𝗂𝗇 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝖬𝖺𝗇𝖺𝗀𝖾𝗆𝖾𝗇𝗍:**

- **𝖮𝗏𝖾𝗋𝗏𝗂𝖾𝗐:**
  𝖳𝗁𝗂𝗌 𝗆𝗈𝖽𝗎𝗅𝖾 𝗁𝖾𝗅𝗉𝗌 𝖺𝖽𝗆𝗂𝗇𝗂𝗌𝗍𝗋𝖺𝗍𝗈𝗋𝗌 𝗆𝖺𝗇𝖺𝗀𝖾 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍𝗌 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉𝗌 𝗐𝗁𝖾𝗋𝖾 𝗍𝗁𝖾 𝖺𝗉𝗉𝗋𝗈𝗏𝖺𝗅 𝗌𝗒𝗌𝗍𝖾𝗆 𝗂𝗌 𝖾𝗇𝖺𝖻𝗅𝖾𝖽.
 
- **𝖥𝗎𝗇𝖼𝗍𝗂𝗈𝗇𝖺𝗅𝗂𝗍𝗒:**
  ✧ 𝖭𝗈𝗍𝗂𝖿𝗂𝖾𝗌 𝗍𝗁𝖾 𝗀𝗋𝗈𝗎𝗉 𝗐𝗁𝖾𝗇 𝖺 𝗇𝖾𝗐 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗂𝗌 𝗋𝖾𝖼𝖾𝗂𝗏𝖾𝖽.
   ✧ 𝖣𝗂𝗌𝗉𝗅𝖺𝗒𝗌 𝗍𝗁𝖾 𝗎𝗌𝖾𝗋'𝗌 𝗂𝗇𝖿𝗈𝗋𝗆𝖺𝗍𝗂𝗈𝗇, 𝗌𝗎𝖼𝗁 𝖺𝗌:
    - 𝖭𝖺𝗆𝖾, 𝗆𝖾𝗇𝗍𝗂𝗈𝗇, 𝖺𝗇𝖽 𝖨𝖣.
     - 𝖲𝖼𝖺𝗆 𝗌𝗍𝖺𝗍𝗎𝗌.
     - 𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾 (𝗂𝖿 𝖺𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾).
   ✧ 𝖯𝗋𝗈𝗏𝗂𝖽𝖾𝗌 𝗂𝗇𝗅𝗂𝗇𝖾 𝖻𝗎𝗍𝗍𝗈𝗇𝗌 𝗍𝗈 𝖾𝗂𝗍𝗁𝖾𝗋 𝖺𝖼𝖼𝖾𝗉𝗍 𝗈𝗋 𝖽𝖾𝖼𝗅𝗂𝗇𝖾 𝗍𝗁𝖾 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍.
 
- **𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌 𝖺𝗇𝖽 𝖥𝖾𝖺𝗍𝗎𝗋𝖾𝗌:**

  ✧ **𝖭𝖾𝗐 𝖩𝗈𝗂𝗇 𝖱𝖾𝗊𝗎𝖾𝗌𝗍:**
    - 𝖶𝗁𝖾𝗇 𝖺 𝗇𝖾𝗐 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗂𝗌 𝖽𝖾𝗍𝖾𝖼𝗍𝖾𝖽, 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗌𝖾𝗇𝖽𝗌 𝖺 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗐𝗂𝗍𝗁 𝗎𝗌𝖾𝗋 𝖽𝖾𝗍𝖺𝗂𝗅𝗌 𝖺𝗇𝖽 𝗈𝗉𝗍𝗂𝗈𝗇𝗌 𝗍𝗈 𝖾𝗂𝗍𝗁𝖾𝗋 𝖺𝖼𝖼𝖾𝗉𝗍 𝗈𝗋 𝖽𝖾𝖼𝗅𝗂𝗇𝖾 𝗍𝗁𝖾 𝗋𝖾𝗊𝗎𝖾𝗌𝗍.
     - 𝖳𝗁𝖾 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗂𝗇𝖼𝗅𝗎𝖽𝖾𝗌 𝗍𝗁𝖾 𝖿𝗈𝗅𝗅𝗈𝗐𝗂𝗇𝗀 𝖻𝗎𝗍𝗍𝗈𝗇𝗌:
      - 𝖠𝖼𝖼𝖾𝗉𝗍: 𝖠𝗉𝗉𝗋𝗈𝗏𝖾𝗌 𝗍𝗁𝖾 𝗎𝗌𝖾𝗋'𝗌 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍.
       - 𝖣𝖾𝖼𝗅𝗂𝗇𝖾: 𝖣𝖾𝖼𝗅𝗂𝗇𝖾𝗌 𝗍𝗁𝖾 𝗎𝗌𝖾𝗋'𝗌 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍.
 
  ✧ **𝖠𝗉𝗉𝗋𝗈𝗏𝖺𝗅/𝖣𝖾𝖼𝗅𝗂𝗇𝖾:**
    - 𝖢𝗅𝗂𝖼𝗄𝗂𝗇𝗀 𝗈𝗇 𝗍𝗁𝖾 "𝖠𝖼𝖼𝖾𝗉𝗍" 𝖻𝗎𝗍𝗍𝗈𝗇 𝖺𝗉𝗉𝗋𝗈𝗏𝖾𝗌 𝗍𝗁𝖾 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍.
     - 𝖢𝗅𝗂𝖼𝗄𝗂𝗇𝗀 𝗈𝗇 𝗍𝗁𝖾 "𝖣𝖾𝖼𝗅𝗂𝗇𝖾" 𝖻𝗎𝗍𝗍𝗈𝗇 𝗋𝖾𝗃𝖾𝖼𝗍𝗌 𝗍𝗁𝖾 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍.
     - 𝖮𝗇𝗅𝗒 𝖺𝖽𝗆𝗂𝗇𝗂𝗌𝗍𝗋𝖺𝗍𝗈𝗋𝗌 𝗈𝗋 𝗈𝗐𝗇𝖾𝗋𝗌 𝖼𝖺𝗇 𝗍𝖺𝗄𝖾 𝗍𝗁𝖾𝗌𝖾 𝖺𝖼𝗍𝗂𝗈𝗇𝗌.
     - 𝖭𝗈𝗇-𝖺𝖽𝗆𝗂𝗇𝗌 𝖺𝗍𝗍𝖾𝗆𝗉𝗍𝗂𝗇𝗀 𝗍𝗈 𝗂𝗇𝗍𝖾𝗋𝖺𝖼𝗍 𝗐𝗂𝗍𝗁 𝗍𝗁𝖾 𝖻𝗎𝗍𝗍𝗈𝗇𝗌 𝗐𝗂𝗅𝗅 𝗋𝖾𝖼𝖾𝗂𝗏𝖾 𝖺𝗇 𝖺𝗅𝖾𝗋𝗍.
 
"""
