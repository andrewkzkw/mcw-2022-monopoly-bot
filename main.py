from datetime import datetime
import datetimerange
import emoji
from telebot import types, TeleBot
import json
from google_sheets import GoogleSheet

settings = json.loads(open(file="secrets.json", mode="r", encoding="UTF-8").read())
bot = TeleBot(token=settings["telegram_token"])
sheet = GoogleSheet(
    google_sheet_link=settings["google_sheet_link"],
    google_auth_file_path=settings["google_auth_file_path"],
)


@bot.message_handler(commands=["start"])
def start_handler(message):
    sticker_id = "CAACAgQAAxkBAAEF-fRjOJQ9_PVrCFv2NZPdVXkOS6pAIQACFgoAArHxyVOb0JkKNVNU_yoE"  # TODO:  сюда вставить ID стикера
    greeting = f'Привет, {message.from_user.first_name}. Меня зовут Полик и я {emoji.emojize(":red_heart:")} играть в монополию. Поздравляю тебя с успешной регистрацией и желаю хорошей карьерной недели! Чтобы увидеть, что я умею - нажми на кнопку "Меню".'
    bot.send_sticker(message.chat.id, sticker_id)
    bot.send_message(message.chat.id, greeting, parse_mode="html")


@bot.message_handler(commands=["brands"])
def brands_handler(message):
    brands = sheet.get_records_by_telegram_id(message.chat.id)
    answer = 'Ваши бренды:\n'
    if brands:  # if != None
        for br in brands.keys():
            answer += f"{br} ({brands[br]} / 3)\n"
        bot.send_message(message.chat.id, f"{answer}")
    else:
        bot.send_message(message.chat.id, "У вас еще нет брендов!")


@bot.message_handler(commands=["prize"])
def prize_handler(message):
    participant_id = message.from_user.id
    prize_message = f'Твой ID: <b>{participant_id}</b>. Скажи его организаторам в воскресенье и забирай свои призы!'
    bot.send_message(message.chat.id, prize_message, parse_mode="html")


@bot.message_handler(commands=["question"])
def question_handler(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_rules = types.InlineKeyboardButton(text="Правила", callback_data="rules")
    item_faq = types.InlineKeyboardButton(text="FAQ", callback_data="faq")
    markup_inline.add(item_rules, item_faq)
    bot.send_message(message.chat.id, "Чем я могу тебе помочь?", reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: call.data == "rules")
def rules_handler(call):
    rules = f'Правила моей монополии даже понятнее, чем у оригинальной игры. Погнали!\n\n<b>1. Регистрация</b>\nРегистрация была произведена автоматически после нажатия команды "Старт"\n{emoji.emojize(":check_mark:")}Поздравляю, ты в игре!\n\n<b>2. Как заработать бренды и собрать <u>бизнес-центр</u>?</b>\nНикаких сложных квестов, главное — искренняя вовлеченность в ивенты недели!\n{emoji.emojize(":star:")}   Посещай мероприятия и получай 1 бренд за каждое из них;\n{emoji.emojize(":star:")}   Занимай призовые места в квизах, бизнес-играх и чемпионатах, за это я подарю тебе любой бренд на твой выбор;\n{emoji.emojize(":star:")}   Активно участвуй в мероприятии, задавай вопросы спикеру — получишь +1 желаемый бренд в свою копилку;\n{emoji.emojize(":star:")}   Last but not least: заполняй форму фидбэка после каждого мероприятия MCW, чтобы заполучить бренд и точно забрать свой подарок!\n\n<b>3. Как узнать, сколько брендов в моей коллекции?</b>\nЧтобы посмотреть свои бренды и бизнес-центры, достаточно написать в чат /brands или выбрать эту команду в "Меню". Можешь попробовать прямо сейчас!\n\n<b>4. Ура, <u>бизнес-центр</u> собран! А как получить приз?</b>\nПервое и самое основное — приходи на воскресные мероприятия Management Career Week. Затем выбери в меню команду, чтобы узнать свой уникальный ID. Дальше все просто: назови указанный ID организаторам, чтобы забрать подарок {emoji.emojize(":party_popper:")}\n\n<b>5. Что делать, если у меня остались вопросы?</b>\nЕсли ответа на твой вопрос нет в правилах и FAQ, обязательно напиши @andre1kazakoff.'
    bot.send_message(call.message.chat.id, rules, parse_mode="html")

@bot.callback_query_handler(func=lambda call: call.data == "faq")
def faq_handler(call):
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_monopoly = types.KeyboardButton("Монополия")
    item_brands = types.KeyboardButton("Бренды")
    item_registration = types.KeyboardButton("Регистрация")
    item_prize = types.KeyboardButton("Приз")
    item_business_centre = types.KeyboardButton("Бизнес-центры")
    item_other = types.KeyboardButton("Другое")
    markup_reply.add(
        item_monopoly,
        item_brands,
        item_registration,
        item_prize,
        item_business_centre,
        item_other,
    )
    bot.send_message(call.message.chat.id, "Частые вопросы", reply_markup=markup_reply)


@bot.message_handler(
    func=lambda message: message.text.split()[0].lower() in ["вшм", "аналитик", "маркетинг"]
)
def activities_handler(message):
    try:
        command, args = map(str, message.text.split())
    except:
        command, args = message.text, ''
    actions = {
        #ТЕСТОВЫЕ ИВЕНТЫ
        "вшм": [
            datetime(year=2022, month=10, day=15, hour=12, minute=30, second=0),
            datetime(year=2022, month=10, day=15, hour=20, minute=50, second=0),
        ],
        "аналитик": [
            datetime(year=2022, month=10, day=15, hour=13, minute=2, second=0),
            datetime(year=2022, month=10, day=15, hour=20, minute=0, second=0),
        ],
        "маркетинг": [
            datetime(year=2022, month=10, day=15, hour=13, minute=0, second=0),
            datetime(year=2022, month=10, day=16, hour=23, minute=0, second=0),
        ],
        #ОФИЦИАЛЬНЫЕ ИВЕНТЫ В ТЕЧЕНИЕ НЕДЕЛИ
        "китай": [#карьера в странах азии
            datetime(year=2022, month=11, day=7, hour=16, minute=0, second=0),
            datetime(year=2022, month=11, day=7, hour=17, minute=30, second=0),
        ],
        "ребрендинг": [#с чистого листа: ребрендинг известных компаний
            datetime(year=2022, month=11, day=7, hour=17, minute=45, second=0),
            datetime(year=2022, month=11, day=7, hour=18, minute=45, second=0),
        ],
        "импорт": [#лекарство от всех болезней - параллельный импорт
            datetime(year=2022, month=11, day=8, hour=17, minute=45, second=0),
            datetime(year=2022, month=11, day=8, hour=18, minute=45, second=0),
        ],
        "команда": [#team design
            datetime(year=2022, month=11, day=8, hour=19, minute=0, second=0),
            datetime(year=2022, month=11, day=8, hour=20, minute=30, second=0),
        ],
        "веб3": [#web1, web2, web3
            datetime(year=2022, month=11, day=9, hour=17, minute=45, second=0),
            datetime(year=2022, month=11, day=9, hour=18, minute=45, second=0),
        ],
        "Дорожный": [#дата-сторителлинг
            datetime(year=2022, month=11, day=9, hour=19, minute=0, second=0),
            datetime(year=2022, month=11, day=9, hour=20, minute=30, second=0),
        ],
        "фармацевтика": [#запуск инновационного продукта
            datetime(year=2022, month=11, day=10, hour=17, minute=45, second=0),
            datetime(year=2022, month=11, day=10, hour=19, minute=15, second=0),
        ],
        "оффер": [#заветный job-offer
            datetime(year=2022, month=11, day=10, hour=17, minute=45, second=0),
            datetime(year=2022, month=11, day=10, hour=19, minute=15, second=0),
        ],
        "мода": [#смотря какой fabric
            datetime(year=2022, month=11, day=11, hour=17, minute=45, second=0),
            datetime(year=2022, month=11, day=11, hour=19, minute=15, second=0),
        ],
        "айтишник": [#уйти в айти
            datetime(year=2022, month=11, day=11, hour=17, minute=45, second=0),
            datetime(year=2022, month=11, day=11, hour=19, minute=15, second=0),
        ],
        "линчевание": [#бизнес-линч
            datetime(year=2022, month=11, day=12, hour=13, minute=0, second=0),
            datetime(year=2022, month=11, day=12, hour=15, minute=0, second=0),
        ],
        "йога": [#ловим дзен
            datetime(year=2022, month=11, day=13, hour=11, minute=0, second=0),
            datetime(year=2022, month=11, day=13, hour=12, minute=0, second=0),
        ],
        "фейлы": [#gsom ups & downs
            datetime(year=2022, month=11, day=13, hour=12, minute=0, second=0),
            datetime(year=2022, month=11, day=13, hour=13, minute=30, second=0),
        ],
        "кейс": [#ивент с кейс-клубом
            datetime(year=2022, month=11, day=13, hour=14, minute=30, second=0),
            datetime(year=2022, month=11, day=13, hour=16, minute=30, second=0),
        ],
        #ПРОЧИЕ СПОСОБЫ НАКОПИТЬ БАЛЛЫ
        "код": [#за победу в мероприятии 1
            datetime(year=2022, month=11, day=7, hour=10, minute=0, second=0),
            datetime(year=2022, month=11, day=13, hour=18, minute=0, second=0),
        ],
        "фидбек": [#за заполнение фидбека
            datetime(year=2022, month=11, day=7, hour=10, minute=0, second=0),
            datetime(year=2022, month=11, day=13, hour=18, minute=0, second=0),
        ],
        "вопросы": [#за активное участие и вопросы
            datetime(year=2022, month=11, day=7, hour=10, minute=0, second=0),
            datetime(year=2022, month=11, day=13, hour=18, minute=0, second=0),
        ]
    }
    now_time = datetime.now()
    action = actions[command.lower()]
    is_in_time = now_time in datetimerange.DateTimeRange(action[0], action[1])
    if is_in_time:
        if "вшм" in command.lower():
            sheet.insert_row([message.chat.id, "вшм"])
            bot.send_message(message.chat.id, f"это правильный ответ vmsh")
        elif "аналитик" in command.lower():
            sheet.insert_row([message.chat.id, "аналитик"])
            bot.send_message(message.chat.id, f"это правильный ответ analytic")
        elif "Дорожный" in command.lower():
            sheet.insert_row([message.chat.id, "аналитик"])
            bot.send_message(message.chat.id, f"это правильный ответ analytic")
        elif "маркетинг" in command.lower():
            sheet.insert_row([message.chat.id, "маркетинг"])
            bot.send_message(message.chat.id, f"это правильный ответ marketing")
    else:
        bot.send_message(
            message.chat.id,
            "Время события еще не пришло или ответ был отправлен после окончания события! К сожалению, я не могу принять такой ответ",
        )


@bot.message_handler(content_types=["text"])
def faq_and_err_handler(message):
    faq_responses = {
        "Монополия": f'Монополия MCW — это новый, интерактивный способ получить памятные призы для самых активных участников карьерной недели!{emoji.emojize(":fire:")} Посещай мероприятия, побеждай в соревнованиях и будь активным, чтобы заработать бренды — аналог улиц монополии. Накопленные бренды помогут тебе не уйти с пустыми руками в финальный день Management Career Week{emoji.emojize(":wrapped_gift:")}',
        "Бренды": f'Все будет зависеть от твоей вовлеченности: чем чаще ты посещаешь мероприятия и активно участвуешь в них, тем выше шанс получить больше брендов.\n\nМожет быть, ты и есть та самая акула бизнеса, которая соберет все бренды?{emoji.emojize(":winking_face:")}',
        "Регистрация": f'Чтобы участвовать в монополии, необходима регистрация на MCW: твой уникальный id при регистрации на MCW будет задействован и в монополии. Это позволит тебе точно получить заслуженный приз{emoji.emojize(":money_bag:")}, а нам — оценить популярность ивентов и сделать карьерную неделю еще лучше!',
        "Приз": f'Если прийти в воскресенье за подарком не получается - не переживай. В случае победы мы точно не оставим тебя без подарка! Напиши @andre1kazakoff, чтобы выбрать любой другой удобный день для вручения приза.\n\nНо учти: если я не смогу встретиться с тобой в воскресенье, я буду очень сильно грустить {emoji.emojize(":crying_face:")}',
        "Бизнес-центры": f'В зависимости от цвета бизнес-центра тебе потребуется собрать от двух до трех брендов:\n\n{emoji.emojize(":blue_square:")}   Альфа-Банк, Nexign, Балтика\n{emoji.emojize(":red_square:")}   Компания 1, Технологии Доверия, Burger King Italy\n{emoji.emojize(":green_square:")}   SBS Consulting, Б1',
        "Другое": f"Нет ответа на вопрос? Напиши @andre1kazakoff, он поможет тебе",
    }

    if message.text in faq_responses.keys():
        bot.send_message(message.chat.id, faq_responses[message.text])

    else:
        bot.send_message(
            message.chat.id,
            f"К сожалению, это неправильный ответ. либо мой функционал не предусматривает ответ на это сообщение",
        )

bot.polling(none_stop=True)