import re
import time
from src.Modules.PromptBuilder import call_gpt
from src.Databases.MJDB import get_database
from src.Modules.keys import StickerMakerAPIKey as APIKEY
from src.Modules.Functions import token_cost as tc
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--ask', type=int, help='Number of times to run')
args = parser.parse_args()
ask = args.ask

# connect to MJ-DB
dbname = get_database()
collection_name = dbname["MJ_prompts"]

# zeroize counts
run = 0
retry = 0
total_cost = 0

# The Loop
while run < int(ask) and retry < 10:
    try:
        # call gpt for two prompts
        gen_prompts = call_gpt(APIKEY)

        # set the returned values to variables for calling later.
        request = gen_prompts[0][1]["content"]
        chat1 = gen_prompts[1]
        chat2 = gen_prompts[2]
        message = request + chat1 + chat2

        # calculate CHATGPT API cost
        tokens, cost = tc([message])
        total_cost = total_cost + cost

        # print(f'This run cost: {cost}')
        # print(f'cumulative cost is: {total_cost}')

        print(f'Cost of this iteration: {cost}')
        print(f'Cost of whole session: {total_cost}')

        # split the generated user message for adding into db
        print(request)
        split_request = {}

        # Use regular expressions to extract key-value pairs
        pattern = r"(\w+):\s\[(.*?)\]"
        matches = re.findall(pattern, request)

        # Iterate over the matches and populate the split_request dictionary
        for match in matches:
            key = match[0]
            value = match[1].split(', ')
            split_request[key] = value

        print("split", split_request)

        # create our db items for upload
        item1 = {
            "material": split_request["material"],
            "shape": split_request["shapes"],
            "colors": split_request["colors"],
            "medium": split_request["medium"],
            "prompt": chat1
        }
        print("item", item1)
        item2 = {
            "material": split_request["material"],
            "shape": split_request["shapes"],
            "colors": split_request["colors"],
            "medium": split_request["medium"],
            "prompt": chat2
        }
        print("item", item2)
        collection_name.insert_many([item1, item2])

        # increment the run counter.
        run += 1
    except Exception as e:
        if 'RateLimitError' in str(e):
            retry += 1
            print(f'Rate limit reached.  Retrying in 5 seconds. Retry count: {retry}')
            time.sleep(5)
        else:
            print("An error occurred", str(e))
            break
