import os
import requests
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler

# Load environment variables from .env file
load_dotenv()

# Telegram bot token
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Stock symbol and Nadariya Watson indicator zone parameters
STOCK_SYMBOL = 'AAPL'  # Replace with your desired stock symbol
NADARIYA_WATSON_ZONE = (100, 200)  # Replace with your desired zone

# Function to check the stock price
def check_stock_price(context):
    url = f'https://api.marketstack.com/v1/eod/latest?access_key={os.getenv("MARKETSTACK_API_KEY")}&symbols={STOCK_SYMBOL}'
    response = requests.get(url)
    data = response.json()

    if 'data' in data and len(data['data']) > 0:
        stock_price = data['data'][0]['close']
        if NADARIYA_WATSON_ZONE[0] <= stock_price <= NADARIYA_WATSON_ZONE[1]:
            send_alert(context, f"The stock price of {STOCK_SYMBOL} is in the Nadariya Watson indicator zone: {stock_price}")
    else:
        send_alert(context, "Failed to fetch stock data.")

# Function to send alert message via Telegram
def send_alert(context, message):
    context.bot.send_message(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text=message)

# Telegram command handler
def start(update, context):
    context.job_queue.run_repeating(check_stock_price, interval=60, first=0, context=update.message.chat_id)

# Initialize the Telegram bot
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Register the start command
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Start the bot
updater.start_polling()
