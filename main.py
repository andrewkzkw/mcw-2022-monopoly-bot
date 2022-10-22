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
    sticker_id = "CAACAgIAAxkBAAEGIbVjTthulEWlhBEI_77ZSv1qZ1RGFAACSCQAAq5_WUqvrZ3eFcHvFCoE"
    greeting = f'Привет, {message.from_user.first_name}. Меня зовут Полик, и я {emoji.emojize(":red_heart:")} играть в монополию. Поздравляю тебя с успешной регистрацией и желаю хорошей карьерной недели! Чтобы увидеть, что я умею - нажми на кнопку "Меню".'
    bot.send_sticker(message.chat.id, sticker_id)
    bot.send_message(message.chat.id, greeting, parse_mode="html")


@bot.message_handler(commands=["brands"])
def brands_handler(message):
    brands = sheet.get_records_by_telegram_id(message.chat.id)
    answer = 'Твоя коллекция:\n'
    if brands:
        bot.send_message(message.chat.id, f'Подожди немного, я считаю твои бренды.')
        for br in brands.keys():
            answer += f'{br} {brands[br]}\n'
        bot.send_message(message.chat.id, f"{answer}")
    else:
        bot.send_message(message.chat.id, f'У тебя еще нет брендов. Чтобы собрать бренды, приходи на мероприятия MCW. Я очень жду тебя{emoji.emojize(":red_heart:")}')


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
    rules = f'Правила моей монополии даже понятнее, чем у оригинальной игры. Погнали!\n\n<b>1. Регистрация</b>\nРегистрация была произведена автоматически после нажатия команды "Старт"\n{emoji.emojize(":check_mark:")}Поздравляю, ты в игре!\n\n<b>2. Как заработать бренды?</b>\nНикаких сложных квестов, главное — искренняя вовлеченность в ивенты недели!\n{emoji.emojize(":star:")}   Посещай мероприятия и получай бренд одного из цветов за каждое из них;\n{emoji.emojize(":star:")}   Занимай призовые места в квизах, бизнес-играх и чемпионатах. За это я подарю тебе желтый бренд;\n{emoji.emojize(":star:")}   Активно участвуй в мероприятии, задавай вопросы спикеру и получишь +1 фиолетовый бренд в свою копилку;\n{emoji.emojize(":star:")}   Покупай кофе у моих друзей, вскрывай стикеры и ты получишь шанс выиграть дополнительно бренд одного из трех цветов;\n{emoji.emojize(":star:")}   Ищи пасхалки. Достаточно просто отправить мне сообщение с правильным ответом и я подарю тебе бренд;\n{emoji.emojize(":star:")}   Last but not least: заполняй форму фидбэка после каждого мероприятия MCW, чтобы заполучить бренд и точно забрать свой подарок!\n\n<b>3. Как узнать, сколько брендов в моей коллекции?</b>\nЧтобы посмотреть свои бренды, напиши в чат /brands или выбери эту команду в "Меню". Можешь попробовать прямо сейчас!\n\n<b>4. Ура, <u>бренды</u> собраны! А как получить приз?</b>\nПервое и самое основное — приходи на воскресные мероприятия Management Career Week. Затем выбери в меню команду /prize, чтобы узнать свой уникальный ID. Дальше все просто: назови указанный ID организаторам, чтобы забрать подарок {emoji.emojize(":party_popper:")}\n\n<b>5. Что означают цвета брендов?</b>\nЦвет бренда - это обменный курс. Желтый бренд дает тебе 3 балла, фиолетовый - 2 балла, а зеленый - 1 балл. В конце недели я посчитаю все баллы и назову имена победителей!\n\n<b>6. Что делать, если у меня остались вопросы?</b>\nЕсли ответа на твой вопрос нет в правилах и FAQ, обязательно напиши @andre1kazakoff.'
    bot.send_message(call.message.chat.id, rules, parse_mode="html")


@bot.callback_query_handler(func=lambda call: call.data == "faq")
def faq_handler(call):
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_monopoly = types.KeyboardButton("Монополия")
    item_registration = types.KeyboardButton("Регистрация")
    item_brands = types.KeyboardButton("Бренды")
    item_colors = types.KeyboardButton("Цвета")
    item_prize = types.KeyboardButton("Приз")
    item_other = types.KeyboardButton("Другое")
    markup_reply.add(
        item_monopoly,
        item_registration,
        item_brands,
        item_colors,
        item_prize,
        item_other
    )
    bot.send_message(call.message.chat.id, "Частые вопросы", reply_markup=markup_reply)


@bot.message_handler(
    func=lambda message: message.text.split()[0].lower() in ["бля", "ебать", "блять", "сука", "пизда", "хуй", "работяга", "1301", "балтика", "ласковая", "макроэкономика", "кузнецов", "андрей", "сингапур", "amazon", "импортозамещение", "тимбилдинг", "децентрализация", "гистограмма", "ниокр", "скрининг", "gucci", "python", "8b13", "845f", "49ad", "0592", "98dd", "a84f", "e076", "7d00", "33c1", "358e", "dc05", "a144", "49da", "9f6f", "a068", "715c", "ae30", "5e2d", "a386", "d12b", "a7bd", "789a", "b042", "2d8c", "05f2", "a9e7", "4c33", "b5b7", "a927", "1159", "283d1", "179a4", "0e064", "e29cc", "0eb1d", "eca06", "81eb0", "40833", "bf903", "cf909", "83ae9", "f95c8", "cac77"]
)
def activities_handler(message):
    try:
        command, args = map(str, message.text.split())
    except:
        command, args = message.text, ''
    actions = {
        "ебать": [
            datetime(year=2022, month=10, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "бля": [
            datetime(year=2022, month=10, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "блять": [
            datetime(year=2022, month=10, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "сука": [
            datetime(year=2022, month=10, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "пизда": [
            datetime(year=2022, month=10, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "хуй": [
            datetime(year=2022, month=10, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "работяга": [
            datetime(year=2022, month=10, day=19, hour=0, minute=30, second=0),
            datetime(year=2022, month=10, day=29, hour=20, minute=50, second=0),
        ],
        "1301": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "балтика": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "ласковая": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "макроэкономика": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "кузнецов": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "андрей": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "сингапур": [
            datetime(year=2022, month=11, day=7, hour=17, minute=0, second=0),
            datetime(year=2022, month=11, day=7, hour=19, minute=30, second=0),
        ],
        "amazon": [
            datetime(year=2022, month=11, day=7, hour=18, minute=15, second=0),
            datetime(year=2022, month=11, day=7, hour=20, minute=45, second=0),
        ],
        "импортозамещение": [
            datetime(year=2022, month=11, day=8, hour=18, minute=15, second=0),
            datetime(year=2022, month=11, day=8, hour=20, minute=45, second=0),
        ],
        "тимбилдинг": [
            datetime(year=2022, month=11, day=8, hour=20, minute=0, second=0),
            datetime(year=2022, month=11, day=8, hour=22, minute=30, second=0),
        ],
        "децентрализация": [
            datetime(year=2022, month=11, day=9, hour=18, minute=15, second=0),
            datetime(year=2022, month=11, day=9, hour=20, minute=45, second=0),
        ],
        "гистограмма": [
            datetime(year=2022, month=11, day=9, hour=20, minute=0, second=0),
            datetime(year=2022, month=11, day=9, hour=22, minute=30, second=0),
        ],
        "ниокр": [
            datetime(year=2022, month=11, day=10, hour=18, minute=45, second=0),
            datetime(year=2022, month=11, day=10, hour=21, minute=15, second=0),
        ],
        "скрининг": [
            datetime(year=2022, month=11, day=10, hour=18, minute=45, second=0),
            datetime(year=2022, month=11, day=10, hour=21, minute=15, second=0),
        ],
        "gucci": [
            datetime(year=2022, month=11, day=11, hour=18, minute=45, second=0),
            datetime(year=2022, month=11, day=11, hour=21, minute=15, second=0),
        ],
        "python": [
            datetime(year=2022, month=11, day=11, hour=18, minute=45, second=0),
            datetime(year=2022, month=11, day=11, hour=21, minute=15, second=0),
        ],
        "8b13": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "845f": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "49ad": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "0592": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "98dd": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "a84f": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "e076": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "7d00": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "33c1": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "358e": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "dc05": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "a144": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "49da": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "9f6f": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "a068": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "715c": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "ae30": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "5e2d": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "a386": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "d12b": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "a7bd": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "789a": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "b042": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "2d8c": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "05f2": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "a9e7": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "4c33": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "b5b7": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "a927": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "1159": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "283d1": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "179a4": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "0e064": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "e29cc": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "0eb1d": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "eca06": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "81eb0": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "40833": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "bf903": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "cf909": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "83ae9": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "f95c8": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ],
        "cac77": [
            datetime(year=2022, month=11, day=1, hour=0, minute=0, second=0),
            datetime(year=2022, month=11, day=11, hour=23, minute=59, second=59),
        ]
    }
    now_time = datetime.now()
    action = actions[command.lower()]
    is_in_time = now_time in datetimerange.DateTimeRange(action[0], action[1])
    if is_in_time:
        if "работяга" in command.lower():
            sheet.insert_row([message.chat.id, "работяга"])
            sticker_id = "CAACAgIAAxkBAAEGIbFjTthrMpevSPtnal3iRhSfRJeqUgADJgACa45ZSkb35B6_Ol0eKgQ"
            bot.send_sticker(message.chat.id, sticker_id)
            bot.send_message(message.chat.id, f"приветики, я работаю, все ок")
        elif "1301" in command.lower():
            sheet.insert_row([message.chat.id, "1301"])
            sticker_id = "CAACAgIAAxkBAAEGIa9jTthpGUDfoXwq8VBX-KVnbSHRLgAC4SMAAjhFWUoDFuY6SUpQ0ioE"
            bot.send_sticker(message.chat.id, sticker_id)
            bot.send_message(message.chat.id, f"Это было легко, не правда ли? Ты получаешь +1 зеленый бренд за найденную пасхалку!")
        elif "балтика" in command.lower():
            sheet.insert_row([message.chat.id, "балтика"])
            sticker_id = "CAACAgIAAxkBAAEGIbFjTthrMpevSPtnal3iRhSfRJeqUgADJgACa45ZSkb35B6_Ol0eKgQ"
            bot.send_sticker(message.chat.id, sticker_id)
            bot.send_message(message.chat.id, f"Пасхалка найдена! Поздравляю, +1 зеленый бренд в твоей копилке!")
        elif "ласковая" in command.lower():
            sheet.insert_row([message.chat.id, "ласковая"])
            sticker_id = "CAACAgIAAxkBAAEGIbFjTthrMpevSPtnal3iRhSfRJeqUgADJgACa45ZSkb35B6_Ol0eKgQ"
            bot.send_sticker(message.chat.id, sticker_id)
            bot.send_message(message.chat.id, f"Анастасия Кирилловна Ласковая - преподаватель, которого я загадал. Поздравляю, фиолетовый бренд твой!")
        elif "макроэкономика" in command.lower():
            sheet.insert_row([message.chat.id, "макроэкономика"])
            sticker_id = "CAACAgIAAxkBAAEGIa9jTthpGUDfoXwq8VBX-KVnbSHRLgAC4SMAAjhFWUoDFuY6SUpQ0ioE"
            bot.send_sticker(message.chat.id, sticker_id)
            bot.send_message(message.chat.id, f"Пары Евгения Валерьевича - это искусство... Искусство любить Набиуллину. За найденную пасхалку я дарю тебе 1 фиолетовый бренд.")
        elif "кузнецов" in command.lower():
            sheet.insert_row([message.chat.id, "кузнецов"])
            sticker_id = "CAACAgIAAxkBAAEGIbFjTthrMpevSPtnal3iRhSfRJeqUgADJgACa45ZSkb35B6_Ol0eKgQ"
            bot.send_sticker(message.chat.id, sticker_id)
            bot.send_message(message.chat.id, f"Иииии... Ты получаешь 1 желтый бренд за найденного Егора!")
        elif "андрей" in command.lower():
            sheet.insert_row([message.chat.id, "андрей"])
            sticker_id = "CAACAgIAAxkBAAEGIa9jTthpGUDfoXwq8VBX-KVnbSHRLgAC4SMAAjhFWUoDFuY6SUpQ0ioE"
            bot.send_sticker(message.chat.id, sticker_id)
            bot.send_message(message.chat.id, f"Секретная пасхалка от создателя бота! В твоей коллекции пополнение: +1 желтый бренд!")
        elif "сингапур" in command.lower():
            sheet.insert_row([message.chat.id, "сингапур"])
            sticker_id = "CAACAgIAAxkBAAEGIatjTthliHRBIt2pkJqNLfn2deO7lQACdyIAAkjqWEpKKf_6cTk7eyoE"
            bot.send_sticker(message.chat.id, sticker_id)
            bot.send_message(message.chat.id, f"Правильно! Я загадал Сингапур. Придется отдать тебе заслуженный зеленый бренд)")
        elif "amazon" in command.lower():
            sheet.insert_row([message.chat.id, "amazon"])
            sticker_id = "CAACAgIAAxkBAAEGIatjTthliHRBIt2pkJqNLfn2deO7lQACdyIAAkjqWEpKKf_6cTk7eyoE"
            bot.send_sticker(message.chat.id, sticker_id)
            bot.send_message(message.chat.id, f"Раньше на логотипе этой компании была изображена река Амазонка, а сама компания называется Amazon. За правильный ответ я даю тебе фиолетовый бренд.")
        elif "импортозамещение" in command.lower():
            sheet.insert_row([message.chat.id, "импортозамещение"])
            sticker_id = "CAACAgIAAxkBAAEGIatjTthliHRBIt2pkJqNLfn2deO7lQACdyIAAkjqWEpKKf_6cTk7eyoE"
            bot.send_sticker(message.chat.id, sticker_id)
            bot.send_message(message.chat.id, f"Это правильный ответ)\n\nДержи от меня желтый бренд.")
        elif "тимбилдинг" in command.lower():
            sheet.insert_row([message.chat.id, "тимбилдинг"])
            sticker_id = "CAACAgIAAxkBAAEGIatjTthliHRBIt2pkJqNLfn2deO7lQACdyIAAkjqWEpKKf_6cTk7eyoE"
            bot.send_sticker(message.chat.id, sticker_id)
            bot.send_message(message.chat.id, f"Правильно! Проверь свои бренды, у тебя пополнение)")
        elif "децентрализация" in command.lower():
            sheet.insert_row([message.chat.id, "децентрализация"])
            sticker_id = "CAACAgIAAxkBAAEGIatjTthliHRBIt2pkJqNLfn2deO7lQACdyIAAkjqWEpKKf_6cTk7eyoE"
            bot.send_sticker(message.chat.id, sticker_id)
            bot.send_message(message.chat.id, f"DAO - decentralized autonomous organization.\n\nЗагаданное слово - децентрализация. Засчитываю! Получи один зеленый бренд.")
        elif "гистограмма" in command.lower():
            sheet.insert_row([message.chat.id, "гистограмма"])
            sticker_id = "CAACAgIAAxkBAAEGIatjTthliHRBIt2pkJqNLfn2deO7lQACdyIAAkjqWEpKKf_6cTk7eyoE"
            bot.send_sticker(message.chat.id, sticker_id)
            bot.send_message(message.chat.id, f"Молодец, правильно! Дарю тебе фиолетовый бренд.")
        elif "ниокр" in command.lower():
            sheet.insert_row([message.chat.id, "ниокр"])
            sticker_id = "CAACAgIAAxkBAAEGIatjTthliHRBIt2pkJqNLfn2deO7lQACdyIAAkjqWEpKKf_6cTk7eyoE"
            bot.send_sticker(message.chat.id, sticker_id)
            bot.send_message(message.chat.id, f"НИОКР - это научно-исследовательские и опытно-конструкторские работы.\n\nВсе правильно, бери фиолетовый сбренд.")
        elif "скрининг" in command.lower():
            sheet.insert_row([message.chat.id, "скрининг"])
            sticker_id = "CAACAgIAAxkBAAEGIatjTthliHRBIt2pkJqNLfn2deO7lQACdyIAAkjqWEpKKf_6cTk7eyoE"
            bot.send_sticker(message.chat.id, sticker_id)
            bot.send_message(message.chat.id, f"Верно! +1 фиолетовый бренд твой.")
        elif "gucci" in command.lower():
            sheet.insert_row([message.chat.id, "gucci"])
            sticker_id = "CAACAgIAAxkBAAEGIatjTthliHRBIt2pkJqNLfn2deO7lQACdyIAAkjqWEpKKf_6cTk7eyoE"
            bot.send_sticker(message.chat.id, sticker_id)
            bot.send_message(message.chat.id, f"Gucci - загаданный мной бренд, а конгломерат называется Kering.\n\nПолучи от меня 1 зеленый бренд.")
        elif "python" in command.lower():
            sheet.insert_row([message.chat.id, "python"])
            sticker_id = "CAACAgIAAxkBAAEGIatjTthliHRBIt2pkJqNLfn2deO7lQACdyIAAkjqWEpKKf_6cTk7eyoE"
            bot.send_sticker(message.chat.id, sticker_id)
            bot.send_message(message.chat.id, f"Загаданный язык программирования - Python. Кстати, я тоже был создан с помощью Python)\n\nЗабирай 1 зеленый бренд себе.")
        elif "8b13" in command.lower():
            sheet.insert_row([message.chat.id, "8b13"])
            bot.send_message(message.chat.id, f"Вот удача! Ты получаешь желтый бренд!")
        elif "845f" in command.lower():
            sheet.insert_row([message.chat.id, "845f"])
            bot.send_message(message.chat.id, f"Вот удача! Ты получаешь желтый бренд!")
        elif "49ad" in command.lower():
            sheet.insert_row([message.chat.id, "49ad"])
            bot.send_message(message.chat.id, f"Вот удача! Ты получаешь желтый бренд!")
        elif "0592" in command.lower():
            sheet.insert_row([message.chat.id, "0592"])
            bot.send_message(message.chat.id, f"Вот удача! Ты получаешь желтый бренд!")
        elif "98dd" in command.lower():
            sheet.insert_row([message.chat.id, "98dd"])
            bot.send_message(message.chat.id, f"Вот удача! Ты получаешь желтый бренд!")
        elif "a84f" in command.lower():
            sheet.insert_row([message.chat.id, "a84f"])
            bot.send_message(message.chat.id, f"Везение на твоей стороне! Дарю тебе фиолетовый бренд!")
        elif "e076" in command.lower():
            sheet.insert_row([message.chat.id, "e076"])
            bot.send_message(message.chat.id, f"Везение на твоей стороне! Дарю тебе фиолетовый бренд!")
        elif "7d00" in command.lower():
            sheet.insert_row([message.chat.id, "7d00"])
            bot.send_message(message.chat.id, f"Везение на твоей стороне! Дарю тебе фиолетовый бренд!")
        elif "33c1" in command.lower():
            sheet.insert_row([message.chat.id, "33c1"])
            bot.send_message(message.chat.id, f"Везение на твоей стороне! Дарю тебе фиолетовый бренд!")
        elif "358e" in command.lower():
            sheet.insert_row([message.chat.id, "358e"])
            bot.send_message(message.chat.id, f"Везение на твоей стороне! Дарю тебе фиолетовый бренд!")
        elif "dc05" in command.lower():
            sheet.insert_row([message.chat.id, "dc05"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "a144" in command.lower():
            sheet.insert_row([message.chat.id, "a144"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "49da" in command.lower():
            sheet.insert_row([message.chat.id, "49da"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "9f6f" in command.lower():
            sheet.insert_row([message.chat.id, "9f6f"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "a068" in command.lower():
            sheet.insert_row([message.chat.id, "a068"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "715c" in command.lower():
            sheet.insert_row([message.chat.id, "715c"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "ae30" in command.lower():
            sheet.insert_row([message.chat.id, "ae30"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "5e2d" in command.lower():
            sheet.insert_row([message.chat.id, "5e2d"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "a386" in command.lower():
            sheet.insert_row([message.chat.id, "a386"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "d12b" in command.lower():
            sheet.insert_row([message.chat.id, "d12b"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "a7bd" in command.lower():
            sheet.insert_row([message.chat.id, "a7bd"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "789a" in command.lower():
            sheet.insert_row([message.chat.id, "789a"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "b042" in command.lower():
            sheet.insert_row([message.chat.id, "b042"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "2d8c" in command.lower():
            sheet.insert_row([message.chat.id, "2d8c"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "05f2" in command.lower():
            sheet.insert_row([message.chat.id, "05f2"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "a9e7" in command.lower():
            sheet.insert_row([message.chat.id, "a9e7"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "4c33" in command.lower():
            sheet.insert_row([message.chat.id, "4c33"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "b5b7" in command.lower():
            sheet.insert_row([message.chat.id, "b5b7"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "a927" in command.lower():
            sheet.insert_row([message.chat.id, "a927"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "1159" in command.lower():
            sheet.insert_row([message.chat.id, "1159"])
            bot.send_message(message.chat.id, f"Юхууу! +1 зеленый бренд в твоей копилке!")
        elif "283d1" in command.lower():
            sheet.insert_row([message.chat.id, "283d1"])
            bot.send_message(message.chat.id, f"Ты получаешь желтый бренд!")
        elif "179a4" in command.lower():
            sheet.insert_row([message.chat.id, "179a4"])
            bot.send_message(message.chat.id, f"Ты получаешь желтый бренд!")
        elif "0e064" in command.lower():
            sheet.insert_row([message.chat.id, "0e064"])
            bot.send_message(message.chat.id, f"Ты получаешь желтый бренд!")
        elif "e29cc" in command.lower():
            sheet.insert_row([message.chat.id, "e29cc"])
            bot.send_message(message.chat.id, f"Ты получаешь желтый бренд!")
        elif "0eb1d" in command.lower():
            sheet.insert_row([message.chat.id, "0eb1d"])
            bot.send_message(message.chat.id, f"Ты получаешь желтый бренд!")
        elif "eca06" in command.lower():
            sheet.insert_row([message.chat.id, "eca06"])
            bot.send_message(message.chat.id, f"Ты получаешь фиолетовый бренд!")
        elif "81eb0" in command.lower():
            sheet.insert_row([message.chat.id, "81eb0"])
            bot.send_message(message.chat.id, f"Ты получаешь фиолетовый бренд!")
        elif "40833" in command.lower():
            sheet.insert_row([message.chat.id, "40833"])
            bot.send_message(message.chat.id, f"Ты получаешь фиолетовый бренд!")
        elif "bf903" in command.lower():
            sheet.insert_row([message.chat.id, "bf903"])
            bot.send_message(message.chat.id, f"Ты получаешь фиолетовый бренд!")
        elif "cf909" in command.lower():
            sheet.insert_row([message.chat.id, "cf909"])
            bot.send_message(message.chat.id, f"Ты получаешь фиолетовый бренд!")
        elif "83ae9" in command.lower():
            sheet.insert_row([message.chat.id, "83ae9"])
            bot.send_message(message.chat.id, f"Ты получаешь зеленый бренд!")
        elif "f95c8" in command.lower():
            sheet.insert_row([message.chat.id, "f95c8"])
            bot.send_message(message.chat.id, f"Ты получаешь зеленый бренд!")
        elif "cac77" in command.lower():
            sheet.insert_row([message.chat.id, "cac77"])
            bot.send_message(message.chat.id, f"Ты получаешь зеленый бренд!")
        elif "ебать" in command.lower():
            sticker_id = "CAACAgIAAxkBAAEGIbNjTthsKeKEfOxcd5uj80z3QYYsUgACihwAAuYyWUpbDMF28ky5RSoE"
            bot.send_sticker(message.chat.id, sticker_id)
        elif "блять" in command.lower():
            sticker_id = "CAACAgIAAxkBAAEGIbNjTthsKeKEfOxcd5uj80z3QYYsUgACihwAAuYyWUpbDMF28ky5RSoE"
            bot.send_sticker(message.chat.id, sticker_id)
        elif "сука" in command.lower():
            sticker_id = "CAACAgIAAxkBAAEGIbNjTthsKeKEfOxcd5uj80z3QYYsUgACihwAAuYyWUpbDMF28ky5RSoE"
            bot.send_sticker(message.chat.id, sticker_id)
        elif "пизда" in command.lower():
            sticker_id = "CAACAgIAAxkBAAEGIbNjTthsKeKEfOxcd5uj80z3QYYsUgACihwAAuYyWUpbDMF28ky5RSoE"
            bot.send_sticker(message.chat.id, sticker_id)
        elif "хуй" in command.lower():
            sticker_id = "CAACAgIAAxkBAAEGIbNjTthsKeKEfOxcd5uj80z3QYYsUgACihwAAuYyWUpbDMF28ky5RSoE"
            bot.send_sticker(message.chat.id, sticker_id)
        elif "бля" in command.lower():
            sticker_id = "CAACAgIAAxkBAAEGIbNjTthsKeKEfOxcd5uj80z3QYYsUgACihwAAuYyWUpbDMF28ky5RSoE"
            bot.send_sticker(message.chat.id, sticker_id)
    else:
        sticker_id = "CAACAgIAAxkBAAEGIa1jTthohn6NeLMb220_bfw1Zze72AACvCMAAwVYSs32_u6RYcgEKgQ"
        bot.send_sticker(message.chat.id, sticker_id)
        bot.send_message(message.chat.id, "К сожалению, я не могу принять такой ответ. Либо он неправильный, либо мой функционал не предусматривает ответ на твое сообщение.")


@bot.message_handler(content_types=["text"])
def faq_and_err_handler(message):
    faq_responses = {
        "Монополия": f'Монополия MCW — это новый, интерактивный способ получить памятные призы для самых активных участников карьерной недели!{emoji.emojize(":fire:")}\n\nВсе просто: посещай мероприятия, побеждай в соревнованиях, ищи пасхалки, покупай кофе и будь активным, чтобы заработать бренды. Накопленные бренды помогут тебе не уйти с пустыми руками в финальный день Management Career Week{emoji.emojize(":wrapped_gift:")}',
        "Бренды": f'Портфель брендов будет зависеть от твоей вовлеченности: чем чаще ты посещаешь мероприятия и активно участвуешь в них, тем выше шанс получить больше брендов.\n\nМожет быть, ты и есть та самая акула бизнеса, которая соберет все бренды?{emoji.emojize(":winking_face:")}',
        "Регистрация": f'Чтобы участвовать в монополии, необходима регистрация на MCW: твой уникальный id при регистрации на события недели автоматически добавит тебя в игру и будет задействован в монополии.\n\nЭто позволит тебе точно получить заслуженный приз{emoji.emojize(":money_bag:")}, а мне — оценить популярность ивентов и сделать карьерную неделю еще лучше!',
        "Приз": f'Если у тебя не получается прийти за подарком в воскресенье, не переживай. В случае победы я точно не оставлю тебя без вознаграждения! Напиши @andre1kazakoff, чтобы выбрать любой другой удобный день для вручения приза.\n\nНо учти: если я не смогу встретиться с тобой в воскресенье, я буду очень сильно грустить {emoji.emojize(":crying_face:")}',
        "Другое": f"Нет ответа на вопрос? Напиши моему создателю @andre1kazakoff, он поможет тебе.",
        "Цвета": f"Бренды бывают 3 цветов: желтые (они дают по 3 балла), фиолетовые (2 балла) и зеленые (1 балл). В конце MCW я посчитаю твои баллы и объявлю результат!"
    }

    if message.text in faq_responses.keys():
        bot.send_message(message.chat.id, faq_responses[message.text])

    else:
        bot.send_message(
            message.chat.id,
            f"К сожалению, я не могу принять такой ответ. Либо он неправильный, либо мой функционал не предусматривает ответ на твое сообщение.",
        )

bot.infinity_polling(timeout=10, long_polling_timeout = 5)
