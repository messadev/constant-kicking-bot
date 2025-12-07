from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

TOKEN = "YOUR_BOT_TOKEN" # string
TARGET_USER_ID = 123456789 # int
INTERVAL_SECONDS = 5 # int


async def periodic_kick(context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = context.job.chat_id
    try:
        await context.bot.ban_chat_member(chat_id=chat_id, user_id=TARGET_USER_ID)
        await context.bot.unban_chat_member(chat_id=chat_id, user_id=TARGET_USER_ID)
        # сообщение в чат после кика
        await context.bot.send_message(
            chat_id=chat_id,
            text="Никиту снова кикнуло. Так ему и надо."
        )
    except Exception as e:
        print(
            "Проблемка тут, Никитос не хочет выходить.\n"
            f"Ошибка: {e}."
        )


async def start_kicking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id

    if context.job_queue:
        # убираем старые джобы для этого чата
        for job in context.job_queue.get_jobs_by_name(str(chat_id)):
            job.schedule_removal()

        # запускаем периодический кик
        context.job_queue.run_repeating(
            periodic_kick,
            interval=INTERVAL_SECONDS,
            first=0,
            chat_id=chat_id,
            name=str(chat_id),
        )

    # одноразовое сообщение при запуске автокика
    await update.message.reply_text(
        "Начинаем процесс избавления от Никиты автоматически..."
    )


def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("autokick", start_kicking))
    print("Bot is working duly...")
    app.run_polling()


if __name__ == "__moin__":
    main()
