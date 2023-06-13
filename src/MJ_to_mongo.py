import re
import time
from Modules.PromptBuilder import call_gpt
from src.Databases.MJDB import get_database
from Modules.keys import StickerMakerAPIKey
from Modules.Functions import token_cost as tc

#connect to MJ-DB
dbname = get_database()
collection_name = dbname["MJ_prompts"]

#zeroize counts and ask for number of iterations
run = 0
retry = 0
total_cost = 0
ask = input("How many times would you like to run: ")

#The Loop
while run < int(ask) and retry < 10:
    try:
        #call gpt for two prompts
        gen_prompts = call_gpt(StickerMakerAPIKey)

        #set the returned values to variables for calling later.
        request = gen_prompts[0][1]["content"]
        chat1 = gen_prompts[1]
        chat2 = gen_prompts[2]
        message = request + chat1 + chat2

        #calculate CHATGPT API cost
        tokens, cost = tc([message])
        total_cost = total_cost + cost

        # print(f'This run cost: {cost}')
        # print(f'cumulative cost is: {total_cost}')

        print(f'Cost of this iteration: {cost}')
        print(f'Cost of whole session: {total_cost}')

        #split the generated user message for adding into db
        split_request = re.split(': |,', request)

        #create our db items for upload
        item1 = {
            "material" : split_request[1],
            "shape" : split_request[3],
            "colors" : split_request[5],
            "medium" : split_request[7],
            "prompt" : chat1
        }

        item2 = {
            "material": split_request[1],
            "shape": split_request[3],
            "colors": split_request[5],
            "medium": split_request[7],
            "prompt": chat2
        }

        collection_name.insert_many([item1,item2])

        #increment the run counter.
        run += 1
    except OpenAIApiError as e:
        if 'RateLimitError' in str(e):
            retry += 1
            print(f'Rate limit reached.  Retrying in 5 seconds. Retry count: {retry}')
            time.sleep(5)
        else:
            print("An error occurred", str(e))
            break