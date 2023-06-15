#Common functions that can be resused everywhere.
import src.Modules.System_messages as Sm
import src.Modules.User_messages as Um


def token_cost(messages):
    word_count = sum(len(msg.split()) for msg in messages)
    tokens = word_count * 1.3333
    cost = (0.002 / 1000) * (tokens * 1.333333)
    return [tokens, cost]

def MJ_message():
    system_message = Sm.PROMPT_ENGINEER
    user_message = Um.midjourney_message()
    messages = [{"role": "system", "content": system_message},{"role": "user", "content": user_message}]
    return [messages, user_message, system_message]