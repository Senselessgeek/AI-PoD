import openai
from lib.config import StickerMakerAPIKey

# Set up your OpenAI API key
openai.api_key = StickerMakerAPIKey

system_message = '''
I want you to act as a prompt engineer. You will help me write prompts for an ai art generator called Midjourney.

I will provide you with short content ideas and your job is to elaborate these into full, explicit, coherent prompts.

Prompts involve describing the content and style of images in concise accurate language. It is useful to be explicit and use references to popular culture, artists and mediums. Your focus needs to be on nouns and adjectives. I will give you some example prompts for your reference. Please define the exact camera that should be used

Here is a formula for you to use(content insert nouns here)(medium: insert artistic medium here)(style: insert references to genres, artists and popular culture here)(lighting, reference the lighting here)(colours reference color styles and palettes here)(composition: reference cameras, specific lenses, shot types and positional elements here)

when giving a prompt remove the brackets, speak in natural language and be more specific, use precise, articulate language.

always output me two full prompt options that are different

Example prompt:

Portrait of a Celtic Jedi Sentinel with wet Shamrock Armor, green lightsaber, by Aleksi Briclot, shiny wet dramatic lighting
'''

messages = [
    {"role": "system", "content": system_message}
]

total_session = 0

while True:
    content = input("User: ")
    messages.append({"role": "user", "content": content})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    chat_response = completion.choices[0].message.content
    print(f'ChatGPT: {chat_response}')
    messages.append({"role": "assistant", "content": chat_response})
    word_count = sum(len(msg['content'].split()) for msg in messages)
    total_session = total_session + word_count
    print(f'Tokens: {total_session * 1.333333}')
    print(f'Total Session Cost: ${(0.002 / 1000) * (total_session * 1.333333)}')
