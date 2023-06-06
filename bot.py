from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging
from datetime import time
import schedule

CHAT_IDS = []
TELEGRAM_TOKEN = '5918475980:AAECzvqGQo3688uzPUHttPKplgN4xYq1_Hc'

bot = TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    chat_id = message.chat.id
    if chat_id not in CHAT_IDS:
        CHAT_IDS.append(chat_id)
    bot.send_message(
        chat_id=chat_id,
        text=f'Привет! Я бот, который будет напоминать тебе про '
             f'решение задач по математике перед экзаменом ЕГЭ. '
             f'Каждый день в 10 утра по Московскому времени предлагаю решить тест. '
             f'Нажми на кнопку, чтобы начать тест.',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Решить', url='https://ege.sdamgia.ru/test?a=own_test')]
        ])
    )
    logging.info(f"{user.username} ({user.id}) subscribed to the notifications.")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'start_test':
        chat_id = call.message.chat.id
        bot.send_message(
            chat_id=chat_id,
            text='Переходи по ссылке и начинай решать тест: '
                 'https://ege.sdamgia.ru/test?a=own_test'
        )


def send_notification():
    for chat_id in CHAT_IDS:
        bot.send_message(
            chat_id=chat_id,
            text='Решить ЕГЭ про математику (Профиль)',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Решить', callback_data='start_test')]
            ])
        )


def scheduled_jobs():
    try:
        bot.send_message(
            chat_id=CHAT_IDS[0],
            text="This is scheduled message sent once a minute."
        )
    except:
        print('scheduled_jobs() Error')


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    scheduled_time = time(hour=10, minute=00, second=00)
    try:
        bot.send_message(chat_id=CHAT_IDS[0], text=f"Notifications will be sent every day at {scheduled_time}")
    except:
        print('scheduled_jobs() Error')
    schedule.every().day.at("05:00").do(send_notification)
    bot.polling(none_stop=True)

while True:
    schedule.run_pending()
    time.sleep(1)
