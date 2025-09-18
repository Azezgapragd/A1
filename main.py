import telebot
from telebot import types

# ضع التوكن الخاص بك هنا
bot = telebot.TeleBot("7665778378:AAEDTKrO57bQSELMQuwv2v-TxOFWMTmeR4o")

numbers = {}
cntr = 0
flagOfDo = 0
result = 1

# /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global flagOfDo, cntr, result, numbers
    bot.send_message(message.chat.id, "اهلاً بك")
    bot.send_message(message.chat.id, "أرسل الرقم الأول")
    flagOfDo = 1
    cntr = 0
    result = 1
    numbers = {}

# استقبال الأرقام
@bot.message_handler(func=lambda message: True)
def handle_numbers(message):
    global cntr, flagOfDo, result, numbers

    try:
        numbers[cntr] = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "من فضلك أرسل رقم صحيح")
        return

    if cntr == 1:  # عندنا رقمين
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("*", callback_data="mul"))
        markup.add(types.InlineKeyboardButton("%", callback_data="div"))
        markup.add(types.InlineKeyboardButton("+", callback_data="add"))
        markup.add(types.InlineKeyboardButton("-", callback_data="sub"))
        bot.send_message(message.chat.id, "إختر العملية الحسابية:", reply_markup=markup)
        cntr = 0
        result = 0
        return

    if result == 1:
        if flagOfDo == 1:
            bot.send_message(message.chat.id, "أرسل الرقم الثاني")
            flagOfDo = 0
            cntr = 1
        else:
            bot.send_message(message.chat.id, "أرسل الرقم الأول")
            flagOfDo = 1

# معالجة ضغط الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global numbers, result
    op = call.data

    try:
        if op == "div":
            res = numbers[0] / numbers[1]
        elif op == "mul":
            res = numbers[0] * numbers[1]
        elif op == "add":
            res = numbers[0] + numbers[1]
        elif op == "sub":
            res = numbers[0] - numbers[1]
        else:
            bot.answer_callback_query(call.id, "عملية غير صحيحة!")
            return

        bot.send_message(call.message.chat.id, f"نتيجتك: {res}")
        bot.send_message(call.message.chat.id, "أدخل /start للبدء من جديد")
        result = 1
        numbers = {}

    except Exception:
        bot.send_message(call.message.chat.id, "خطأ في العملية الحسابية، حاول مرة أخرى")
        result = 1
        numbers = {}

print("البوت شغال ...")
bot.infinity_polling()
