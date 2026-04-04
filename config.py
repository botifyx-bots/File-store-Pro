import logging
from logging.handlers import RotatingFileHandler

# Bot Configuration
LOG_FILE_NAME = "bot.log"
PORT = '5010'
OWNER_ID = 7156099919

MSG_EFFECT = 5046509860389126442

SHORT_URL = "shrinkme.io" # shortner url 
SHORT_API = "e75f29485ddb045e6887d284f762f3daeb84f869"
SHORT_TUT = "https://t.me/ANIME_X_FLEX/19"

# Bot Configuration
SESSION = "SASUKE"
TOKEN = "8207472717:AAHLdPsRtYZsXErJouz3z2WfTxIDLbdW6hA"
API_ID = "27226524"
API_HASH = "a14c9cd4629fde6b4d9b8c77df00fb00"
WORKERS = 5

DB_URI = "mongodb+srv://ANI_OTAKU:ANI_OTAKU@cluster0.t3frstc.mongodb.net/?appName=Cluster0"
DB_NAME = "SASUKE-FILESTORE"

FSUBS = [[-1003483476894, True, 10]] # Force Subscription Channels [channel_id, request_enabled, timer_in_minutes]
# Database Channel (Primary)
DB_CHANNEL =  -1001753514086  # just put channel id dont add ""
# Multiple Database Channels (can be set via bot settings)
# DB_CHANNELS = {
#     "-1002595092736": {"name": "Primary DB", "is_primary": True, "is_active": True},
#     "-1001234567890": {"name": "Secondary DB", "is_primary": False, "is_active": True}
# }
# Auto Delete Timer (seconds)
AUTO_DEL = 300
# Admin IDs
ADMINS = [7156099919]
# Bot Settings
DISABLE_BTN = True
PROTECT = True

# Messages Configuration
MESSAGES = {
    "START": "<b>›› ʜᴇʏ!! {mention}× sᴇɴᴘᴀɪ 🎊\n</b><blockquote><b>ᴜɴʟᴏᴄᴋ ᴛʜᴇ ᴇɴɪɢᴍᴀ ᴏꜰ ᴏɴɢᴏɪɴɢ ᴀɴɪᴍᴇ ᴡʜᴇʀᴇ ᴅᴇsɪʀᴇ ʟɪɴɢᴇʀs ʙᴇʏᴏɴᴅ ᴇᴠᴇʀʏ ꜰʀᴀᴍᴇ, ᴅʀᴀᴡɪɴɢ ʏᴏᴜ ɪɴᴛᴏ ᴀ ʀᴇᴀʟᴍ ᴏꜰ ʜɪᴅᴅᴇɴ ꜰᴀɴᴛᴀsɪᴇs ᴀɴᴅ sɪʟᴇɴᴛ ᴏʙsᴇssɪᴏɴs.</b></blockquote>\n<blockquote>››ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a href='https://t.me/ITSANIMEN'>彡 Δ𝙽𝙸_𝙾𝚃Δ𝙺𝚄 彡</a></blockquote>",
    "FSUB": "<blockquote>›› ʜᴇʏ {mention}× sᴇɴᴘᴀɪ 🎊</blockquote>\n<blockquote><b>ʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ, sᴜʙsᴄʀɪʙᴇ ɴᴏᴡ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇs</b></blockquote>",
    "ABOUT": "<b>›› ғᴏʀ ᴍᴏʀᴇ: <a href='https://t.me/ANIME_X_FLEX'>Cʟɪᴄᴋ ʜᴇʀᴇ</a>\n<blockquote expandable>›› ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/BotifyX_Pro_Botz'>ʙᴏᴛɪғʏx_ᴏғғɪᴄɪᴀʟ</a> \n›› ᴏᴡɴᴇʀ: @ITSANIMEN\n›› ʟᴀɴɢᴜᴀɢᴇ: <a href='https://docs.python.org/3/'>Pʏᴛʜᴏɴ 3</a> \n›› ʟɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ ᴠ2</a> \n›› ᴅᴀᴛᴀʙᴀsᴇ: <a href='https://www.mongodb.com/docs/'>Mᴏɴɢᴏ ᴅʙ</a> \n›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @ITS_shun_x</b></blockquote>",
    "CHANNELS":"<b>›› ᴀɴɪᴍᴇ ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/Anime_z_Flex'>ᴏᴛᴀᴋᴜ_ɴᴀᴛɪᴏɴx</a>\n<blockquote expandable>›› ᴍᴏᴠɪᴇs: <a href='https://t.me/OTAKU_Mania'>ᴀɴɪ_ᴍᴏᴠɪᴇ's ᴍᴀɴɪᴀ</a>\n›› ᴀɴɪᴍᴇ ᴇᴅɪᴛᴢ: <a href='https://t.me/Animez_Edits'>ᴀɴɪᴍᴇ'ᴢ ᴇᴅɪᴛ'ᴢ</a>\n›› ᴀᴅᴜʟᴛ ᴄʜᴀɴɴᴇʟs: <a href='https://t.me/Hamine_flix'>𝖧𝖺𝗇𝗂𝗆𝖾 𝖥𝗅𝗂𝗑</a>\n›› ᴍᴀɴʜᴡᴀ ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/pornwhaa_flix'>ᴘᴏʀɴʜᴡᴀ ғʟɪx</a>\n›› ᴄᴏᴍᴍᴜɴɪᴛʏ: <a href='https://t.me/ANIME_X_FLEX'>ᴏᴛᴀᴋᴜғʟɪx</a>\n›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @ITSANIMEN</b></blockquote>",
    "REPLY": "<b>ғᴜᴄᴋ ᴏғғ ʙɪᴛᴄʜ !!!</b>",
    "SHORT_MSG": "<blockquote><b>✧ TOKEN EXPIRED</b></blockquote>\n<blockquote>›› ᴘʟᴇᴀsᴇ ᴠᴇʀɪғʏ ᴛᴏ ʀᴇɢᴀɪɴ ᴀᴄᴄᴇss ᴛᴏ ᴛʜᴇ ғɪʟᴇs\n›› ᴠᴀʟɪᴅ ᴄʀᴇᴅɪᴛs: 5 ᴄʀᴇᴅɪᴛs</blockquote>\n────────────────────────\n<blockquote>›› ᴡʜᴀᴛ ɪs ᴀ ᴛᴏᴋᴇɴ?</blockquote>\n<blockquote>≡  ᴇᴀᴄʜ ᴀᴅ ʙʏᴘᴀss ʀᴇᴡᴀʀᴅ ʏᴏᴜ ᴡɪᴛʜ 5 ᴄʀᴇᴅɪᴛs.ᴏɴᴇ ᴄʀᴇᴅɪᴛ ɪs ᴄᴏɴsᴜᴍᴇᴅ ᴘᴇʀ ғɪʟᴇ/ʟɪɴᴋ ᴀᴄᴄᴇss.</blockquote>",
    "START_PHOTO": "https://ibb.co/ch6kvnMf",
    "FSUB_PHOTO": "https://ibb.co/C5q41g1C",
    "SHORT_PIC": "https://ibb.co/XxMhdhDs",
    "SHORT": "https://ibb.co/mC9H5kmF",
    "SHORT_VERIFY": "https://ibb.co/rGg6R2q6",
    "PREMIUM_PLANS_PIC": "https://ibb.co/8Dzq5n9G",
    "QR_PAYMENT_PIC": "https://ibb.co/kVPDT5cP"
}

def LOGGER(name: str, client_name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    formatter = logging.Formatter(
        f"[%(asctime)s - %(levelname)s] - {client_name} - %(name)s - %(message)s",
        datefmt='%d-%b-%y %H:%M:%S'
    )
    file_handler = RotatingFileHandler(LOG_FILE_NAME, maxBytes=50_000_000, backupCount=10)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
