import asyncio
from openai import OpenAI
from pyrogram import Client, filters
from pyrogram.types import Message
from Nobara import app
from config import config
from Nobara.decorator.save import save 
from Nobara.decorator.errors import error
from lexica import Client as LexicaClient, languageModels

# Initialize OpenAI client
openai_client = OpenAI(api_key=config.OPENAI_KEY)
MODEL = "gpt-3.5-turbo"


def askgemini(prompt: str) -> dict:
    client = LexicaClient()
    response = client.ChatCompletion(prompt, languageModels.gemini)
    return response

@app.on_message(filters.command("askgpt" , config.COMMAND_PREFIXES))
@error
@save
async def ask_openai(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("𝖴𝗌𝖺𝗀𝖾: /𝖺𝗌𝗄𝗀𝗉𝗍 <𝗉𝗋𝗈𝗆𝗉𝗍>")
        return

    prompt = message.text.split(maxsplit=1)[1]
    processing_message = await message.reply("💭 𝖳𝗁𝗂𝗇𝗄𝗂𝗇𝗀... 𝖯𝗅𝖾𝖺𝗌𝖾 𝗐𝖺𝗂𝗍")

    try:
        # Call OpenAI API for a streaming response
        stream = openai_client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            stream=True,
        )

        response_text = ""
        last_edit_time = 0  # Track the time of the last message edit
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                response_text += content

                # Only edit the message if enough time has passed
                current_time = asyncio.get_event_loop().time()
                if current_time - last_edit_time > 2:  # Edit every 1.5 seconds
                    await processing_message.edit(response_text)
                    last_edit_time = current_time

        # Ensure final response is updated
        if response_text.strip():
            await processing_message.edit(response_text.strip())
        else:
            await processing_message.edit("𝖨 𝖼𝗈𝗎𝗅𝖽𝗇'𝗍 𝗀𝖾𝗇𝖾𝗋𝖺𝗍𝖾 𝖺 𝗋𝖾𝗌𝗉𝗈𝗇𝗌𝖾. 𝖯𝗅𝖾𝖺𝗌𝖾 𝗍𝗋𝗒 𝖺𝗀𝖺𝗂𝗇.")

    except Exception as e:
        print(e)
        await processing_message.edit(f"𝖠𝗇 𝖾𝗋𝗋𝗈𝗋 𝗈𝖼𝖼𝗎𝗋𝗋𝖾𝖽 : {e}")
 

# /ask command handler
@app.on_message(filters.command("askgemini", config.COMMAND_PREFIXES))
async def ask_handler(client, message):
    try:
        # Get the query after the command
        query = " ".join(message.command[1:])
        if not query:
            await message.reply_text("Please provide a prompt after the /askgemini command.")
            return

        # Call the Lexica API
        a = await message.reply_text("💭")
        response = askgemini(query)
        content = response["content"][0]["text"] 
        
        # Format and send the response
        if response:
            await a.edit_text(f"**Response:**\n{content}")
        else:
            await a.edit_text("No response from the Gemini.")
    except Exception as e:
        await a.edit_text(f"An error occurred")
        

__module__ = "𝖠𝗌𝗄"
__help__ = """✧ /askgpt <prompt> : 𝖴𝗌𝖾 𝖦𝖯𝖳-3.5-𝗍𝗎𝗋𝖻𝗈 𝗍𝗈 𝗀𝖾𝗇𝖾𝗋𝖺𝗍𝖾 𝗋𝖾𝗌𝗉𝗈𝗇𝗌𝖾𝗌.
✧ /askgemini <prompt> : 𝖴𝗌𝖾 𝖫𝖾𝗑𝗂𝖼𝖺'𝗌 𝖦𝖾𝗆𝗂𝗇𝗂 𝗅𝖺𝗇𝗀𝗎𝖺𝗀𝖾 𝗆𝗈𝖽𝖾𝗅 𝗍𝗈 𝗀𝖾𝗇𝖾𝗋𝖺𝗍𝖾 𝗋𝖾𝗌𝗉𝗈𝗇𝗌𝖾𝗌."""
