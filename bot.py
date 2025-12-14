import logging
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

# ================= CONFIG =================
# ---------------- CONFIG ----------------
import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

PAY_QR = "@QRcoderoyalsdeals"   # QR scanner username
REVIEW_USERNAME = "@royalsdealsreview"

# =========================================

logging.basicConfig(level=logging.INFO)

# ---------------- WELCOME ----------------
WELCOME = f"""
Welcome to royals_deals

How are you today?

We provide premium subscriptions at best prices.

Available Services:
• YouTube / YT Music
• Prime Video
• JioHotstar
• Sony Liv
• Hoichoi
• Canva
• Crunchyroll
• Spotify
• Telegram Account
• Special Combo Offers

Just type the service name.
Example: youtube, prime, hotstar

Reviews: {REVIEW_USERNAME}
"""

# ---------------- FOOTER ----------------
FOOTER = f"""

Activate:
Pay via QR Scanner:
{PAY_QR}

Send payment screenshot after payment.

Reviews: {REVIEW_USERNAME}
"""

# ---------------- OFFERS ----------------
YOUTUBE = """
YouTube + YT Music

₹20  – 1 Month
Plan – Premium (On your Email)
Activation – Your Mail
Validity – 1 Month

₹99 – 1 Month
Plan – Family Plan
Members – 5
Activation – On your Email
Validity – 1 Month

For activation, proceed with payment.
""" + FOOTER


PRIME = """
Prime Video

₹39 – 1 Month – 1 Device
₹99 – 1 Month – Unlimited
₹179 – 6 Month – Unlimited
""" + FOOTER

HOTSTAR = """
JioHotstar

₹29 – 1080p HD – 1 Month
Activation: On your number
""" + FOOTER

SONY = """
Sony Liv Premium

₹31 – 1 Month
Login Only
""" + FOOTER

HOICHOI = """
Hoichoi Premium

₹39 – 1 Month (Email)
₹189 – 1 Year (Number)
""" + FOOTER

CANVA = """
Canva Education Plan

₹39 – 1 Month
₹59 – 3 Month
₹99 – 6 Month
₹189 – 1 Year
""" + FOOTER

CRUNCHYROLL = """
Crunchyroll Mega Fan

₹49 – 1 Month
1 Device Only
""" + FOOTER

SPOTIFY = """
Spotify Premium

₹69 – 2 Month
Individual Plan
""" + FOOTER

TELEGRAM_ACC = """
Telegram Account

India – ₹79
USA – ₹89
Lifetime Validity
""" + FOOTER

COMBO = """
Special Offer Combo – ₹199

Hoichoi
Zee5
Sony Liv
JioHotstar
YouTube Premium
YouTube Music
Prime Video (1 Device)
Netflix (Free APK)

Validity: 1 Month

Netflix Premium (1 screen) – ₹109
""" + FOOTER

# ---------------- FORWARD TO ADMIN ----------------
def forward_to_admin(update, context):
    user = update.message.from_user
    info = (
        "New User Message\n\n"
        f"Name: {user.first_name}\n"
        f"Username: @{user.username if user.username else 'No Username'}\n"
        f"User ID: {user.id}\n"
        "----------------------"
    )
    context.bot.send_message(chat_id=ADMIN_ID, text=info)
    context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )

# ---------------- ADMIN REPLY ----------------
def reply_cmd(update, context):
    if update.message.from_user.id != ADMIN_ID:
        return
    try:
        user_id = int(context.args[0])
        msg = " ".join(context.args[1:])
        context.bot.send_message(chat_id=user_id, text=msg)
        update.message.reply_text("Reply sent successfully.")
    except:
        update.message.reply_text("Use:\n/reply USER_ID message")
# ---------------- START COMMAND ----------------
def start_cmd(update, context):
    update.message.reply_text(WELCOME)

# ---------------- TEXT HANDLER ----------------
def text_handler(update, context):
    text = update.message.text.lower()
    forward_to_admin(update, context)

    if any(k in text for k in ["hi", "hello", "start", "hey"]):
        update.message.reply_text(WELCOME)

    elif any(k in text for k in ["youtube", "yt", "utube", "utub", "you tube", "youtub"]):
        update.message.reply_text(YOUTUBE)

    elif any(k in text for k in ["prime", "amazon", "primevideo", "prime video"]):
        update.message.reply_text(PRIME)

    elif any(k in text for k in ["hotstar", "jiohotstar", "jio hotstar"]):
        update.message.reply_text(HOTSTAR)

    elif any(k in text for k in ["sony", "sonyliv", "sony liv"]):
        update.message.reply_text(SONY)

    elif any(k in text for k in ["hoichoi", "hoi choi"]):
        update.message.reply_text(HOICHOI)

    elif any(k in text for k in ["canva", "canvaa"]):
        update.message.reply_text(CANVA)

    elif any(k in text for k in ["crunchy", "crunchyroll"]):
        update.message.reply_text(CRUNCHYROLL)

    elif any(k in text for k in ["spotify", "spotfy", "spoti"]):
        update.message.reply_text(SPOTIFY)

    elif any(k in text for k in ["telegram", "tg", "telegram account"]):
        update.message.reply_text(TELEGRAM_ACC)

    elif any(k in text for k in ["combo", "all app", "allapps", "special offer"]):
        update.message.reply_text(COMBO)

# ---------------- PHOTO HANDLER ----------------
def photo_handler(update, context):
    forward_to_admin(update, context)

# ---------------- MAIN ----------------
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_cmd))
    dp.add_handler(CommandHandler("reply", reply_cmd))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_handler))
    dp.add_handler(MessageHandler(Filters.photo, photo_handler))

    updater.start_polling(drop_pending_updates=True)
    updater.idle()

if __name__ == "__main__":
    main()
