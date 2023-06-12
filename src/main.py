from Modules.MjPromptBuilder import call_gpt

a = 0
b = input("How many times would you like to run: ")
prompts = []
while a < int(b):
    gen_prompts = call_gpt()

    user = gen_prompts[0]
    chat1 = gen_prompts[1]
    chat2 = gen_prompts[2]


    prompts.append(chat1)
    prompts.append(chat2)
    a += 1

    print()
    print()

    # print to console
    print(f'Request: {user["content"]}')
    print()

    # print to console
    print(f'ChatGPT1: {chat1}')
    print()
    print()
    print(f'ChatGPT2: {chat2}')
    print()
    print()
    print(prompts)