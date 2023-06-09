import openai
import src.Modules.Functions as F



# Start a loop to feed in random material, shapes, colors, and mediums as prompts.
def call_midjourney_gpt(APIKEY):
    openai.api_key = APIKEY
    messages = F.MJ_message()[0]

    #call openai to create a response4
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        n = 2,
        max_tokens = 125
    )

    #set openai response as variable
    chat_response1 = completion.choices[0].message.content
    chat_response2 = completion.choices[1].message.content

    return [messages, chat_response1, chat_response2]

def call_seo_gpt(APIKEY, user_message):
    user_message = user_message
    openai.api_key = APIKEY
    messages = F.SEO_message(str("here is my text: " + user_message))[0]

    #call openai to create a response4
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        n = 2,
        max_tokens = 200
    )

    #set openai response as variable

    chat_response1 = completion.choices[0].message.content
    return [messages, chat_response1]
