from datetime import datetime
import jdatetime
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

# تنظیمات لاگ‌گیری
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# توکن ربات شما
TOKEN = "9293939179:AAH-y2zmBAAUJ-LI5kW5sFUBk_G4-LQIf9k"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! ربات مدیریت کوئست‌های کلن IranCommunity[WIC] روشن شد."
    )


async def new_quest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text(
            "لطفاً تاریخ و عنوان کوئست را وارد کنید.\nمثال:\n`/newquest 1405/09/20 بازی در تورنمنت`",
            parse_mode="Markdown",
        )
        return

    date = args[0]
    title = " ".join(args[1:])

    # دکمه‌های وضعیت برای کاربران در گروه
    keyboard = [
        [
            InlineKeyboardButton(
                "✅ انجام دادم", callback_data="status_done"
            ),
            InlineKeyboardButton(
                "⏳ در حال انجامم", callback_data="status_doing"
            ),
        ],
        [
            InlineKeyboardButton(
                "🆘 نیاز به کمک دارم", callback_data="status_help"
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🎯 **کوئست جدید کلن!**\n\n"
        f"📌 عنوان: {title}\n"
        f"📅 مهلت: {date}\n\n"
        f"👇 لطفاً وضعیت خود را برای این کوئست انتخاب کنید:",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def user_status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    user_name = user.full_name
    data = query.data

    # دریافت تاریخ و ساعت دقیق شمسی همان لحظه
    now_jalali = jdatetime.datetime.now()
    date_str = now_jalali.strftime("%Y/%m/%d")
    time_str = now_jalali.strftime("%H:%M")

    if data == "status_done":
        await query.answer(
            f"عالی {user_name}! کوئست در تاریخ {date_str} ساعت {time_str} با موفقیت ثبت شد. ✅",
            show_alert=True,
        )
    elif data == "status_doing":
        await query.answer(
            f"موفق باشی {user_name}! وضعیت شما: «در حال انجامم» ثبت شد. ⏳",
            show_alert=True,
        )
    elif data == "status_help":
        await query.answer(
            f"{user_name} عزیز، درخواست کمک شما ثبت شد. ادمین‌ها راهنمایی‌ات می‌کنند! 🆘",
            show_alert=True,
        )


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("newquest", new_quest))
    app.add_handler(
        CallbackQueryHandler(
            user_status_handler,
            pattern="^(status_done|status_doing|status_help)$",
        )
    )

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
