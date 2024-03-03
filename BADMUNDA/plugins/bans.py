from random import choice
from traceback import format_exc

from pyrogram import enums
from pyrogram.errors import (ChatAdminRequired, PeerIdInvalid, RightForbidden,
                             RPCError, UserAdminInvalid)
from pyrogram.filters import regex
from pyrogram.types import (CallbackQuery, ChatPrivileges,
                            InlineKeyboardButton, InlineKeyboardMarkup,
                            Message)

from BADMUNDA import LOGGER, MESSAGE_DUMP, OWNER_ID
from BADMUNDA.bot_class import BAD
from BADMUNDA.supports import get_support_staff
from BADMUNDA.utils.caching import ADMIN_CACHE, admin_cache_reload
from BADMUNDA.utils.custom_filters import command, restrict_filter
from BADMUNDA.utils.extract_user import extract_user
from BADMUNDA.utils.extras import BAN_GIFS, KICK_GIFS
from BADMUNDA.utils.parser import mention_html
from BADMUNDA.utils.string import extract_time
from BADMUNDA.vars import Config

SUPPORT_STAFF = get_support_staff()

@BAD.on_message(command("tban") & restrict_filter)
async def tban_usr(c: BAD, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="I can't ban nothing!")
        await m.stop_propagation()

    try:
        user_id, user_first_name, _ = await extract_user(c, m)
    except Exception:
        return

    if not user_id:
        await m.reply_text("Cannot find user to ban")
        return
    if user_id == Config.BOT_ID:
        await m.reply_text("WTF??  Why would I ban myself?")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="This user is in my support staff, cannot restrict them."
        )
        LOGGER.info(
            f"{m.from_user.id} trying to ban {user_id} (SUPPORT_STAFF) in {m.chat.id}",
        )
        await m.stop_propagation()

    r_id = m.reply_to_message.id if m.reply_to_message else m.id

    if m.reply_to_message and len(m.text.split()) >= 2:
        reason = m.text.split(None, 1)[1]
    elif not m.reply_to_message and len(m.text.split()) >= 3:
        reason = m.text.split(None, 2)[2]
    else:
        await m.reply_text("Read /help !!")
        return

    if not reason:
        await m.reply_text("You haven't specified a time to ban this user for!")
        return

    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""

    bantime = await extract_time(m, time_val)

    if not bantime:
        return

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "ban")

    if user_id in admins_group:
        await m.reply_text(text="This user is an admin, I cannot ban them!")
        await m.stop_propagation()

    try:
        admin = await mention_html(m.from_user.first_name, m.from_user.id)
        banned = await mention_html(user_first_name, user_id)
        chat_title = m.chat.title
        LOGGER.info(f"{m.from_user.id} tbanned {user_id} in {m.chat.id}")
        await m.chat.ban_member(
            user_id,
            until_date=bantime)
        t_t=f"{admin} banned {banned} in <b>{chat_title}</b>!",
        txt = t_t
        if type(t_t) is tuple:
            txt = t_t[0] # Done this bcuz idk why t_t is tuple type data. SO now if it is tuple this will get text from it
        if reason:
            txt += f"\n<b>Reason</b>: {reason}"
        if time_val:
            txt += f"\n<b>Banned for</b>:{time_val}"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Unban",
                        callback_data=f"unban_={user_id}",
                    ),
                ],
            ],
        )
        anim = choice(BAN_GIFS)
        try:
            await m.reply_animation(
                reply_to_message_id=r_id,
                animation=str(anim),
                caption=txt,
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.HTML,
            )
        except Exception:
            
            await m.reply_text(
                reply_to_message_id=r_id,
                text=txt,
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.HTML,
            )
            await c.send_message(MESSAGE_DUMP,f"#REMOVE from BAN_GFIS\n{anim}")
    # await m.reply_text(txt, reply_markup=keyboard,
    # reply_to_message_id=r_id)
    except ChatAdminRequired:
        await m.reply_text(text="I'm not admin or I don't have rights.")
    except PeerIdInvalid:
        await m.reply_text(
            "I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="Cannot act on this user, maybe I wasn't the one who changed their permissions."
        )
    except RightForbidden:
        await m.reply_text(text="I don't have enough rights to ban this user.")
    except RPCError as ef:
        await m.reply_text(
            (
                f"""Some error occured, report it using `/bug`

      <b>Error:</b> <code>{ef}</code>"""
            )
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())
    return


@BAD.on_message(command("stban") & restrict_filter)
async def stban_usr(c: BAD, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="I can't ban nothing!")
        await m.stop_propagation()

    try:
        user_id, _, _ = await extract_user(c, m)
    except Exception:
        return

    if not user_id:
        await m.reply_text("Cannot find user to ban")
        return
    if user_id == Config.BOT_ID:
        await m.reply_text("What the heck? Why would I ban myself?")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="This user is in my support staff, cannot restrict them."
        )
        LOGGER.info(
            f"{m.from_user.id} trying to ban {user_id} (SUPPORT_STAFF) in {m.chat.id}",
        )
        await m.stop_propagation()

    if m.reply_to_message and len(m.text.split()) >= 2:
        reason = m.text.split(None, 1)[1]
    elif not m.reply_to_message and len(m.text.split()) >= 3:
        reason = m.text.split(None, 2)[2]
    else:
        await m.reply_text("Read /help !!")
        return

    if not reason:
        await m.reply_text("You haven't specified a time to ban this user for!")
        return

    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""

    bantime = await extract_time(m, time_val)

    if not bantime:
        return

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "ban")

    if user_id in admins_group:
        await m.reply_text(text="This user is an admin, I cannot ban them!")
        await m.stop_propagation()

    try:
        LOGGER.info(f"{m.from_user.id} stbanned {user_id} in {m.chat.id}")
        await m.chat.ban_member(user_id, until_date=bantime)
        await m.delete()
        if m.reply_to_message:
            await m.reply_to_message.delete()
            return
        return
    except ChatAdminRequired:
        await m.reply_text(text="I'm not admin or I don't have rights.")
    except PeerIdInvalid:
        await m.reply_text(
            "I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="Cannot act on this user, maybe I wasn't the one who changed their permissions."
        )
    except RightForbidden:
        await m.reply_text(text="I don't have enough rights to ban this user.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""Some error occured, report it using `/bug`

      <b>Error:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())
    return


@BAD.on_message(command("dtban") & restrict_filter)
async def dtban_usr(c: BAD, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="I can't ban nothing!")
        await m.stop_propagation()

    if not m.reply_to_message:
        await m.reply_text(
            "Reply to a message with this command to temp ban and delete the message.",
        )
        await m.stop_propagation()

    user_id = m.reply_to_message.from_user.id
    user_first_name = m.reply_to_message.from_user.first_name

    if not user_id:
        await m.reply_text("Cannot find user to ban")
        return
    if user_id == Config.BOT_ID:
        await m.reply_text("Huh, why would I ban myself?")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(text="I am not going to ban one of my support staff")
        LOGGER.info(
            f"{m.from_user.id} trying to ban {user_id} (SUPPORT_STAFF) in {m.chat.id}",
        )
        await m.stop_propagation()

    if m.reply_to_message and len(m.text.split()) >= 2:
        reason = m.text.split(None, 1)[1]
    elif not m.reply_to_message and len(m.text.split()) >= 3:
        reason = m.text.split(None, 2)[2]
    else:
        await m.reply_text("Read /help !!")
        return

    if not reason:
        await m.reply_text("You haven't specified a time to ban this user for!")
        return

    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""

    bantime = await extract_time(m, time_val)

    if not bantime:
        return

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "ban")

    if user_id in admins_group:
        await m.reply_text(text="This user is an admin, I cannot ban them!")
        await m.stop_propagation()

    try:
        admin = await mention_html(m.from_user.first_name, m.from_user.id)
        banned = await mention_html(user_first_name, user_id)
        chat_title = m.chat.title
        LOGGER.info(f"{m.from_user.id} dtbanned {user_id} in {m.chat.id}")
        await m.chat.ban_member(user_id, until_date=bantime)
        await m.reply_to_message.delete()
        txt = f"{admin} banned {banned} in <b>{chat_title}</b>!"
        if reason:
            txt += f"\n<b>Reason</b>: {reason}"
        if bantime:
            txt += f"\n<b>Banned for</b>: {time_val}"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Unban",
                        callback_data=f"unban_={user_id}",
                    ),
                ],
            ],
        )
        anim = choice(BAN_GIFS)
        try:
            await m.reply_animation(
                animation=str(anim),
                caption=txt,
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.HTML,
            )
        except Exception:
            
            await m.reply_text(
                txt,
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.HTML,
            )
            await c.send_message(MESSAGE_DUMP,f"#REMOVE from BAN_GFIS\n{anim}")
        # await c.send_message(m.chat.id, txt, reply_markup=keyboard)
    except ChatAdminRequired:
        await m.reply_text(text="I'm not admin or I don't have rights.")
    except PeerIdInvalid:
        await m.reply_text(
            "I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="Cannot act on this user, maybe I wasn't the one who changed their permissions."
        )
    except RightForbidden:
        await m.reply_text(text="I don't have enough rights to ban this user.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""Some error occured, report it using `/bug`

      <b>Error:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())
    return


@BAD.on_message(command("kick") & restrict_filter)
async def kick_usr(c: BAD, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="I can't kick nothing!")
        return

    reason = None

    if m.reply_to_message:
        r_id = m.reply_to_message.id
        if len(m.text.split()) >= 2:
            reason = m.text.split(None, 1)[1]
    else:
        r_id = m.id
        if len(m.text.split()) >= 3:
            reason = m.text.split(None, 2)[2]
    try:
        user_id, user_first_name, _ = await extract_user(c, m)
    except Exception:
        return

    if not user_id:
        await m.reply_text("Cannot find user to kick")
        return

    if user_id == Config.BOT_ID:
        await m.reply_text("Huh, why would I kick myself?")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="This user is in my support staff, cannot restrict them."
        )
        LOGGER.info(
            f"{m.from_user.id} trying to kick {user_id} (SUPPORT_STAFF) in {m.chat.id}",
        )
        await m.stop_propagation()

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "kick")

    if user_id in admins_group:
        await m.reply_text(text="This user is an admin, I cannot kick them!")
        await m.stop_propagation()

    try:
        admin = await mention_html(m.from_user.first_name, m.from_user.id)
        kicked = await mention_html(user_first_name, user_id)
        chat_title = m.chat.title
        LOGGER.info(f"{m.from_user.id} kicked {user_id} in {m.chat.id}")
        await m.chat.ban_member(user_id)
        txt = f"{admin} kicked {kicked} in <b>{chat_title}</b>!"
        if reason:
            txt += f"\n<b>Reason</b>: {reason}"
        # await m.reply_text(txt, reply_to_message_id=r_id)
        kickk = choice(KICK_GIFS)
        try:
            await m.reply_animation(
                reply_to_message_id=r_id,
                animation=str(kickk),
                caption=txt,
                parse_mode=enums.ParseMode.HTML,
            )
        except:
            await m.reply_text(
                reply_to_message_id=r_id,
                text=txt,
                parse_mode=enums.ParseMode.HTML,
            )
            await c.send_message(MESSAGE_DUMP,f"#REMOVE from KICK_GFIS\n{kickk}")
        await m.chat.unban_member(user_id)
    except ChatAdminRequired:
        await m.reply_text(text="I'm not admin or I don't have rights.")
    except PeerIdInvalid:
        await m.reply_text(
            "I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="Cannot act on this user, maybe I wasn't the one who changed their permissions."
        )
    except RightForbidden:
        await m.reply_text(text="I don't have enough rights to ban this user.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""Some error occured, report it using `/bug`

      <b>Error:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())

    return


@BAD.on_message(command("skick") & restrict_filter)
async def skick_usr(c: BAD, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="I can't kick nothing!")
        return

    try:
        user_id, _, _ = await extract_user(c, m)
    except Exception:
        return

    if not user_id:
        await m.reply_text("Cannot find user to kick")
        return

    if user_id == Config.BOT_ID:
        await m.reply_text("Huh, why would I kick myself?")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="This user is in my support staff, cannot restrict them."
        )
        LOGGER.info(
            f"{m.from_user.id} trying to skick {user_id} (SUPPORT_STAFF) in {m.chat.id}",
        )
        await m.stop_propagation()

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "kick")

    if user_id in admins_group:
        await m.reply_text(text="This user is an admin, I cannot kick them!")
        await m.stop_propagation()

    try:
        LOGGER.info(f"{m.from_user.id} skicked {user_id} in {m.chat.id}")
        await m.chat.ban_member(user_id)
        await m.delete()
        if m.reply_to_message:
            await m.reply_to_message.delete()
        await m.chat.unban_member(user_id)
    except ChatAdminRequired:
        await m.reply_text(text="I'm not admin or I don't have rights.")
    except PeerIdInvalid:
        await m.reply_text(
            "I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?",
        )
    except UserAdminInvalid:
        await m.reply_text(
            text="Cannot act on this user, maybe I wasn't the one who changed their permissions."
        )
    except RightForbidden:
        await m.reply_text(text="I don't have enough rights to kick this user.")
    except RPCError as ef:
        await m.reply_text(
            text=f"""Some error occured, report it using `/bug`

      <b>Error:</b> <code>{ef}</code>"""
        )
        LOGGER.error(ef)
        LOGGER.error(format_exc())

    return


@BAD.on_message(command("dkick") & restrict_filter)
async def dkick_usr(c: BAD, m: Message):
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(text="I can't ban nothing!")
        return
    if not m.reply_to_message:
        return await m.reply_text("Reply to a message to delete it and kick the user!")

    reason = None

    user_id = m.reply_to_message.from_user.id
    user_first_name = m.reply_to_message.from_user.first_name

    if not user_id:
        await m.reply_text("Cannot find user to kick")
        return

    if user_id == Config.BOT_ID:
        await m.reply_text("Huh, why would I kick myself?")
        await m.stop_propagation()

    if user_id in SUPPORT_STAFF:
        await m.reply_text(
            text="This user is in my support staff, cannot restrict them."
        )
        LOGGER.info(
            f"{m.from_user.id} trying to dkick {user_id} (SUPPORT_STAFF) in {m.chat.id}",
        )
        await m.stop_propagation()

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(m, "kick")

    if user_id in admins_group:
        await m.reply_text(text="This user is an admin, I cannot kick them!")
        await m.stop_propagation()

    try:
        LOGGER.info(f"{m.from_user.id} dkicked {user_id} in {m.chat.id}")
        await m.reply_to_message.delete()
        await m.chat.ban_member(user_id)
        admin = await mention_html(m.from_user.first_name, m.from_user.id)
        kicked = await mention_html(user_first_name, user_id)
        chat_title = m.chat.title
        txt = f"{admin} kicked {kicked} in <b>{chat_title}</b>!"
        if reason:
            txt += f"\n<b>Reason</b>: {reason}"
        kickk = choice(KICK_GIFS)
        try:
            await m.reply_animation(
                animation=str(kickk),
                caption=txt,
                parse_mode=enums.ParseMode.HTML,
            )
        except:
            await m.reply_text(
                txt,
                parse_mode=enums.ParseMode.HTML,
            )
            await c.send_message(MESSAGE_D