from creds import BOT_USERNAME


def get_new_user_start_command_reply(new_user_credit):
    return f"""👋 Hello there!

🤖 I am your personal AI assistant, ready to help you with any questions you may have.

🎁 *You've received {new_user_credit} credits for free!* Enjoy the perks! 😊

🚀 To get help, use the command /help.""", "markdown"


def get_old_user_start_command_reply(credit):
    return f"""🥳 Welcome back, dear user!

🤖 I am your personal AI assistant, ready to help you with any questions you may have.

💰 *You currently have {credit} credits to use.*

🚀 To get help, use the command /help.""", "markdown"


def get_help_command_reply():
    return """👋 Hello there! 

📝 Simply send me any question you have, and I'll answer promptly.

💡 Just a quick heads up: *For every question you ask, one credit will be deducted from your balance.* 💰

🧠 Please keep in mind that I won't retain any context from previous messages, so each inquiry should be standalone.

💳 To check your available credits and learn how to earn more, use the command /status.""", "markdown"


def get_referer_rewarded_reply(reward_credit, current_credit):
    return f"""🎉 Congratulations!

🤝 A new user has joined using your referral link.

🎁 *You have been rewarded with {reward_credit} credits*, bringing your current credit balance to {current_credit}.

🌟 Keep sharing your referral link and earning more credits! 😊
""", "markdown"


def get_referral_link_reply(chat_id):
    return f"""🎁 Sharing is rewarding!

💬 Invite your friends using this referral link and get extra credits: 
https://t.me/{BOT_USERNAME}?start={chat_id}

🌟 The more friends you invite, the more credits you'll earn! Start sharing now and enjoy the benefits! 😃""", None


def get_status_command_reply(current_credit, monthly_reward_credit):
    return f"""
💰 Your remaining credit balance is `{current_credit}`.

👥 To earn more credits, refer your friends using your unique referral link. You will be rewarded every time someone joins through your link.

🎁 Additionally, you'll receive `{monthly_reward_credit}` *free credits* every month!

🚀 Keep sharing and enjoy the perks.""", "markdown"


def get_current_balance_reply(credit):
    return f"💰 Your remaining credit balance is `{credit}`.", "markdown"

def get_insufficient_credit_reply():
    return '''🚫 Oh no! Your current balance is insufficient to get an answer right now. 😔

💰 But don't worry! You can earn more credits by referring your friends to use this bot. 👥

📈 To learn more about your credit status and ways to earn more, use the command /status.''', None


def get_monthly_reward_message(monthly_credit, current_credit):
    return f"""🎉 Congratulations!

🎁 *You have got {monthly_credit} monthly credits for free*. Your current credit balance is {current_credit}.

🌟 Enjoy! 😊
""", "markdown"