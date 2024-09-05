#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters,
)

from pathlib import Path
import yaml  # pyyaml

from dotenv import load_dotenv
import os

load_dotenv(os.getcwd()+"/.env")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CHOOSING, ADMIN, TYPING_CHOICE = range(3)

reply_keyboard = [
    ["Пройти тест", "Результаты"],
]

ans_keyboard = [
    ["Да", "Нет"],
]

admin_keyboard = [
    ["Список вопросов", "Список ответов", ],
    ["Редактировать вопрос", "Редактировать ответ"],
    ["Добавить вопрос"], ["Удалить вопрос"],
     ["Вернуться в меню"],
]

QUESTIONS = {}
ANSWERS = {}
markup_reply = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
markup_ans = ReplyKeyboardMarkup(ans_keyboard, one_time_keyboard=True)
markup_admin = ReplyKeyboardMarkup(admin_keyboard, one_time_keyboard=True)


QUESTIONS = yaml.load(Path('questions.yaml').read_text(), Loader=yaml.SafeLoader)
ANSWERS = yaml.load(Path('answers.yaml').read_text(), Loader=yaml.SafeLoader)

def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation, display any stored data and ask user for input."""
    reply_text = f"Можете пройти тест или посмотреть результаты."
    
    await update.message.reply_text(reply_text, reply_markup=markup_reply)

    return CHOOSING


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """General response handler"""


    msg = update.message
    user = msg.from_user
    if (msg.text == "Пройти тест"):
        context.user_data['quiz'] = {}
        context.user_data['quiz']['answers'] = ""
    elif (msg.text == "Да"):
        context.user_data['quiz']['answers'] += '1'
    elif (msg.text == "Нет"):
        context.user_data['quiz']['answers'] += '0'

    # Debug
    # print(questions_left)
    # print(context.user_data['quiz']['answers'])
    # print(msg.text)

    if (len(QUESTIONS) == len(context.user_data['quiz']['answers'])):
        reply_text = f"Тест завершен!"
        # Посчитать result

        context.user_data['quiz']['results'] = context.user_data['quiz']['answers'] 
        await update.message.reply_text(reply_text, reply_markup=markup_reply)
    else:
        reply_text = QUESTIONS[len(context.user_data['quiz']['answers'])]['q']
        await update.message.reply_text(reply_text, reply_markup=markup_ans)

    

    return CHOOSING

async def results(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show results for user"""
    if 'quiz' not in context.user_data:
        reply_text = (
            "Нет данных. Вначале пройдите тест."
        )
    else:
        reply_text = f"Ваш результат {context.user_data['quiz']['results']}."


    await update.message.reply_text(reply_text, reply_markup=markup_reply)

    return CHOOSING

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    msg = update.message
    
    reply_text = ""

    if (msg.text == "Список вопросов"):
        for i in QUESTIONS:
            reply_text += f"{i['id']} : {i['q']}\n"
    elif (msg.text == "Список ответов"):
        pass
    elif (msg.text == "Редактировать вопрос"):
        pass
    elif (msg.text == "Редактировать ответ"):
        pass
    elif (msg.text == "Добавить вопрос"):
        pass
    elif (msg.text == "Удалить вопрос"):
        pass
    elif (msg.text == "Вернуться в меню"):
        reply_text = f"Можете пройти тест или посмотреть результаты."
        
        await update.message.reply_text(reply_text, reply_markup=markup_reply)

        return CHOOSING
    else:
        reply_text = "Выберете действие"

    await update.message.reply_text(reply_text, reply_markup=markup_admin)

    return ADMIN


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    if "choice" in context.user_data:
        del context.user_data["choice"]

    await update.message.reply_text(
        f"I learned these facts about you: {facts_to_str(context.user_data)}Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    persistence = PicklePersistence(filepath="conversationbot")
    application = Application.builder().token(os.getenv("TOKEN")).persistence(persistence).build()

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), CommandHandler("admin", admin_panel),],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^(Пройти тест|Да|Нет)$"), test
                ),
                MessageHandler(
                    filters.Regex("^(Результаты)$"), results
                ),
                CommandHandler(
                    "admin", admin_panel
                ),
            ],
            ADMIN: [
                MessageHandler(
                    filters.Regex("^(Список вопросов)$"), admin_panel
                ),
                MessageHandler(
                    filters.Regex("^(Список ответов)$"), admin_panel
                ),
                MessageHandler(
                    filters.Regex("^(Редактировать вопрос)$"), admin_panel
                ),
                MessageHandler(
                    filters.Regex("^(Редактировать ответ)$"), admin_panel
                ),
                MessageHandler(
                    filters.Regex("^(Добавить вопрос)$"), admin_panel
                ),
                MessageHandler(
                    filters.Regex("^(Удалить вопрос)$"), admin_panel
                ),
                MessageHandler(
                    filters.Regex("^(Вернуться в меню)$"), admin_panel
                ),
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
        name="my_conversation",
        persistent=True,
    )

    application.add_handler(conv_handler)

    # show_data_handler = CommandHandler("show_data", show_data)
    # application.add_handler(show_data_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()