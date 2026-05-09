from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, CommandHandler, ContextTypes, ApplicationBuilder, ConversationHandler, filters
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
CHANNEL_ID = os.getenv("CHANNEL_ID", "@your_channel")

ASK_NAME, ASK_REQUEST, CONFIRM, ASK_MORE, RESTART = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter your name:", reply_markup=ReplyKeyboardRemove())
    return ASK_NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    name = update.message.text
    await update.message.reply_text(f"{name}, please write your request:")
    return ASK_REQUEST

async def get_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["request"] = update.message.text

    keyboard = [["Yes", "No"]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "Confirm submission?",
        reply_markup=reply_markup
    )

    return CONFIRM

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    request = context.user_data.get("request")
    keyboard1 = [["More", "End"]]

    if text == "Yes" and request:
        await update.message.reply_text("Request sent ✅", reply_markup=ReplyKeyboardRemove())
        message = (
        f"<b>New request:</b>\n"
        f"<b>Name:</b> {context.user_data.get('name')}\n"
        f"<b>Request:</b> {request}"
)

        await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=message,
        parse_mode="HTML"        
        )

        await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=message,
        parse_mode="HTML"
)

    else:
        await update.message.reply_text("Request canceled ❌", reply_markup=ReplyKeyboardRemove())

    context.user_data.pop("request", None)

    reply_markup = ReplyKeyboardMarkup(
        keyboard1,
        resize_keyboard=True
        )
    await update.message.reply_text(
        "Send another request?",
        reply_markup=reply_markup
        )

    return ASK_MORE

async def onemore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = [["Start Over"]]
    ewe = update.message.text
    name = context.user_data.get("name")
    if ewe == "More":
        await update.message.reply_text(f"{name}, please write your request:", reply_markup=ReplyKeyboardRemove())
        return ASK_REQUEST
    elif ewe == "End":
        reply_markup = ReplyKeyboardMarkup(
            button,
            resize_keyboard=True
        )
        await update.message.reply_text(
            "Click the button below to start a new request",
            reply_markup=reply_markup
        )
        return RESTART
    
    return ASK_MORE

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    res = update.message.text
    if res == "Start Over":
        await update.message.reply_text("Enter your name:", reply_markup=ReplyKeyboardRemove())
        return ASK_NAME

    return ASK_NAME
    

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        ASK_REQUEST: [MessageHandler(filters.TEXT &~filters.COMMAND, get_request)],
        CONFIRM: [MessageHandler(filters.Regex("^(Yes|No)$"), confirm)],
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        ASK_MORE: [MessageHandler(filters.TEXT & ~filters.COMMAND, onemore)],
        RESTART: [MessageHandler(filters.TEXT & ~filters.COMMAND, restart)]
    },
    fallbacks=[]
)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(conversation_handler)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Type /start to begin.",
        reply_markup=ReplyKeyboardRemove()
    )

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

app.run_polling()

