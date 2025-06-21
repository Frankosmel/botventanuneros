from aiogram import Bot, Dispatcher, types, executor
from config import BOT_TOKEN, ADMIN_ID
from utils.sms_activate import SMSActivateClient
import json
import os

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

sms = SMSActivateClient()

LOG_PATH = "data/logs.json"
if not os.path.exists(LOG_PATH):
    with open(LOG_PATH, "w") as f:
        json.dump([], f)

@dp.message_handler(commands=["start"])
async def start_cmd(msg: types.Message):
    await msg.reply("👋 ¡Bienvenido a @micuenta_ff_id_bot!

"
                    "Con este bot puedes comprar números virtuales 📱 para verificar cuentas como Telegram, WhatsApp y más.
"
                    "Usa /comprar para comenzar.")

@dp.message_handler(commands=["comprar"])
async def comprar_cmd(msg: types.Message):
    await msg.reply("🛍️ ¿Qué servicio necesitas?
Ejemplo: /numero telegram")

@dp.message_handler(commands=["numero"])
async def pedir_numero(msg: types.Message):
    try:
        service = msg.get_args().strip()
        if not service:
            await msg.reply("❗ Debes escribir un servicio. Ejemplo:
/numero telegram")
            return
        number_info = sms.obtener_numero(service)
        if not number_info:
            await msg.reply("❌ No hay números disponibles en este momento.")
            return
        numero, activation_id = number_info
        guardar_log(msg.from_user.id, service, numero, activation_id)
        await msg.reply(f"✅ Número generado:
📱 {numero}
🆔 Activación ID: {activation_id}

"
                        f"Cuando recibas el SMS, usa /codigo {activation_id} para ver el código.
"
                        f"Si deseas cancelar, usa /cancelar {activation_id}")
    except Exception as e:
        await msg.reply(f"⚠️ Error: {e}")

@dp.message_handler(commands=["codigo"])
async def codigo_cmd(msg: types.Message):
    activation_id = msg.get_args().strip()
    if not activation_id:
        await msg.reply("❗ Usa /codigo <activation_id>")
        return
    try:
        codigo = sms.obtener_codigo(activation_id)
        await msg.reply(f"🔐 Código recibido:
📩 {codigo}")
    except Exception as e:
        await msg.reply(f"⚠️ Error al obtener código: {e}")

@dp.message_handler(commands=["cancelar"])
async def cancelar_cmd(msg: types.Message):
    activation_id = msg.get_args().strip()
    if not activation_id:
        await msg.reply("❗ Usa /cancelar <activation_id>")
        return
    sms.cancelar_activacion(activation_id)
    await msg.reply("❌ Activación cancelada y reembolso solicitado.")

def guardar_log(user_id, servicio, numero, activation_id):
    with open(LOG_PATH, "r") as f:
        data = json.load(f)
    data.append({
        "usuario_id": user_id,
        "servicio": servicio,
        "numero": numero,
        "activation_id": activation_id
    })
    with open(LOG_PATH, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)