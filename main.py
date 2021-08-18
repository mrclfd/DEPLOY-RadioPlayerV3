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

import os
import sys
import asyncio
import subprocess
from threading import Thread
from signal import SIGINT
from pyrogram import Client, filters, idle
from config import Config
from utils import mp, USERNAME, FFMPEG_PROCESSES
from pyrogram.raw import functions, types

CHAT=Config.CHAT
ADMINS=Config.ADMINS
LOG_GROUP=Config.LOG_GROUP

bot = Client(
    "RadioPlayer",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins")
)
if not os.path.isdir("./downloads"):
    os.makedirs("./downloads")
async def main():
    async with bot:
        await mp.start_radio()

def stop_and_restart():
    bot.stop()
    os.system("git pull")
    os.execl(sys.executable, sys.executable, *sys.argv)


bot.run(main())
bot.start()
print("\n\n@GenthoMusicBot Berjalan!")
bot.send(
    functions.bots.SetBotCommands(
        commands=[
            types.BotCommand(
                command="start",
                description="Mulai Bot"
            ),
            types.BotCommand(
                command="help",
                description="Tampilkan Pesan Bantuan"
            ),
            types.BotCommand(
                command="play",
                description="Putar Musik Dari YouTube"
            ),
            types.BotCommand(
                command="song",
                description="Unduh Musik Sebagai Audio"
            ),
            types.BotCommand(
                command="skip",
                description="Lewati Musik Saat Ini"
            ),
            types.BotCommand(
                command="pause",
                description="Jeda Musik Saat Ini"
            ),
            types.BotCommand(
                command="resume",
                description="Lanjutkan Musik yang Dijeda"
            ),
            types.BotCommand(
                command="radio",
                description="Mulai Radio/Siaran langsung"
            ),
            types.BotCommand(
                command="current",
                description="Tampilkan Lagu yang Sedang Diputar"
            ),
            types.BotCommand(
                command="playlist",
                description="Tampilkan Daftar Putar Saat Ini"
            ),
            types.BotCommand(
                command="join",
                description="Gabung Ke Obrolan Suara"
            ),
            types.BotCommand(
                command="leave",
                description="Keluar Dari Obrolan Suara"
            ),
            types.BotCommand(
                command="stop",
                description="Berhenti Memutar Musik"
            ),
            types.BotCommand(
                command="stopradio",
                description="Hentikan Radio/Siaran Langsung"
            ),
            types.BotCommand(
                command="replay",
                description="Putar Ulang Dari Awal"
            ),
            types.BotCommand(
                command="clean",
                description="Bersihkan Cache"
            ),
            types.BotCommand(
                command="mute",
                description="Bisukan Userbot Dalam Obrolan Suara"
            ),
            types.BotCommand(
                command="unmute",
                description="Suarakan Userbot Dalam Obrolan Suara"
            ),
            types.BotCommand(
                command="volume",
                description="Ubah Volume Obrolan Suara"
            ),
            types.BotCommand(
                command="restart",
                description="Perbarui & Mulai Ulang Bot (Khusus Pemilik)"
            )
        ]
    )
)

@bot.on_message(filters.command(["restart", f"restart@{USERNAME}"]) & filters.user(ADMINS) & (filters.chat(CHAT) | filters.private | filters.chat(LOG_GROUP)))
async def restart(client, message):
    k=await message.reply_text("🔄 **Memeriksa Pembaruan...**")
    await asyncio.sleep(3)
    await k.edit("🔄 **Memperbarui, Harap Tunggu...**")
    await asyncio.sleep(5)
    await k.edit("🔄 **Berhasil diperbarui!**")
    await asyncio.sleep(2)
    await k.edit("🔄 **Memulai ulang...**")
    try:
        await message.delete()
    except:
        pass
    process = FFMPEG_PROCESSES.get(CHAT)
    if process:
        try:
            process.send_signal(SIGINT)
        except subprocess.TimeoutExpired:
            process.kill()
        except Exception as e:
            print(e)
            pass
        FFMPEG_PROCESSES[CHAT] = ""
    Thread(
        target=stop_and_restart
        ).start()    

idle()
bot.stop()
print("\n\n@GenthoMusicBot Berhenti!")
