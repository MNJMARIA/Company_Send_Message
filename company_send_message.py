from quart import Quart, request, jsonify
from telethon import TelegramClient

app = Quart(__name__)

api_id = '17860937'
api_hash = '6bdbb8eae683414b8d13798b2b37640b'
client = TelegramClient('company_message_session', api_id, api_hash)

@app.before_serving
async def startup():
    await client.start()  # Підключаємося до Telegram клієнта
    print("Telegram client started")

@app.after_serving
async def shutdown():
    await client.disconnect()
    print("Telegram client disconnected")

async def send_message(phone_number, message):
    try:
        print(f"Відправляємо повідомлення на номер: {phone_number}")
        await client.send_message(phone_number, message)
        print("Повідомлення надіслано успішно")
    except Exception as e:
        print(f"Помилка в send_message: {e}")
        raise e

@app.route('/send_message', methods=['POST'])
async def send_greeting():
    data = await request.get_json()
    phone_number = data.get('phone_number')
    message = data.get('message')

    if not phone_number or not message:
        return jsonify({"status": "error", "message": "Phone number or message is missing"}), 400

    try:
        await send_message(phone_number, message)
        return jsonify({"status": "success", "message": f"Message sent to {phone_number}"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to send message: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
