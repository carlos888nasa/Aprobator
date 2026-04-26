from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

SELECCIONANDO_OPCION, ESPERANDO_TIEMPO = range(2)

async def pomodoro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    teclado = [
        [
            InlineKeyboardButton("1 Hora 🍅", callback_data='pomo_60'),
            InlineKeyboardButton("2 Horas 🔥", callback_data='pomo_120')
        ],
        [
            InlineKeyboardButton("3 Horas 🦾", callback_data='pomo_180'),
            InlineKeyboardButton("4 Horas 🧠", callback_data='pomo_240')
        ],
        [
            InlineKeyboardButton("Elegir tiempo manual ✍️", callback_data='pomo_custom')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(teclado)
    await update.message.reply_text("¡Hora de ponerse a estudiar! Elige tu sesión de estudio:", reply_markup=reply_markup)
    return SELECCIONANDO_OPCION

async def boton_pomodoro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    datos_boton = query.data

    if datos_boton == 'pomo_custom':
        await query.edit_message_text("✍️ Escribe en números cuántos minutos totales quieres estudiar (ejemplo: 150):")
        return ESPERANDO_TIEMPO
    minutos_pedidos = int(datos_boton.split('_')[1])
    pomodoro_totales = minutos_pedidos // 30
    
    mis_datos = {'totales': pomodoro_totales, 'completado': 0}
    await query.edit_message_text(f"🚀 ¡Modo Bestia! Programados {pomodoro_totales} bloques de estudio.\nEmpieza el primer ciclo de 25 min. ¡A por todas!")
    context.job_queue.run_once(alarma_estudio, 25 * 60, chat_id=query.message.chat_id, data=mis_datos)
    return ConversationHandler.END
    
async def alarma_estudio(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    datos = job.data
    datos['completado'] += 1

    if datos ['completado'] % 4 == 0:
        tiempo_descanso = 15*60
        txt = f"🏆 ¡Ciclo {datos['completados']} terminado! Te toca descanso LARGO (15 min)."
    else:
        tiempo_descanso = 5*60
        txt = f"✅ ¡Ciclo {datos['completados']} terminado! Te toca descanso CORTO (5 min)."
    await context.bot.send_message(chat_id=context.job.chat_id, text = txt) 
    context.job_queue.run_once(alarma_descanso, tiempo_descanso, chat_id=job.chat_id, data=datos)

async def alarma_descanso(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    datos = job.data

    if datos['completado'] >= datos['totales']:
        await context.bot.send_message(chat_id=context.job.chat_id, text=f"🎉 ¡Felicidades! Has completado los {datos['totales']} ciclos de estudio. ¡Tómate un merecido descanso largo! 🏖️")

    await context.bot.send_message(chat_id=job.chat_id, text=f"⏰ ¡Descanso terminado! Hora de volver a estudiar para el ciclo {datos['completados'] + 1}. ¡Tú puedes lograrlo!")
    context.job_queue.run_once(alarma_estudio, 25*60, chat_id=job.chat_id, data=datos)

async def proceso_manual(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    texto_usuario = update.message.text
    chat_id = update.message.chat_id
    
    if not texto_usuario.isdigit():
        await update.message.reply_text("Por favor, ingresa un número válido de minutos.")
        return ESPERANDO_TIEMPO
    
    minutos_pedidos = int(texto_usuario)
    pomodoro_totales = minutos_pedidos // 30

    if pomodoro_totales == 1:
        pomodoro_totales = 1 

    mis_datos = {'totales': pomodoro_totales, 'completados': 0}
    
    await update.message.reply_text(f"🍅 ¡Perfecto! Calculados {pomodoro_totales} bloques para tus {minutos_pedidos} minutos.\n¡Empieza el Ciclo 1!")
    
    context.job_queue.run_once(alarma_estudio, 25 * 60, chat_id=chat_id, data=mis_datos)
    
    return ConversationHandler.END

async def cancelar_pomodoro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛑 Configuración de Pomodoro cancelada. ¡Descansa!")
    return ConversationHandler.END
