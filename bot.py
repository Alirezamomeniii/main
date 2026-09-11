import telebot
from telebot import types
from pprint import pprint
from services import UserService,TicketService
from services import Database, UserService, TicketService


bot = telebot.TeleBot("8617341248:AAFq5_eVqREdxOjjz3Y0OzxXcUx5AFuefnk")

database = Database()

users = UserService(database)
tickets = TicketService(database)
titles = {}


@bot.message_handler(commands=["start"])
def start(message):

    users.add_user(message.from_user.id,message.from_user.username)

    keyboard =types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add("ثبت درخواست 📝")
    keyboard.add("درخواست‌های من 📋")
    keyboard.add("راهنما ℹ️")

    bot.send_message(message.chat.id,"به سیستم پشتیبانی خوش آمدید 🌹",reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "ثبت درخواست 📝")
def create_ticket(message):

    bot.send_message(message.chat.id,"موضوع درخواست را وارد کنید:")

    bot.register_next_step_handler(message, get_title)


def get_title(message):

    titles[message.from_user.id] = message.text

    bot.send_message(message.chat.id,"توضیحات درخواست را وارد کنید:")

    bot.register_next_step_handler(message, get_description)


def get_description(message):

    ticket = tickets.create_ticket(message.from_user.id,titles[message.from_user.id],message.text)

    bot.send_message(message.chat.id,f"درخواست ثبت شد ✅\n\n"f"شماره: #{ticket.id}\n"f"موضوع: {ticket.title}\n"f"وضعیت: {ticket.status}")


@bot.message_handler(func=lambda message: message.text == "درخواست‌های من 📋")
def my_tickets(message):

    result = tickets.get_user_tickets(message.from_user.id)

    if len(result) == 0:

        bot.send_message(message.chat.id,"شما هنوز درخواستی ثبت نکرده‌اید.")

        return

    keyboard = types.InlineKeyboardMarkup()

    for ticket in result:

        button =types.InlineKeyboardButton(f"{ticket.status}-{ticket.title}-#{ticket.id}",callback_data=str(ticket.id))

        keyboard.add(button)

    bot.send_message(message.chat.id,"📋 درخواست‌های شما:",reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def ticket_details(call):

    ticket_id =int(call.data)

    ticket =tickets.get_ticket(ticket_id)

    bot.answer_callback_query(call.id)

    bot.send_message(
        call.message.chat.id,f"🎫 درخواست #{ticket.id}\n\n"f"📌 موضوع: {ticket.title}\n\n"f"📝 توضیحات: {ticket.description}\n\n"
        f"📊 وضعیت: {ticket.status}\n"f"🕐 تاریخ: {ticket.created_at.strftime('%Y/%m/%d %H:%M')}")


@bot.message_handler(func=lambda message: message.text== "راهنما ℹ️")
def help(message):

    bot.send_message(message.chat.id,"ℹ️ راهنمای سیستم\n\n""📝 ثبت درخواست → ایجاد درخواست جدید\n\n"
                    "📋 درخواست‌های من → مشاهده درخواست‌ها\n\n""🎫 روی هر درخواست بزنید → مشاهده جزئیات")

if __name__=="__main__":
    pprint("run")
    bot.infinity_polling()