#Common functions that can be resused everywhere.
import Modules.System_messages as Sm
import Modules.User_messages as Um


def token_cost(messages) :
    word_count = sum(len(msg.split()) for msg in messages)
    tokens = word_count * 1.3333
    cost = (0.002 / 1000) * (tokens * 1.333333)
    return [tokens, cost]

def MJ_message() :
    system_message = Sm.Prompt_engineer
    user_message = Um.midjourney_message()
    messages = [{"role": "system", "content": system_message},{"role": "user", "content": user_message}]
    return [messages, user_message, system_message]