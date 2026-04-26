from telegram import Update
from telegram.ext import ContextTypes


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