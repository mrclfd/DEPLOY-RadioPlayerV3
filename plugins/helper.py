"""
RadioPlayerV3, Telegram Voice Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import asyncio
from pyrogram import Client, filters, emoji
from utils import USERNAME, mp
from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

msg=Config.msg
CHAT=Config.CHAT
ADMINS=Config.ADMINS
playlist=Config.playlist

HOME_TEXT = "👋🏻 **Hai [{}](tg://user?id={})**,\n\nSaya **Gentho Music Bot** \nSaya Dapat Memutar Radio / Musik / Siaran Langsung YouTube di Channel & Group 24x7 Nonstop."
HELP_TEXT = """
**BANTUAN PENGGUNAAN PERINTAH**

--**Perintah Umum**-- :
\u2022 `/play` - membalas audio atau tautan YouTube untuk memutarnya atau menggunakan `/play [judul lagu]`
\u2022 `/help` - menunjukkan bantuan untuk perintah
\u2022 `/song` [judul lagu] - unduh lagu sebagai trek audio
\u2022 `/current` - menunjukkan waktu pemutaran trek saat ini
\u2022 `/playlist` - menunjukkan daftar putar saat ini dengan kontrol

--**Perintah Khusus Admin**-- :
\u2022 `/radio` - mulai siaran radio
\u2022 `/stopradio` - hentikan siaran radio
\u2022 `/skip` - lewati musik yang sedang diputar
\u2022 `/join` - bergabung ke obrolan suara
\u2022 `/leave` - keluar dari obrolan suara
\u2022 `/stop` - berhenti memutar musik
\u2022 `/volume` - atur volume (0-200)
\u2022 `/replay` - putar dari awal
\u2022 `/clean` - bersihkan cache
\u2022 `/pause` - jeda memutar musik
\u2022 `/resume` - lanjutkan memutar musik
\u2022 `/mute` - bisukan obrolan suara userbot
\u2022 `/unmute` - suarakan obrolan suara userbot
\u2022 `/restart` - perbarui & mulai ulang bot

© **Bot Based on [AsmSafone](https://github.com/AsmSafone)**
"""


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.from_user.id not in Config.ADMINS and query.data != "help":
        await query.answer(
            "Anda Tidak Diizinkan!",
            show_alert=True
            )
        return
    else:
        await query.answer()
    if query.data == "replay":
        group_call = mp.group_call
        if not playlist:
            return
        group_call.restart_playout()
        if not playlist:
            pl = f"{emoji.NO_ENTRY} **Daftar Putar Kosong!**"
        else:
            pl = f"{emoji.PLAY_BUTTON} **Daftar putar**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Permintaan dari:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(
                f"{pl}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏸", callback_data="pause"),
                            InlineKeyboardButton("⏭", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    elif query.data == "pause":
        if not playlist:
            return
        else:
            mp.group_call.pause_playout()
            pl = f"{emoji.PLAY_BUTTON} **Daftar putar**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  **Permintaan dari:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} **Dijeda!**\n\n{pl}",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("▶️", callback_data="resume"),
                            InlineKeyboardButton("⏭", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    elif query.data == "resume":   
        if not playlist:
            return
        else:
            mp.group_call.resume_playout()
            pl = f"{emoji.PLAY_BUTTON} **Daftar putar**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Permintaan dari:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} **Dilanjutkan!**\n\n{pl}",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏸", callback_data="pause"),
                            InlineKeyboardButton("⏭", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    elif query.data=="skip":   
        if not playlist:
            return
        else:
            await mp.skip_current_playing()
            pl = f"{emoji.PLAY_BUTTON} **Daftar putar**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Permintaan dari:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} **Dilewati!**\n\n{pl}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔄", callback_data="replay"),
                        InlineKeyboardButton("⏸", callback_data="pause"),
                        InlineKeyboardButton("⏭", callback_data="skip")
                            
                    ],
                ]
            )
        )
        except:
            pass
    elif query.data=="help":
        buttons = [
            [
                InlineKeyboardButton("OWNER", url="https://t.me/ngeringerong"),
                InlineKeyboardButton("GROUP", url="https://t.me/bermusikria"),
            ],
            [
                InlineKeyboardButton("TUTUP PESAN", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            HELP_TEXT,
            reply_markup=reply_markup

        )

    elif query.data=="close":
        await query.message.delete()


@Client.on_message(filters.command(["start", f"start@{USERNAME}"]))
async def start(client, message):
    buttons = [
             [
                InlineKeyboardButton("OWNER", url="https://t.me/ngeringerong"),
                InlineKeyboardButton("GROUP", url="https://t.me/bermusikria"),
            ],
            [
                InlineKeyboardButton("CARA PENGGUNAAN", callback_data="help"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    m=await message.reply_photo(photo="https://telegra.ph/file/5a00f37d0a84d381f0e57.jpg", caption=HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    await mp.delete(m)
    await mp.delete(message)


@Client.on_message(filters.command(["help", f"help@{USERNAME}"]))
async def help(client, message):
    buttons = [
            [
                InlineKeyboardButton("OWNER", url="https://t.me/ngeringerong"),
                InlineKeyboardButton("GROUP", url="https://t.me/bermusikria"),
            ],
            [
                InlineKeyboardButton("TUTUP PESAN", callback_data="close", show_alert=True),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    if msg.get('help') is not None:
        await msg['help'].delete()
    msg['help'] = await message.reply_photo(photo="https://telegra.ph/file/5a00f37d0a84d381f0e57.jpg", caption=HELP_TEXT, reply_markup=reply_markup)
    await mp.delete(message)

