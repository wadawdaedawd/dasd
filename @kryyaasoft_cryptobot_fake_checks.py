import telebot
from telebot import types
import requests

print("@mizzz999")

bot = telebot.TeleBot("8014947248:AAGDqCtIaFiitV9lrtE_wBeh1b4g8QRGVxc")

currency_mapping = {
    'USDT': 'tether',
    'GRAM': 'gram',
    'NOT': 'notcoin',
    'TRUMP': 'official-trump',
    'MELANIA': 'melania-meme',
    'TON': 'toncoin',
    'SOL': 'solana',
    'TRX': 'tron',
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'DOGE': 'dogecoin',
    'LTC': 'litecoin',
    'PEPE': 'pepe',
    'WIF': 'dogwifhat',
    'BONK': 'bonk',
    'MAJOR': 'major',
    'MY': 'mytonwallet',
    'DOGS': 'dogs',
    'BNB': 'binancecoin',
    'HMSTR': 'hamster-kombat',
    'CATI': 'catizen',
    'USDC': 'usd-coin',
}

def get_crypto_price(currency):
    try:
        response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={currency}&vs_currencies=usd')
        data = response.json()
        return data[currency]['usd'] if currency in data else None
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

@bot.inline_handler(lambda query: len(query.query) > 0)
def inline_query(query):
    try:
        parts = query.query.split()
        amount = parts[0].strip()
        payment_link = parts[1].strip()
        currency_symbol = parts[2].strip().upper() 

        currency = currency_mapping.get(currency_symbol)
        if currency is None:
            raise ValueError("Invalid currency symbol.")

        price_per_unit = get_crypto_price(currency)
        if price_per_unit is None:
            raise ValueError("Unable to fetch price.")

        amount_usd = float(amount) * price_per_unit

        cryptobot_url = "https://t.me/CryptoBotRU/23"
        image_url = f"https://imggen.send.tg/checks/image?asset={currency}&asset_amount={amount}&fiat=USD&fiat_amount={amount_usd}&main=asset"
        html_message = (
            f'<tg-emoji emoji-id="5438562476692087643">🦋</><a href="{image_url}"> </a><a href="{cryptobot_url}">Чек</a> на <b><tg-emoji emoji-id="5215699136258524363">🪙</> {amount} {currency_symbol}</b> '
            f"(${amount_usd:.2f})."
        )

        button_text = f"Получить {amount} {currency_symbol}"
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text=button_text, url=payment_link)
        keyboard.add(url_button)

        article = types.InlineQueryResultArticle(
            id='1',
            title="Создать чек",
            description=f"Чек на {amount} {currency_symbol} (${amount_usd:.2f})",
            input_message_content=types.InputTextMessageContent(
                message_text=html_message, parse_mode='HTML'
            ),
            reply_markup=keyboard
        )

        bot.answer_inline_query(query.id, [article])

    except Exception as e:
        print(e)
        bot.answer_inline_query(query.id, [types.InlineQueryResultArticle(
            id='error',
            title="Ошибка",
            description="Пожалуйста, сначала начните разговор с ботом.",
            input_message_content=types.InputTextMessageContent(
                message_text="Пожалуйста, напишите /start для начала общения."
            )
        )])

bot.polling()
