# Made with python3
# (C) @JoshephX
# Copyright permission under MIT License
# All rights reserved by JoshephX
# License -> https://github.com/Yuziful/S1l4pbot/blob/main/LICENSE

import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

REMOVEBG_API = os.environ.get("REMOVEBG_API", "")
UNSCREEN_API = os.environ.get("UNSCREEN_API", "")
IMG_PATH = "./DOWNLOADS"

Yuziful = Client(
    "Arxaplan silmə botu",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
)

START_TEXT = """
Salam {},Mən medya arxaplan silmə botuyam.Mənə şəkil göndər və arxaplanını silib sənə göndərim.

Hazırladı: @JoshephX
"""
HELP_TEXT = """
- Sadəcə mənə şəkil göndər
- Mən onu yükləyəcəm
- Və arxa planını silib sənə göndərəcəm
Hazırladı: @JoshephX
"""
ABOUT_TEXT = """
- **Bot :** `Arxaplan silmə botu`
- **Qurucu :** [Fayas](https://telegram.me/JoshephX)
- **Kanal :** [Fayas Noushad](https://telegram.me/Graphsbots)
- **Mənbə :** [Click here](https://github.com/Yuziful/S1l4pbot/tree/main)
- **Dil :** [Python3](https://python.org)
- **Kitabxana :** [Pyrogram](https://pyrogram.org)
- **Server :** [Heroku](https://heroku.com)
"""
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Channel', url='https://telegram.me/Graphsbots'),
        InlineKeyboardButton('Feedback', url='https://telegram.me/JoshephX')
        ],[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ERROR_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Yeniliklər üçün kanala qoşulun', url='https://telegram.me/Graphsbots')
        ]]
    )

@Yuziful.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()

@Yuziful.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )

@Yuziful.on_message(filters.private & (filters.photo | filters.video | filters.document))
async def remove_background(bot, update):
    if not REMOVEBG_API:
        await update.reply_text(
            text="Xəta :- Arxaplan silmədə xəta ",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=ERROR_BUTTONS
        )
        return
    await update.reply_chat_action("typing")
    message = await update.reply_text(
        text="Analiz edilir..",
        quote=True,
        disable_web_page_preview=True
    )
    if update and update.media:
        new_file = PATH + "/" + str(message.from_user.id) + "/"
        if update.photo or (update.document and "image" in update.document.mime_type):
            file_name = new_file + "image.jpg"
            new_file_name = new_file + "no_bg.png"
            await update.download(file_name)
            await message.edit_text(
                text="Şəkil yükləndi.İndi arxaplan silinir..",
                disable_web_page_preview=True
            )
            new_image = removebg_image(file_name)
            if new_image.status_code == 200:
                with open(f"{new_file_name}", "wb") as image:
                    image.write(new_image.content)
            else:
                await update.reply_text(
                    text="API xətalıdır.",
                    quote=True,
                    reply_markup=ERROR_BUTTONS
                )
                return
            await update.reply_chat_action("upload_photo")
            try:
                await update.reply_document(
                    document=new_file_name,
                    quote=True
                )
                await message.delete()
                try:
                    os.remove(file_name)
                except:
                    pass
            except Exception as error:
                print(error)
                await message.edit_text(
                    text="Bir şeylər səhvdir.Yəqin ki APİ limitidir.",
                    disable_web_page_preview=True,
                    reply_markup=ERROR_BUTTONS
                ) 
    else:
        await message.edit_text(
            text="Medya dəstəklənmir",
            disable_web_page_preview=True,
            reply_markup=ERROR_BUTTONS
        )


def removebg_image(file):
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": open(file_name, "rb")},
        data={"size": "auto"},
        headers={"X-Api-Key": REMOVEBG_API}
    )


def removebg_video(file):
    return requests.post(
        "https://api.unscreen.com/v1.0/videos",
        files={"video_file": open(file, "rb")},
        headers={"X-Api-Key": UNSCREEN_API}
    )


Yuziful.run()
