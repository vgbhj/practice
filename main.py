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
from typing import Dict, Optional, Tuple

from telegram import Chat, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ChatMemberUpdated, ChatMember
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    CallbackContext,
    ChatMemberHandler,
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

CHOOSING, ADMIN, EDIT, ADD, REMOVE = range(5)

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
    ["Добавить чат"], ["Вернуться в меню"],
]

global QUESTIONS
global ANSWERS
markup_reply = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
markup_ans = ReplyKeyboardMarkup(ans_keyboard, one_time_keyboard=True)
markup_admin = ReplyKeyboardMarkup(admin_keyboard, one_time_keyboard=True)


QUESTIONS = yaml.load(Path('questions.yaml').read_text(), Loader=yaml.SafeLoader)
ANSWERS = yaml.load(Path('answers.yaml').read_text(), Loader=yaml.SafeLoader)
ADMINS = yaml.load(Path('admin.yaml').read_text(), Loader=yaml.SafeLoader)
ALLOWED_GROUP_ID = yaml.load(Path('groups.yaml').read_text(), Loader=yaml.SafeLoader)

async def track_group_member(update: Update, context: CallbackContext):
    """Track users who interact with the bot in the group."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    # Only track if the message is from the correct group
    if chat_id in ALLOWED_GROUP_ID:
        # Add the user to the list of group members in persistent storage
        group_members = context.bot_data.get('group_members', set())
        group_members.add(user_id)
        context.bot_data['group_members'] = group_members

def extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
    """Takes a ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
    of the chat and whether the 'new_chat_member' is a member of the chat. Returns None, if
    the status didn't change.
    """
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = old_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    is_member = new_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)

    return was_member, is_member

async def track_chats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tracks the chats the bot is in."""
    result = extract_status_change(update.my_chat_member)
    if result is None:
        return
    was_member, is_member = result

    # Let's check who is responsible for the change
    cause_name = update.effective_user.full_name

    # Handle chat types differently:
    chat = update.effective_chat
    if chat.type == Chat.PRIVATE:
        if not was_member and is_member:
            # This may not be really needed in practice because most clients will automatically
            # send a /start command after the user unblocks the bot, and start_private_chat()
            # will add the user to "user_ids".
            # We're including this here for the sake of the example.
            logger.info("%s unblocked the bot", cause_name)
            context.bot_data.setdefault("user_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s blocked the bot", cause_name)
            context.bot_data.setdefault("user_ids", set()).discard(chat.id)
    elif chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        if not was_member and is_member:
            logger.info("%s added the bot to the group %s", cause_name, chat.title)
            context.bot_data.setdefault("group_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s removed the bot from the group %s", cause_name, chat.title)
            context.bot_data.setdefault("group_ids", set()).discard(chat.id)
    elif not was_member and is_member:
        logger.info("%s added the bot to the channel %s", cause_name, chat.title)
        context.bot_data.setdefault("channel_ids", set()).add(chat.id)
    elif was_member and not is_member:
        logger.info("%s removed the bot from the channel %s", cause_name, chat.title)
        context.bot_data.setdefault("channel_ids", set()).discard(chat.id)


async def show_chats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows which chats the bot is in"""
    user_ids = ", ".join(str(uid) for uid in context.bot_data.setdefault("user_ids", set()))
    group_ids = ", ".join(str(gid) for gid in context.bot_data.setdefault("group_ids", set()))
    channel_ids = ", ".join(str(cid) for cid in context.bot_data.setdefault("channel_ids", set()))
    text = (
        f"@{context.bot.username} is currently in a conversation with the user IDs {user_ids}."
        f" Moreover it is a member of the groups with IDs {group_ids} "
        f"and administrator in the channels with IDs {channel_ids}."
    )
    await update.effective_message.reply_text(text)


async def greet_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greets new users in chats and announces when someone leaves"""
    result = extract_status_change(update.chat_member)
    if result is None:
        return

    was_member, is_member = result
    cause_name = update.chat_member.from_user.mention_html()
    member_name = update.chat_member.new_chat_member.user.mention_html()

    user_id = update.chat_member.new_chat_member.user.id
    group_members = context.bot_data.get('group_members', set())
    chat_id = update.effective_chat.id

    if chat_id in ALLOWED_GROUP_ID:
        if not was_member and is_member:
            group_members.add(user_id)
            context.bot_data['group_members'] = group_members
            print(
                f"{member_name} was added by {cause_name}. Welcome!"
            )

    elif was_member and not is_member:
        if user_id in group_members:
            group_members.remove(user_id)
            context.bot_data['group_members'] = group_members
        print(
            f"{member_name} is no longer with us. Thanks a lot, {cause_name} ..."
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation, display any stored data and ask user for input."""

    user_id = update.effective_user.id
    group_members = context.bot_data.get('group_members', set())
    
    # Check if the user is tracked as a group member
    if user_id in group_members:
        reply_text = f"Можете пройти тест или посмотреть результаты."
    
        await update.message.reply_text(reply_text, reply_markup=markup_reply)

        return CHOOSING
    else:
        await update.message.reply_text("You are not in the group, so you cannot interact with me in private.")



async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """General response handler"""

    QUESTIONS = yaml.load(Path('questions.yaml').read_text(), Loader=yaml.SafeLoader)
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
    reply_text = "Something went wrong"
    if 'quiz' not in context.user_data:
        reply_text = (
            "Нет данных. Вначале пройдите тест."
        )
    else:
        for i in ANSWERS:
            if i['code'] == context.user_data['quiz']['results']:
                reply_text = f"Ваш результат {i['ans']}."


    await update.message.reply_text(reply_text, reply_markup=markup_reply)

    return CHOOSING

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.effective_user.username not in ADMINS:
        return

    
    QUESTIONS = yaml.load(Path('questions.yaml').read_text(), Loader=yaml.SafeLoader)
    ANSWERS = yaml.load(Path('answers.yaml').read_text(), Loader=yaml.SafeLoader)
    ALLOWED_GROUP_ID = yaml.load(Path('groups.yaml').read_text(), Loader=yaml.SafeLoader)
    
    msg = update.message
    
    reply_text = ""
    

    if (msg.text == "Список вопросов"):
        for i in QUESTIONS:
            reply_text += f"{i['id']} : {i['q']}\n"

    elif (msg.text == "Список ответов"):
        if ANSWERS:
            for i in ANSWERS:
                human_read = "-".join('да' if x == '1' else 'нет' for x in i['code'])
                reply_text += f"{i['id']}. ({human_read}): {i['ans']}\n"

    elif (msg.text == "Редактировать вопрос"):
         context.user_data['edit'] = 'question'

         reply_text = "Введите номер вопроса"

         await update.message.reply_text(reply_text)
         
         return EDIT

    elif (msg.text == "Редактировать ответ"):
         context.user_data['edit'] = 'answer'

         reply_text = "Введите номер ответа"

         await update.message.reply_text(reply_text)
         
         return EDIT

    elif (msg.text == "Добавить вопрос"):
        context.user_data['add'] = 'question'

        reply_text = "Введите вопрос"

        await update.message.reply_text(reply_text)
        return ADD
    elif (msg.text == "Удалить вопрос"):
        context.user_data['remove'] = 'question'

        reply_text = "Введите номер вопроса"

        await update.message.reply_text(reply_text)
        return REMOVE
    elif (msg.text == "Добавить чат"):
        context.user_data['add'] = 'chat'

        reply_text = "Введите id чата"

        await update.message.reply_text(reply_text)
        return ADD
    elif (msg.text == "Вернуться в меню"):
        reply_text = f"Можете пройти тест или посмотреть результаты."
        
        await update.message.reply_text(reply_text, reply_markup=markup_reply)

        return CHOOSING
    else:
        reply_text = "Выберете действие"

    if reply_text == "":
        reply_text = "Пусто"

    await update.message.reply_text(reply_text, reply_markup=markup_admin)

    return ADMIN

async def edit_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    msg = update.message
    
    QUESTIONS = yaml.load(Path('questions.yaml').read_text(), Loader=yaml.SafeLoader)
    ANSWERS = yaml.load(Path('answers.yaml').read_text(), Loader=yaml.SafeLoader)
    reply_text = ""

    edit = ""
    if 'edit' in context.user_data:
        edit = context.user_data['edit']

    if edit:
        if msg.text.isdigit():
            id = int(msg.text) - 1
            if edit == 'question':
                if id >= 0 and id < len(QUESTIONS):
                    context.user_data['edit_id'] = id
                    reply_text = "Введите вопрос"
                    await update.message.reply_text(reply_text)
                    return EDIT
                else:
                    reply_text = "Неверный номер!"
            if edit == 'answer':
                if id >= 0 and id < len(ANSWERS):
                    context.user_data['edit_id'] = id
                    reply_text = "Введите ответ"
                    await update.message.reply_text(reply_text)
                    return EDIT
                else:
                    reply_text = "Неверный номер!"

    
    await update.message.reply_text(reply_text, reply_markup=markup_admin)

    return ADMIN

async def edit_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    msg = update.message
    
    reply_text = "Edited"
    QUESTIONS = yaml.load(Path('questions.yaml').read_text(), Loader=yaml.SafeLoader)
    ANSWERS = yaml.load(Path('answers.yaml').read_text(), Loader=yaml.SafeLoader)

    edit = ""
    edit_id = -1
    if 'edit' in context.user_data:
        edit = context.user_data['edit']
    
    if 'edit_id' in context.user_data:
        edit_id = context.user_data['edit_id']
    
    if edit_id != -1:
        if edit == 'question':
            QUESTIONS[edit_id]['q'] = msg.text
            with open("questions.yaml", 'w') as file:
                yaml.dump(QUESTIONS, file, default_flow_style=False, allow_unicode=True)
        if edit == 'answer':
            ANSWERS[edit_id]['ans'] = msg.text
            with open("answers.yaml", 'w') as file:
                yaml.dump(ANSWERS, file, default_flow_style=False, allow_unicode=True)
        context.user_data['edit'] = None
        context.user_data['edit_id'] = None
    else:
        reply_text = "Something went wrong!"
    
    await update.message.reply_text(reply_text, reply_markup=markup_admin)

    return ADMIN

def update_answers():

    QUESTIONS = yaml.load(Path('questions.yaml').read_text(), Loader=yaml.SafeLoader)
    ANSWERS = yaml.load(Path('answers.yaml').read_text(), Loader=yaml.SafeLoader)
    ANSWERS = []
    n = 2**len(QUESTIONS)
    for i in range(2**len(QUESTIONS)):
        n -= 1
        bin_n = str(bin(n)[2:])
        tmp_dict = {'ans' : f"Ответ {i+1}", 'code' : '0'*(len(QUESTIONS)-len(bin_n)) + bin_n, 'id': i+1}
        ANSWERS.append(tmp_dict)
        with open("answers.yaml", 'w') as file:
            yaml.dump(ANSWERS, file, default_flow_style=False, allow_unicode=True)


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    msg = update.message


    QUESTIONS = yaml.load(Path('questions.yaml').read_text(), Loader=yaml.SafeLoader)

    reply_text = "Added"
    add = ""

    if 'add' in context.user_data:
        add = context.user_data['add']

    if add:
        if add == 'question':
            QUESTIONS.append({'id' : len(QUESTIONS)+1, 'q' : msg.text})
            with open("questions.yaml", 'w') as file:
                yaml.dump(QUESTIONS, file, default_flow_style=False, allow_unicode=True)

            update_answers()
        if add == 'chat':
            if msg.text[1:].isdigit():
                ALLOWED_GROUP_ID.append(int(msg.text))
                with open("groups.yaml", 'w') as file:
                    yaml.dump(ALLOWED_GROUP_ID, file, default_flow_style=False, allow_unicode=True)
            else:
                reply_text = "Неверный номер!"


    await update.message.reply_text(reply_text, reply_markup=markup_admin)

    return ADMIN


async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    msg = update.message
    reply_text = "Deleted"
    remove = "Something went wrong!"
    
    QUESTIONS = yaml.load(Path('questions.yaml').read_text(), Loader=yaml.SafeLoader)

    if 'remove' in context.user_data:
        remove = context.user_data['remove']
    
    if remove:
        if msg.text.isdigit():
            id = int(msg.text) - 1
            if remove == 'question':
                if id >= 0 and id < len(QUESTIONS):
                    tmp_q = []

                    for i in range(len(QUESTIONS)):
                        if i != id:
                            QUESTIONS[i]['id'] = i+1
                            tmp_q.append(QUESTIONS[i])

                    QUESTIONS = tmp_q
                    with open("questions.yaml", 'w') as file:
                        yaml.dump(QUESTIONS, file, default_flow_style=False, allow_unicode=True)

                    update_answers()
                else:
                    reply_text = "Неверный номер!"
            
        else:
            reply_text = "Неверный номер!"


    await update.message.reply_text(reply_text, reply_markup=markup_admin)

    return ADMIN

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    if "choice" in context.user_data:
        del context.user_data["choice"]

    await update.message.reply_text(
        f"...",
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
                    filters.Regex("^(Добавить чат)$"), admin_panel
                ),
                MessageHandler(
                    filters.Regex("^(Вернуться в меню)$"), admin_panel
                ),
            ],
            EDIT:[
                MessageHandler(
                    filters.Regex("^[0-9]*$"), edit_id
                ),
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), edit_text
                ),
            ],
            ADD:[
                MessageHandler(
                    filters.Regex("^[0-9]*$"), add
                ),
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), add
                ),
            ],
            REMOVE:[
                MessageHandler(
                    filters.Regex("^[0-9]*$"), remove
                ),
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
        name="my_conversation",
        persistent=True,
    )

    application.add_handler(conv_handler)

    group_filter = filters.ChatType.GROUPS | filters.ChatType.SUPERGROUP
    application.add_handler(MessageHandler(group_filter, track_group_member))

    # Keep track of which chats the bot is in
    application.add_handler(ChatMemberHandler(track_chats, ChatMemberHandler.MY_CHAT_MEMBER))
    application.add_handler(CommandHandler("show_chats", show_chats))

    # Handle members joining/leaving chats.
    application.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER))



    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()