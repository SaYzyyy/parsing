import telebot
import time
import datetime
import json
import random
import os
from photos_parse import main as main_photo
from wb_parse_async import main as main_text

TOKEN = '7963701545:AAFp_Ep-0ai1hNHBrmkv9ZmABCfmUgWB25U'
bot = telebot.TeleBot(TOKEN)

CHANNEL_ID = '@wbwithoutbill'

# CHANNELS = {
#     'Электроника': '@wbwithoutbill',
#     'Красота': '@wbwithoutbillkrasota',
# }

# main_text()

@bot.message_handler(content_types=['text'])
def commands(message):

    try:

        if 'зап' in message.text.lower():

            with open('parse_results/result.json', 'r', encoding='utf-8') as file:

                data = json.load(file)

            for index in range(1, 100000000):

                if isinstance(data, list) and len(data) > 0:

                    random_item = random.choice(data)

                    c_article = random_item.get('Артикул')
                    print(c_article)

                    with open('parse_results/articles.txt', 'r', encoding='utf-8') as file1:

                        if str(c_article) in file1.readline():

                            data.remove(random_item)

                            index-=1

                            print('__________________________________________________')
                            print('\nКарточка удалена!!!')
                            print('__________________________________________________\n')

                        elif str(c_article) not in file1.readline():

                            if random_item.get('Ссылка') is not None:

                                c_article = random_item.get('Артикул')
                                c_name = random_item.get('Название')
                                c_link = random_item.get('Ссылка')
                                c_shop = random_item.get('Магазин')
                                c_pricebig = random_item.get('Цена без скидки')
                                c_pricelow = random_item.get('Цена со скидкой')
                                c_rating = random_item.get('Рейтинг')
                                c_kategory = random_item.get('Категория')

                                main_photo(c_link)

                                time.sleep(30)

                                card = f'<b><a href="{c_link}">{c_name}</a></b>\n' \
                                    f'Магазин: {c_shop}\n' \
                                    f'<s>Цена без скидки: {c_pricebig}</s>\n' \
                                    f'<ins>Цена со скидкой: {c_pricelow}</ins>\n' \
                                    f'Оценка: {c_rating}\n' \
                                    f'<b><span class="tg-spoiler">НАЖМИ ПО НАЗВАНИЮ, ЧТОБЫ ПЕРЕЙТИ НА ТОВАР В ПРИЛОЖЕНИЕ))</span></b>\n'

                                # CHANNEL_ID = CHANNELS.get(c_kategory, '@wbwithoutbill')

                                with open(f'parse_images/image_{c_article}.jpeg', 'rb') as photo1:
                                    bot.send_photo(CHANNEL_ID, photo=photo1, caption=card, parse_mode='HTML')

                                with open('parse_results/articles.txt', 'a', encoding='utf-8') as file2:
                                    file2.write(str(c_article))

                                data.remove(random_item)

                                with open("parse_results/result.json", "w", encoding="utf-8") as file1:
                                    json.dump(data, file1, ensure_ascii=False)

                                print('__________________________________________________')
                                print(f'\nКарточка отправлена в канал {CHANNEL_ID} и удалена!!!')
                                print('__________________________________________________\n')
                                
                                if index%5==0:
                                    time.sleep(900)

                            else:

                                print('Ссылка отсутствует, карточка не отправлена.')

    except Exception as e:

        print(f'Ошибка: {e}')

bot.polling()