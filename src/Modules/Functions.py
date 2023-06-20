#Common functions that can be resused everywhere.
import src.Modules.System_messages as Sm
import src.Modules.User_messages as Um


def token_cost(messages, model):
    word_count = sum(len(msg.split()) for msg in str(messages))
    tokens = word_count * 1.3333
    if model == "gpt-3.5-turbo":
        cost = (0.002 / 1000) * (tokens * 1.333333)
    elif model == "gpt-4":
        cost = (0.045 / 1000) * (tokens * 1.333333)
    return [tokens, cost]

def MJ_message():
    system_message = Sm.PROMPT_ENGINEER
    user_message = Um.midjourney_message()
    messages = [{"role": "system", "content": system_message},{"role": "user", "content": user_message}]
    return [messages, user_message, system_message]

def SEO_message(user_message):
    system_message = Sm.SEO_SPECIALIST
    messages = [{"role": "system", "content": system_message},{"role": "user", "content": user_message}]
    return [messages, user_message, system_message]