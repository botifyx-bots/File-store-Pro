from helper.helper_func import *
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import humanize
from config import MSG_EFFECT, OWNER_ID
from plugins.shortner import get_short
from helper.helper_func import get_messages, force_sub, decode, batch_auto_del_notification
import asyncio
import time
#===============================================================#

@Client.on_message(filters.command('start') & filters.private)
@force_sub
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id

    # 1. Add user if not present
    present = await client.mongodb.present_user(user_id)
    if not present:
        try:
            await client.mongodb.add_user(user_id)
        except Exception as e:
            client.LOGGER(__name__, client.name).warning(f"Error adding a user:\n{e}")

    # 2. Check if banned
    is_banned = await client.mongodb.is_banned(user_id)
    if is_banned:
        return await message.reply("**You have been banned from using this bot!**")

    text = message.text
    if len(text) > 7:
        try:
            original_payload = text.split(" ", 1)[1]
            base64_string = original_payload

            is_short_link = False
            if base64_string.startswith("yu3elk"):
                base64_string = base64_string[6:-1]
                is_short_link = True
                session, saved_payload, verify_time = await client.mongodb.get_verify_data(user_id)
                if not session:
                    return await message.reply(
                        "<blockquote>⚠️ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴇxᴘɪʀᴇᴅ.\nᴘʟᴇᴀsᴇ ɢᴇɴᴇʀᴀᴛᴇ ᴀ ɴᴇᴡ ʟɪɴᴋ.</blockquote>"
                    )
                # ❌ OLD LINK USED
                if saved_payload != base64_string:
                    return await message.reply(
                        "<blockquote>🚫 ᴛʜɪs ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ʟɪɴᴋ ɪꜱ ɴᴏ ʟᴏɴɢᴇʀ ᴠᴀʟɪᴅ.</blockquote>"
                    )
                time_taken = int(time.time()) - verify_time
                # 🚫 BYPASS DETECTED (<45 sec)
                if time_taken < 45:
                    await client.mongodb.clear_verify_session(user_id)
                    return await message.reply(
                        "<blockquote>🚫 ʙʏᴘᴀss ᴅᴇᴛᴇᴄᴛᴇᴅ!\n"
                        "⧗ ᴛɪᴍᴇ ᴛᴀᴋᴇɴ < 45s\n"
                        "ᴘʟᴇᴀsᴇ ᴄᴏᴍᴘʟᴇᴛᴇ ᴛʜᴇ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴘʀᴏᴘᴇʀʟʏ.</blockquote>"
                    )
                # 🚫 SESSION TOO OLD (>2 min)
                if time_taken > 240:
                    await client.mongodb.clear_verify_session(user_id)
                    return await message.reply(
                        "<blockquote>⚠️ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴛɪᴍᴇᴏᴜᴛ!\n"
                        "ᴘʟᴇᴀsᴇ ɢᴇɴᴇʀᴀᴛᴇ ᴀ ɴᴇᴡ ʟɪɴᴋ.</blockquote>"
                    )
                await client.mongodb.clear_verify_session(user_id)
                await client.mongodb.add_credits(user_id, 5)
                unlock_link = f"https://t.me/{client.username}?start={base64_string}"
                success_photo = client.messages.get("SHORT_VERIFY", "")
                success_caption = (
                    "<b>ⓘ Your verification is successful!</b>\n"
                    "<blockquote>✦ 5 Credits Added to Your Account.</blockquote>"
                )
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=success_photo,
                    caption=success_caption,
                    reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton("✨ ᴄʟɪᴄᴋ ʜᴇʀᴇ ✨", url=unlock_link)
                        ],
                        [
                            InlineKeyboardButton("• ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ •", url="https://t.me/ITSANIMEN")
                        ]
                    ])
                )
                return
        except IndexError:
            return await message.reply("Invalid command format.")

        # 3. Check premium status
        is_user_pro = await client.mongodb.is_pro(user_id)
        # 3.5 Check credits
        user_credits = await client.mongodb.get_credits(user_id)
        # 4. Check if shortner is enabled
        shortner_enabled = getattr(client, 'shortner_enabled', True)

        # 5. If user is not premium AND shortner is enabled, send short URL and return
        if not is_user_pro and user_id != OWNER_ID and not is_short_link and shortner_enabled and user_credits <= 0:
            await client.mongodb.set_verify_session(user_id, base64_string)
            try:
                short_link = get_short(f"https://t.me/{client.username}?start=yu3elk{base64_string}7", client)
            except Exception as e:
                client.LOGGER(__name__, client.name).warning(f"Shortener failed: {e}")
                return await message.reply("Couldn't generate short link.")

            short_photo = client.messages.get("SHORT_PIC", "")
            short_caption = client.messages.get("SHORT_MSG", "")
            tutorial_link = getattr(client, 'tutorial_link', "https://t.me/ANIME_X_FLEX/19")

            await client.send_photo(
                chat_id=message.chat.id,
                photo=short_photo,
                caption=short_caption,
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("• ᴏᴘᴇɴ ʟɪɴᴋ", url=short_link),
                        InlineKeyboardButton("ᴛᴜᴛᴏʀɪᴀʟ •", url=tutorial_link)
                    ],
                    [
                        InlineKeyboardButton(" • ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ •", url="https://t.me/Premium_Fliix/21")
                    ]
                ])
            )
            return  # prevent sending actual files

        # 6. Decode and prepare file IDs
        try:
            string = await decode(base64_string)
            argument = string.split("-")
            ids = []
            source_channel_id = None

            if len(argument) == 3:
                # Try to determine source channel from encoded multiplier
                encoded_start = int(argument[1])
                encoded_end = int(argument[2])
                
                # Try primary channel first
                primary_multiplier = abs(client.db)
                start_primary = int(encoded_start / primary_multiplier)
                end_primary = int(encoded_end / primary_multiplier)
                
                # Check if the division results in clean integers (meaning this channel was used for encoding)
                if encoded_start % primary_multiplier == 0 and encoded_end % primary_multiplier == 0:
                    source_channel_id = client.db
                    start = start_primary
                    end = end_primary
                    client.LOGGER(__name__, client.name).info(f"Decoded batch from primary channel {source_channel_id}: {start}-{end}")
                else:
                    # Try secondary channels
                    db_channels = getattr(client, 'db_channels', {})
                    for channel_id_str in db_channels.keys():
                        channel_id = int(channel_id_str)
                        channel_multiplier = abs(channel_id)
                        start_test = int(encoded_start / channel_multiplier)
                        end_test = int(encoded_end / channel_multiplier)
                        
                        if encoded_start % channel_multiplier == 0 and encoded_end % channel_multiplier == 0:
                            source_channel_id = channel_id
                            start = start_test
                            end = end_test
                            client.LOGGER(__name__, client.name).info(f"Decoded batch from secondary channel {source_channel_id}: {start}-{end}")
                            break
                    
                    # Fallback to primary if no match found
                    if source_channel_id is None:
                        source_channel_id = client.db
                        start = start_primary
                        end = end_primary
                
                ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))

            elif len(argument) == 2:
                # Single message
                encoded_msg = int(argument[1])
                
                # Try primary channel first
                if hasattr(client, 'db_channel') and client.db_channel:
                    primary_multiplier = abs(client.db_channel.id)
                    msg_id_primary = int(encoded_msg / primary_multiplier)
                    
                    if encoded_msg % primary_multiplier == 0:
                        source_channel_id = client.db_channel.id
                        ids = [msg_id_primary]
                    else:
                        # Try secondary channels
                        db_channels = getattr(client, 'db_channels', {})
                        for channel_id_str in db_channels.keys():
                            channel_id = int(channel_id_str)
                            channel_multiplier = abs(channel_id)
                            msg_id_test = int(encoded_msg / channel_multiplier)
                            
                            if encoded_msg % channel_multiplier == 0:
                                source_channel_id = channel_id
                                ids = [msg_id_test]
                                break
                        
                        # Fallback to primary
                        if source_channel_id is None:
                            source_channel_id = client.db_channel.id if hasattr(client, 'db_channel') else client.db
                            ids = [msg_id_primary]
                else:
                    # Fallback for legacy compatibility
                    source_channel_id = client.db
                    ids = [int(encoded_msg / abs(client.db))]

        except Exception as e:
            client.LOGGER(__name__, client.name).warning(f"Error decoding base64: {e}")
            return await message.reply("⚠️ Invalid or expired link.")

        # 7. Get messages from the specific source channel first
        temp_msg = await message.reply("Wait A Sec..")
        messages = []

        try:
            # Try to get messages from the identified source channel first
            if source_channel_id:
                client.LOGGER(__name__, client.name).info(f"Trying to get messages from source channel: {source_channel_id}")
                try:
                    msgs = await client.get_messages(
                        chat_id=source_channel_id,
                        message_ids=list(ids)
                    )
                    # Filter out None messages (deleted/not found)
                    valid_msgs = [msg for msg in msgs if msg is not None]
                    messages.extend(valid_msgs)
                    client.LOGGER(__name__, client.name).info(f"Found {len(valid_msgs)} messages from source channel {source_channel_id}")
                    
                    # If we didn't get all messages, try the fallback system
                    if len(valid_msgs) < len(list(ids)):
                        missing_ids = [mid for mid in ids if mid not in {msg.id for msg in valid_msgs}]
                        if missing_ids:
                            client.LOGGER(__name__, client.name).info(f"Missing {len(missing_ids)} messages, trying fallback system")
                            # Use the fallback system for missing messages
                            additional_messages = await get_messages(client, missing_ids)
                            messages.extend(additional_messages)
                            client.LOGGER(__name__, client.name).info(f"Found {len(additional_messages)} additional messages from fallback")
                except Exception as e:
                    client.LOGGER(__name__, client.name).warning(f"Error getting messages from source channel {source_channel_id}: {e}")
                    # Fallback to the multi-channel system
                    messages = await get_messages(client, ids)
            else:
                client.LOGGER(__name__, client.name).info("No specific source channel identified, using multi-channel fallback")
                # Use the multi-channel fallback system
                messages = await get_messages(client, ids)
        except Exception as e:
            await temp_msg.edit_text("Something went wrong!")
            client.LOGGER(__name__, client.name).warning(f"Error getting messages: {e}")
            return

        if not messages:
            return await temp_msg.edit("Couldn't find the files in the database.")
        await temp_msg.delete()

        yugen_msgs = []
        for msg in messages:
            caption = (
                client.messages.get('CAPTION', '').format(
                    previouscaption=msg.caption.html if msg.caption else msg.document.file_name
                ) if bool(client.messages.get('CAPTION', '')) and bool(msg.document)
                else ("" if not msg.caption else msg.caption.html)
            )
            reply_markup = msg.reply_markup if not client.disable_btn else None

            try:
                copied_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    reply_markup=reply_markup,
                    protect_content=client.protect
                )
                yugen_msgs.append(copied_msg)
                
            except FloodWait as e:
                await asyncio.sleep(e.x)
                copied_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    reply_markup=reply_markup,
                    protect_content=client.protect
                )
                yugen_msgs.append(copied_msg)
            except Exception as e:
                client.LOGGER(__name__, client.name).warning(f"Failed to send message: {e}")
                pass
        # Deduct 1 credit per link unlock
        if not is_user_pro and not is_short_link:
            skip = await client.mongodb.should_skip_deduct(user_id)
    
            if skip:
                await client.mongodb.clear_skip_deduct(user_id)
            else:
                await client.mongodb.deduct_credit(user_id)
                await client.mongodb.add_used_credit(user_id)
                credits_left = await client.mongodb.get_credits(user_id)

            if credits_left <= 0:
                await client.mongodb.user_data.update_one(
                    {'_id': user_id},
                    {'$set': {'verify_session': False}}
                )

        # 8. Auto delete timer
        if messages and client.auto_del > 0:
            # Create transfer link for getting files again (original base64_string)
            transfer_link = original_payload
            
            # Start batch auto delete notification - single notification for all files
            asyncio.create_task(batch_auto_del_notification(
                bot_username=client.username,
                messages=yugen_msgs,
                delay_time=client.auto_del,
                transfer_link=transfer_link,
                chat_id=message.from_user.id,
                client=client
            ))
        return

    # 9. Normal start message
    else:
        buttons = [
            [
                InlineKeyboardButton("•ᴀʙᴏᴜᴛ•", callback_data="about"),
                InlineKeyboardButton("•ᴄʜᴀɴɴᴇʟs•", callback_data="channels")
            ],
            [
                InlineKeyboardButton("•ᴄʟᴏsᴇ•", callback_data="close")
            ]
        ]
        if user_id in client.admins:
            buttons.insert(0, [InlineKeyboardButton("⛩️ ꜱᴇᴛᴛɪɴɢꜱ ⛩️", callback_data="settings")])

        photo = client.messages.get("START_PHOTO", "")
        start_caption = client.messages.get('START', 'Welcome, {mention}').format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        )

        if photo:
            await client.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=start_caption,
                message_effect_id=MSG_EFFECT,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            await client.send_message(
                chat_id=message.chat.id,
                text=start_caption,
                message_effect_id=MSG_EFFECT,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        return

#===============================================================#

@Client.on_message(filters.command('request') & filters.private)
async def request_command(client: Client, message: Message):
    user_id = message.from_user.id
    is_admin = user_id in client.admins  # ✅ Fix this line
    is_user_premium = await client.mongodb.is_pro(user_id)

    if is_admin or user_id == OWNER_ID:
        await message.reply_text("🔹 **You are my sensei!**\nThis command is only for users.")
        return

    if not is_user_premium: 
        BUTTON_URL = "https://t.me/ITSANIMEN"
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 Upgrade to Premium", url=BUTTON_URL)]
        ])
        await message.reply(
            "❌ **You are not a premium user.**\nUpgrade to premium to access this feature.",
            reply_markup=reply_markup
        )
        return

    if len(message.command) < 2:
        await message.reply("⚠️ **Send me your request in this format:**\n`/request Your_Request_Here`")
        return

    requested = " ".join(message.command[1:])

    owner_message = (
        f"📩 **New Request from {message.from_user.mention}**\n\n"
        f"🆔 User ID: `{user_id}`\n"
        f"📝 Request: `{requested}`"
    )

    await client.send_message(OWNER_ID, owner_message)
    await message.reply("✅ **Thanks for your request!**\nYour request will be reviewed soon. Please wait.")

#===============================================================#

@Client.on_message(filters.command('profile') & filters.private)
async def my_plan(client: Client, message: Message):
    user_id = message.from_user.id
    is_admin = user_id in client.admins  # ✅ Fix here

    if is_admin or user_id == OWNER_ID:
        await message.reply_text("🔹 You're my sensei! This command is only for users.")
        return
    
    is_user_premium = await client.mongodb.is_pro(user_id)
    credits = await client.mongodb.get_credits(user_id)

    if is_user_premium:
        await message.reply_text(
            "**👤 Profile Information:**\n\n"
            "🔸 Ads: Disabled\n"
            "🔸 Plan: Premium\n"
            "🔸 Request: Enabled\n\n"
            "🌟 You're a Premium User!"
        )
    else:
        await message.reply_text(
            "**👤 Profile Information:**\n\n"
            "🔸 Ads: Enabled\n"
            "🔸 Plan: Free\n"
            "🔸 Request: Disabled\n"
            f"💳 Credits: {credits}\n"
            "🔓 Unlock Premium to get more benefits\n"
            "Contact: @ITSANIMEN"
        )

#===============================================================#

@Client.on_message(filters.command('credits') & filters.private)
async def credits_command(client: Client, message: Message):
    user_id = message.from_user.id
    
    credits = await client.mongodb.get_credits(user_id)
    used = await client.mongodb.get_used_credits(user_id)


    text = (
        "<blockquote>📁 <b>𝖄𝖔𝖚𝖗 𝕮𝖗𝖊𝖉𝖎𝖙𝖘 𝕴𝖓𝖋𝖔𝖗𝖒𝖆𝖙𝖎𝖔𝖓</b></blockquote>\n\n"
        f"▪️ <b>Remaining Credits:</b> <code>{credits}</code>\n"
        f"▪️ <b>Total Used Credits:</b> <code>{used}</code>\n"
        "▪️ <b>Credits Per Verification:</b> <code>5</code>\n\n"
        "<i>Use /cplan to earn more credits!</i>"
    )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 ᴄʀᴇᴅɪᴛ ᴘʟᴀɴꜱ", callback_data="show_cplan")],
        [InlineKeyboardButton("• ᴄʟᴏꜱᴇ •", callback_data="close")]
    ])

    await message.reply_text(text, reply_markup=buttons)

#===============================================================#

@Client.on_message(filters.command('cplan') & filters.private)
async def credit_plan(client: Client, message: Message):

    text = (
        "<blockquote>✦ <b>𝗖𝗥𝗘𝗗𝗜𝗧 𝗕𝗔𝗦𝗘𝗗 𝗣𝗟𝗔𝗡𝗦</b></blockquote>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "<blockquote>\n"
        "» 30 credits : ₹50\n"
        "» 60 credits : ₹110\n"
        "» 120 credits : ₹220\n"
        "» 240 credits : ₹480</blockquote>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "<blockquote>✦ Contact @ITSANIMEN to Buy Credits</blockquote>"
    )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("• ᴄʟᴏꜱᴇ •", callback_data="close")]
    ])

    await message.reply_text(text, reply_markup=buttons)

#===============================================================#

@Client.on_message(filters.command("add_credit") & filters.private)
async def add_credit_command(client: Client, message: Message):

    if message.from_user.id not in client.admins:
        return await message.reply_text("❌ You are not allowed to use this command.")

    if len(message.command) != 3:
        return await message.reply_text(
            "<blockquote>⚠️ Usage:\n/add_credit user_id amount</blockquote>"
        )

    try:
        user_id = int(message.command[1])
        amount = int(message.command[2])
    except:
        return await message.reply_text("⚠️ Invalid User ID or Amount.")

    # Check if user exists
    if not await client.mongodb.present_user(user_id):
        await client.mongodb.add_user(user_id)

    await client.mongodb.add_credits(user_id, amount)

    await message.reply_text(
        f"<blockquote>✅ Credits Added Successfully</blockquote>\n\n"
        f"👤 User ID: <code>{user_id}</code>\n"
        f"💳 Added Credits: <code>{amount}</code>"
    )

    try:
        await client.send_message(
            chat_id=user_id,
            text=(
                f"<blockquote>🎉 Credits Added to Your Account</blockquote>\n\n"
                f"💳 Amount: <code>{amount}</code>\n"
                f"Use /credits to check your balance."
            )
        )
    except:
        pass

#===============================================================#

@Client.on_message(filters.command('buy') & filters.private)
async def buy_command(client, message):

    photo = client.messages.get("PREMIUM_PLANS_PIC", "")

    text = (
        "<blockquote>✦ <b>𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗣𝗟𝗔𝗡𝗦</b></blockquote>\n"
        "<blockquote expandable>◍ 𝟷 ᴍᴏɴᴛʜ: ₹𝟷𝟿𝟿\n"
        "◍ 𝟹 ᴍᴏɴᴛʜs: ₹𝟹𝟿𝟿 (ʙᴇsᴛ ᴠᴀʟᴜᴇ)\n"
        "◍ 𝟼 ᴍᴏɴᴛʜs: ₹𝟻𝟿𝟿 (ᴍᴏsᴛ ᴘᴏᴘᴜʟᴀʀ)\n"
        "◍ 𝟷𝟸 ᴍᴏɴᴛʜs: ₹𝟷,𝟷𝟿𝟿 (ᴛᴏᴘ ᴄʜᴏɪᴄᴇ)</blockquote>\n"
        "<blockquote>≡ ʟɪғᴇᴛɪᴍᴇ: ₹𝟸,𝟿𝟿𝟿 (ᴘᴀʏ ᴏɴᴄᴇ, ᴜsᴇ ғᴏʀᴇᴠᴇʀ)</blockquote>\n"
        "<blockquote>⧗ ᴘᴀʏᴍᴇɴᴛ ᴍᴇᴛʜᴏᴅs: ᴘᴀʏᴛᴍ, ɢᴘᴀʏ, ᴘʜᴏɴᴇᴘᴇ, ᴜᴘɪ & ǫʀ ᴄᴏᴅᴇ</blockquote>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "<blockquote expandable>◍ ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ!\n◍ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴜs sᴄʀᴇᴀɴsʜᴏᴛ ᴜsɪɴɢ /bought (ʀᴇᴘʟʏ ᴛᴏ sᴄʀᴇᴀɴsʜᴏᴛ)</blockquote>"
    )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Buy Premium", callback_data="premium_select")],
        [InlineKeyboardButton("• Close •", callback_data="close")]
    ])

    await message.reply_photo(photo=photo, caption=text, reply_markup=buttons)

#===============================================================#

@Client.on_message(filters.command('bought') & filters.private)
async def bought_command(client, message):

    user = message.from_user

    # ❌ if not replying
    if not message.reply_to_message:
        return await message.reply(
            "<blockquote>ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ʀᴇᴘʟʏ ᴛᴏ ʏᴏᴜʀ ᴘᴀʏᴍᴇɴᴛ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ</blockquote>"
        )

    replied = message.reply_to_message

    # ❌ if not photo
    if not replied.photo:
        return await message.reply(
            "<blockquote>ʀᴇᴘʟʏ ᴏɴʟʏ ᴛᴏ ᴘᴀʏᴍᴇɴᴛ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ</blockquote>"
        )

    caption = (
        f"📥 <b>New Premium Purchase Request</b>\n"
        f"👤 User: {user.mention}\n"
        f"🆔 ID: <code>{user.id}</code>\n\n"
        f"Check Screenshot"
    )

    for admin in client.admins:
        try:
            await replied.copy(
                chat_id=admin,
                caption=caption
            )
        except:
            pass

    await message.reply(
        "<blockquote>✅ Screenshot Sent to Admin.\n"
        "Please wait for activation.</blockquote>"
    )
