import telebot
import json
from datetime import datetime,timedelta

SAVE_FILE = 'user_gardens.json'

#@MyGardennBot

token = ""
bot = telebot.TeleBot(token)

def load_data():
    try:
        with open(SAVE_FILE,'r',encoding='utf-8') as file:
            data = json.load(file)
            for user_id in data:
                if 'last_used' in data[user_id]:
                    data[user_id]['last_used'] = datetime.fromisoformat(data[user_id]['last_used'])
            return data
    except FileNotFoundError:
        return {}


def save_data():
    data_to_save = {}
    for user_id in user_gardens:
        data_to_save[user_id] = {
            'garden': user_gardens[user_id]['garden'],
            'last_used': user_gardens[user_id]['last_used'].isoformat()
        }
    with open(SAVE_FILE, 'w',encoding='utf-8') as file:
        json.dump(data_to_save,file,ensure_ascii=False,indent=2)


def moods():
    text = ("Список эмодзи:\n"
            "🌞 - Солнышко \n"
            "Настроение - Радость, оптимизм\n"
            "Растение - Подсолнух(🌻)\n"
            "🌧️ - Дождь \n"
            "Настроение - Грусть\n"
            "Растение - Завядший цветок(🥀)\n"
            "⚡ - Молния \n"
            "Настроение - Энергичность\n"
            "Растение - Кактус(🌵)\n"
            "❤️ - Сердце\n"
            "Настроение - Любовь,нежность\n"
            "Растение - Роза(🌹)\n"
            "🌙 - Луна\n"
            "Настроение - Умиротворение,мечтательность\n"
            "Растение - Лунный цветок(🌼)\n"
            "🌈 - Радуга\n"
            "Настроение - Вдохновение\n"
            "Растение - Цветок вдохновения(🌺)\n"
            "🍃 - Листок\n"
            "Настроение - Спокойствие,гармония\n"
            "Растение - Клевер (☘️) \n"
            "🎉 - Фейерверк \n"
            "Настроение - Праздник,восторг\n"
            "Растение - Праздничная пальма(🌴)\n"
            "💡 - Лампочка \n"
            "Настроение - Озарение,любопытство \n"
            "Растение - Гриб(🍄)\n"
            "🔥 - Огонь\n"
            "Настроение - Тревога,суета\n"
            "Растение - Дерево(🌳) \n")
    return text

user_gardens = load_data()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь эмодзи настроения, и я посажу растение в твой сад! 🌸\n"
                          "Используй эмодзи из списка: 🌞, 🌧️, ⚡, ❤️, 🌙, 🌈, 🍃, 🎉, 💡, 🔥")

@bot.message_handler(commands=['help'])
def show_commands(message):
    bot.send_message(message.chat.id, "Вот все команды данного бота: \n"
                                      "/garden - Посмотреть мой сад\n"
                                      "/mood - Посмотреть список эмодзи\n"
                                      "/cooldown - Оставшееся время до посадки")


@bot.message_handler(commands=['garden'])
def show_garden(message):
    user_id = str(message.from_user.id)
    garden = user_gardens.get(user_id, {}).get('garden', 'Твой сад ещё пуст... 🌱')
    bot.send_message(message.chat.id, f"Твой сад:\n"
                                      f"{garden}")

@bot.message_handler(commands=['cooldown'])
def cooldown_time(message):
    user_id = str(message.from_user.id)
    now = datetime.now()
    user_data = user_gardens.get(user_id, {})
    last_used = user_data.get('last_used', datetime.min)
    if now - last_used < timedelta(minutes=1):
        next_time = last_used + timedelta(minutes=1)
        wait_minutes = int((next_time - now).total_seconds() // 60)
        bot.send_message(message.chat.id, f"⏳ Чтобы посадить растение нужно подождать {wait_minutes} минут!")
    else:
        bot.send_message(message.chat.id,"Можно посадить растение!")

@bot.message_handler(commands=['mood'])
def show_mood(message):
    text = moods()
    bot.send_message(message.chat.id,text)



@bot.message_handler(content_types=['text'])
def handle_mood(message):
    user_id = str(message.from_user.id)
    mood = message.text.strip()

    plants = {"🌞": "🌻","🌧️": "🥀","⚡": "🌵","❤️": "🌹",
              "🌙": "🌼","🌈": "🌺","🍃": "☘️","🎉": "🌴",
              "💡": "🍄","🔥": "🌳"
    }
    plant = plants.get(mood, None)

    if not plant:
        bot.send_message(message.chat.id,"Эмодзи не найденно")
        return

    now = datetime.now()
    user_data = user_gardens.get(user_id, {})
    last_used = user_data.get('last_used', datetime.min)

    if now - last_used < timedelta(hours=1):
        next_time = last_used + timedelta(hours=1)
        wait_minutes = int((next_time - now).total_seconds() // 60)
        bot.send_message(message.chat.id, f"⏳ Следующее растение можно посадить через {wait_minutes} минут!")
        return

    if user_id not in user_gardens:
        user_gardens[user_id] = {'garden': plant, 'last_used': now}
    else:
        garden = user_gardens[user_id]['garden']
        garden += plant
        user_gardens[user_id]['garden'] = garden
        user_gardens[user_id]['last_used'] = now

    save_data()
    bot.send_message(message.chat.id, f"+ {plant}\n"
                                      f"Сад обновлен!\n"
                                      f"{user_gardens[user_id]['garden']}")



bot.polling()