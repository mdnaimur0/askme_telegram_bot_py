from creds import BOT_TOKEN
from pytgbot import Bot
from models import User
from pytgbot.api_types.receivable.updates import Update, Message, CallbackQuery
from pytgbot.api_types.sendable.reply_markup import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

import brain, db, strings

bot = Bot(BOT_TOKEN)

NEW_USER_CREDIT = 30
REFER_CREDIT = 15
MONTHLY_CREDIT = 15
IS_SERVICE_AVAILABLE = True


def get_updates(offset):
    return bot.get_updates(poll_timeout=10 * 60, error_as_empty=True, offset=offset)


def handle_monthly_rewards():
    users = db.get_all_user()

    for user in users:
        if db.update_credit(user.chat_id, user.credit + MONTHLY_CREDIT):
            try:
                text, parse_mode = strings.get_monthly_reward_message(
                    MONTHLY_CREDIT, user.credit + MONTHLY_CREDIT
                )
                bot.send_message(chat_id=user.chat_id, text=text, parse_mode=parse_mode)
            except:
                pass

    return len(users)


def handle_update(update: Update):
    if update.message is not None:
        message: Message = update.message
        if message.text is not None:
            if message.text.startswith("/"):
                handle_command(message)
            else:
                handle_text_message(message)
        else:
            handle_nontext_message(message)

    elif update.callback_query is not None:
        handle_callback_query(update)


def handle_text_message(message: Message):
    chat_id, msg_id = get_id(message)
    set_typing(chat_id)
    user = db.get_user(chat_id)
    if user is None:
        db.add_user(get_user_from_message(message=message, credit=NEW_USER_CREDIT - 1))
    else:
        if user.credit <= 0:
            text, parse_mode = strings.get_insufficient_credit_reply()
            bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode,
                reply_to_message_id=msg_id,
                reply_markup=get_refer_reply_markup(),
            )
            return
    if IS_SERVICE_AVAILABLE == False:
        bot.send_message(
            chat_id=chat_id,
            text="Service is currently unavailable.I will let you know when it's available.Thanks for your patience.",
        )
        return

    text = brain.get_response(message.text)
    bot.send_message(
        chat_id=chat_id,
        text=(
            text
            if text is not None
            else "Sorry, I can't answer your question right now! Please try later."
        ),
        reply_to_message_id=msg_id,
    )
    if text is not None and user is not None:
        if db.update_credit(chat_id, user.credit - 1) and (user.credit - 1) % 5 == 0:
            text, parse_mode = strings.get_current_balance_reply(user.credit - 1)
            bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode,
                reply_markup=get_earn_more_credits_reply_markup(),
            )


def handle_command(message: Message):
    chat_id, msg_id = get_id(message)
    text = message.text
    user = db.get_user(chat_id)
    if user is None:
        db.add_user(get_user_from_message(message, NEW_USER_CREDIT))

    if text.startswith("/start"):
        referer_id = None
        if user is None:
            arg = text.replace("/start", "").strip()
            referer_id = arg if arg != "" else None
            text, parse_mode = strings.get_new_user_start_command_reply(NEW_USER_CREDIT)
            bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)
        else:
            text, parse_mode = strings.get_old_user_start_command_reply(user.credit)
            bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)

        if referer_id is not None:
            reward_referer(referer_id)

    elif text.startswith("/refer"):
        text, parse_mode = strings.get_referral_link_reply(chat_id)
        bot.send_message(
            text=text,
            chat_id=chat_id,
            parse_mode=parse_mode,
            disable_web_page_preview=True,
        )

    elif text.startswith("/status"):
        text, parse_mode = strings.get_status_command_reply(
            current_credit=user.credit if user is not None else NEW_USER_CREDIT,
            monthly_reward_credit=MONTHLY_CREDIT,
        )
        bot.send_message(
            text=text,
            chat_id=chat_id,
            parse_mode=parse_mode,
            reply_markup=get_refer_reply_markup(should_send_new_message_on_click=True),
        )

    elif text.startswith("/help"):
        text, parse_mode = strings.get_help_command_reply()
        bot.send_message(
            text=text,
            chat_id=chat_id,
            parse_mode=parse_mode,
        )

    else:
        bot.send_message(
            chat_id=chat_id, text="Invalid command!", reply_to_message_id=msg_id
        )


def handle_callback_query(update: Update):
    message = get_message(update)
    chat_id, msg_id = get_id(message)
    query: CallbackQuery = update.callback_query
    user = db.get_user(chat_id)
    if user is None:
        db.add_user(get_user_from_message(message, NEW_USER_CREDIT))

    if query.data.startswith("/status"):
        text, parse_mode = strings.get_status_command_reply(
            current_credit=user.credit if user is not None else NEW_USER_CREDIT,
            monthly_reward_credit=MONTHLY_CREDIT,
        )
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=msg_id,
            parse_mode=parse_mode,
            reply_markup=get_refer_reply_markup(),
        )
    elif query.data.startswith("/refer"):
        text, parse_mode = strings.get_referral_link_reply(chat_id)
        if "new" in query.data:
            bot.answer_callback_query(callback_query_id=query.id)
            bot.send_message(
                text=text,
                chat_id=chat_id,
                parse_mode=parse_mode,
                disable_web_page_preview=True,
            )
        else:
            bot.edit_message_text(
                text=text,
                chat_id=chat_id,
                message_id=msg_id,
                parse_mode=parse_mode,
                disable_web_page_preview=True,
            )


def reward_referer(referer_id):
    referer = db.get_user(referer_id)
    if referer is not None and db.update_credit(
        referer_id, referer.credit + REFER_CREDIT
    ):
        text, parse_mode = strings.get_referer_rewarded_reply(
            REFER_CREDIT, referer.credit + REFER_CREDIT
        )
        bot.send_message(
            chat_id=referer_id,
            text=text,
            parse_mode=parse_mode,
        )


def get_user_from_message(message: Message, credit: NEW_USER_CREDIT) -> User:
    chat_id, _ = get_id(message)
    name = get_user_name(message)
    username = message.from_peer.username
    return User(None, str(chat_id), name, username, credit)


def handle_nontext_message(message: Message):
    chat_id, msg_id = get_id(message)
    bot.send_message(
        chat_id=chat_id,
        text="I can't understand this message format!",
        reply_to_message_id=msg_id,
    )


def get_earn_more_credits_reply_markup():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💰 Earn more credits", callback_data="/status")]
        ]
    )


def get_refer_reply_markup(should_send_new_message_on_click=False):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👥 Refer friends",
                    callback_data="/refer"
                    + (" new" if should_send_new_message_on_click else ""),
                )
            ]
        ]
    )


def get_message(update: Update) -> Message:
    if update.message is not None:
        return update.message
    elif update.callback_query is not None:
        return update.callback_query.message
    return None


def get_id(message: Message):
    if message is None:
        return -1, -1
    return message.chat.id, message.message_id


def get_user_name(message: Message):
    fname = message.from_peer.first_name
    lname = message.from_peer.last_name
    name = fname + (lname if lname is not None else "")
    return name


def set_typing(chat_id):
    return bot.send_chat_action(chat_id=chat_id, action="typing")
