from pyrogram import Client, filters
import requests
import random
import os
import re
import asyncio
import time
from BADMUNDA.bot_class import BAD

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


BAD.on_message(
    filters.command("repo")
    & filters.group)
async def help(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/a336506e5b756b82dbc41.png",
        caption=f"""🦋 𝐂ʟɪᴄᴋ 𝐁ᴇʟᴏᴡ 𝐁ᴜᴛᴛᴏɴ 𝐓ᴏ 𝐆ᴇᴛ 𝐑ᴇᴘᴏ ❤️""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🗡️ 𝐌ᴜsɪᴄ  𝐑ᴇᴘᴏ 🗡️", url=f"https://github.com/Badhacker98/BADMUSIC/fork")
                ],
                [
                    InlineKeyboardButton(
                        "🗡️ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ  🗡️", url=f"https://github.com/Badhacker98/BadGroup_Bot/fork")
                ],
                [
                    InlineKeyboardButton(
                        "🗡️ 𝐏ʙx ᴜ  𝐑ᴇᴘᴏ  🗡️", url=f"https://github.com/Badhacker98/PbXbot/fork")
                ],
                 [
                    InlineKeyboardButton(
                        "🗡️ 𝐏ʙx 2.0 ᴜ 𝐑ᴇᴘᴏ 🗡️", url=f"https://github.com/Badhacker98/PBX_2.0/fork")
                ],
                 [
                    InlineKeyboardButton(
                        "🗡️ 𝐒ᴘᴀᴍ  𝐑ᴇᴘᴏ 🗡️", url=f"https://github.com/Badhacker98/BAD_SPAM_X/fork")
                 ]
            ]
        ),
    )

@BAD.on_message(
    filters.command("repo")
    & filters.group)
async def help(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/a336506e5b756b82dbc41.png",
        caption=f"""🦋 𝐂ʟɪᴄᴋ 𝐁ᴇʟᴏᴡ 𝐁ᴜᴛᴛᴏɴ 𝐓ᴏ 𝐆ᴇᴛ 𝐑ᴇᴘᴏ ❤️""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🗡️ 𝐌ᴜsɪᴄ  𝐑ᴇᴘᴏ 🗡️", url=f"https://github.com/Badhacker98/BADMUSIC/fork")
                ],
                [
                    InlineKeyboardButton(
                        "🗡️ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ  🗡️", url=f"https://github.com/Badhacker98/BadGroup_Bot/fork")
                ],
                [
                    InlineKeyboardButton(
                        "🗡️ 𝐏ʙx ᴜ  𝐑ᴇᴘᴏ  🗡️", url=f"https://github.com/Badhacker98/PbXbot/fork")
                ],
                 [
                    InlineKeyboardButton(
                        "🗡️ 𝐏ʙx 2.0 ᴜ 𝐑ᴇᴘᴏ 🗡️", url=f"https://github.com/Badhacker98/PBX_2.0/fork")
                ],
                 [
                    InlineKeyboardButton(
                        "🗡️ 𝐒ᴘᴀᴍ  𝐑ᴇᴘᴏ 🗡️", url=f"https://github.com/Badhacker98/BAD_SPAM_X/fork")
                 ]
            ]
        ),
    )

@BAD.on_message(
    filters.command("repo")
    & filters.private)
async def help(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/a336506e5b756b82dbc41.png",
        caption=f"""🦋 𝐂ʟɪᴄᴋ 𝐁ᴇʟᴏᴡ 𝐁ᴜᴛᴛᴏɴ 𝐓ᴏ 𝐆ᴇᴛ 𝐑ᴇᴘᴏ ❤️""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🗡️ 𝐌ᴜsɪᴄ  𝐑ᴇᴘᴏ 🗡️", url=f"https://github.com/Badhacker98/BADMUSIC/fork")
                ],
                [
                    InlineKeyboardButton(
                        "🗡️ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ  🗡️", url=f"https://github.com/Badhacker98/BadGroup_Bot/fork")
                ],
                [
                    InlineKeyboardButton(
                        "🗡️ 𝐏ʙx ᴜ  𝐑ᴇᴘᴏ  🗡️", url=f"https://github.com/Badhacker98/PbXbot/fork")
                ],
                 [
                    InlineKeyboardButton(
                        "🗡️ 𝐏ʙx 2.0 ᴜ 𝐑ᴇᴘᴏ 🗡️", url=f"https://github.com/Badhacker98/PBX_2.0/fork")
                ],
                 [
                    InlineKeyboardButton(
                        "🗡️ 𝐒ᴘᴀᴍ  𝐑ᴇᴘᴏ 🗡️", url=f"https://github.com/Badhacker98/BAD_SPAM_X/fork")
                 ]
            ]
        ),
    )
