import os 
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

MENSAJE_MENU = (
    "¡Hola! Soy Aprobator 🤖. Tu salvavidas universitario.\n\n"
    "Sé que no hay tiempo que perder, así que vamos al grano. "
    "Aquí tienes lo que puedo hacer por ti:\n\n"
    "🎯 /aprobar <nota_actual> <porcentaje_evaluado>\n"
    "Te calculo exactamente qué nota necesitas en el examen final para salvar la asignatura.\n"
    "💡 Ejemplo: Escribe '/aprobar 4.5 40' (si sacaste un 4.5 en un parcial que vale el 40%).\n\n"
    "🆘 /ayuda\n"
    "Vuelve a mostrarte este menú en cualquier momento."
)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(MENSAJE_MENU)

async def aprobar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        nota_actual = float(context.args[0])
        porcentaje_evaluado = float(context.args[1])
        porcentaje_restante = 100 - porcentaje_evaluado
        nota_necesaria = (5 - (nota_actual * (porcentaje_evaluado / 100))) / (porcentaje_restante / 100)
        if nota_necesaria > 10:
            respuesta = f"Lo siento, necesitas un {nota_necesaria:.2f} en el examen final para aprobar, lo cual no es posible. ¡Pero no te rindas!"
        else:
            respuesta = f"Necesitas un {nota_necesaria:.2f} en el examen final para aprobar la asignatura. ¡Tú puedes lograrlo!"
    except (IndexError, ValueError):
        respuesta = "Por favor, usa el formato correcto: /aprobar <nota_actual> <porcentaje_evaluado>"
    await update.message.reply_text(respuesta)
       
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("aprobar", aprobar))
    application.add_handler(CommandHandler("ayuda", start))
    application.run_polling()
