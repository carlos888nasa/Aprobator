import os 
from aprobar import aprobar
from dotenv import load_dotenv
from telegram import Update
from pomodoro import pomodoro, boton_pomodoro, proceso_manual, cancelar_pomodoro, SELECCIONANDO_OPCION, ESPERANDO_TIEMPO

from telegram.ext import  ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, CallbackQueryHandler, MessageHandler, filters

MENSAJE_MENU = (
    "¡Hola! Soy Aprobator 🤖. Tu salvavidas universitario.\n\n"
    "Sé que no hay tiempo que perder, así que vamos al grano. "
    "Aquí tienes lo que puedo hacer por ti:\n\n"
    "🎯 /aprobar <nota_actual> <porcentaje_evaluado>\n"
    "Te calculo exactamente qué nota necesitas en el examen final para salvar la asignatura.\n"
    "💡 Ejemplo: Escribe '/aprobar 4.5 40'\n\n"
    "🍅 /pomodoro\n"
    "Activa el modo bestia de estudio. Gestiono tus tiempos y descansos para que no te quemes el cerebro.\n"
    "💡 Ideal para maratones de biblioteca.\n\n"
    "🆘 /ayuda\n"
    "Vuelve a mostrarte este menú en cualquier momento."
)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(MENSAJE_MENU)
    
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("aprobar", aprobar))
    application.add_handler(CommandHandler("ayuda", start))

    pomodoro_handler = ConversationHandler(
        entry_points=[CommandHandler("pomodoro", pomodoro)],
        states={
            SELECCIONANDO_OPCION: [CallbackQueryHandler(boton_pomodoro, pattern='^pomo_')],
            ESPERANDO_TIEMPO: [MessageHandler(filters.TEXT & ~filters.COMMAND, proceso_manual)]
        },
        fallbacks=[CommandHandler("cancelar", cancelar_pomodoro)]
    )
    application.add_handler(pomodoro_handler)

    application.add_handler(pomodoro_handler)
    application.run_polling()
