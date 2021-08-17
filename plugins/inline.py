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
from pyrogram.handlers import InlineQueryHandler
from youtubesearchpython import VideosSearch
from utils import USERNAME
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, errors
from config import Config

REPLY_MESSAGE=Config.REPLY_MESSAGE
buttons = [
            [
                InlineKeyboardButton("❔ CARA PENGGUNAAN ❔", callback_data="help"),
            ],
            [
                InlineKeyboardButton("OWNER", url="https://t.me/ngeringerong"),
                InlineKeyboardButton("GROUP", url="https://t.me/bermusikria"),
            ],
            [
                InlineKeyboardButton("GABUT? SINI JOIN!", url="https://t.me/AnonyMeetChat"),
            ]
         ]


@Client.on_inline_query()
async def search(client, query):
    answers = []
    if query.query == "P":
        answers.append(
            InlineQueryResultArticle(
                title="Bio ini ditulis oleh tangan yang belum pernah kamu genggam.",
                thumb_url="https://telegra.ph/file/5a00f37d0a84d381f0e57.jpg",
                input_message_content=InputTextMessageContent(f"{REPLY_MESSAGE}\n\n<b>© Powered by railway.app</b>", disable_web_page_preview=True),
                reply_markup=InlineKeyboardMarkup(buttons)
                )
            )
        await query.answer(results=answers, cache_time=0)
        return
    string = query.query.lower().strip().rstrip()
    if string == "":
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text=("Ketik Nama Lagu?"),
            switch_pm_parameter="help",
            cache_time=0
        )
    else:
        videosSearch = VideosSearch(string.lower(), limit=50)
        for v in videosSearch.result()["result"]:
            answers.append(
                InlineQueryResultArticle(
                    title=v["title"],
                    description=("Durasi: {} Penonton: {}").format(
                        v["duration"],
                        v["viewCount"]["short"]
                    ),
                    input_message_content=InputTextMessageContent(
                        "/play https://www.youtube.com/watch?v={}".format(
                            v["id"]
                        )
                    ),
                    thumb_url=v["thumbnails"][0]["url"]
                )
            )
        try:
            await query.answer(
                results=answers,
                cache_time=0
            )
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text=("Error: Waktu Pencarian Habis!"),
                switch_pm_parameter="",
            )


__handlers__ = [
    [
        InlineQueryHandler(
            search
        )
    ]
]
