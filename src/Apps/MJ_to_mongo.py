import re
import time
import os
from colorama import Fore
from colorama import Style
from src.Modules.PromptBuilder import call_midjourney_gpt
from src.Modules.PromptBuilder import call_seo_gpt
from src.Databases.MJDB import get_database
from src.Modules.keys import AIPODKEY as APIKEY
from src.Modules.Functions import token_cost as tc
import argparse

curfile = os.path.basename(__file__)

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--ask', type=int, help='Number of times to run')
args = parser.parse_args()
ask = args.ask

#ask = 1

# connect to MJ-DB
dbname = get_database()
collection_name = dbname["MJ_prompts"]



def the_loop():
    # zeroize counts
    run = 0
    retry = 0
    mj_total_cost = 0
    tag_total_cost = 0
    errors = []
    while run < int(ask):
        print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} run : {Fore.YELLOW} {run} {Style.RESET_ALL}")
        try:
            # call gpt for two prompts
            gen_mj_prompts = call_midjourney_gpt(APIKEY)
            # set the returned values to variables for calling later.
            request = gen_mj_prompts[0][1]["content"]
            chat1 = gen_mj_prompts[1]
            chat2 = gen_mj_prompts[2]
            mj_message = []
            tag_message = []
            mj_message.append(request + chat1 + chat2)

            retry2 = 0
            while retry2 < 3:
                print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} tag retries: {Fore.YELLOW} {retry2} {Style.RESET_ALL}")
                print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} top of SEO while: ", chat1)
                gen_tags = call_seo_gpt(APIKEY, chat1)
                print(type(gen_tags[1]))
                if gen_tags[1].startswith('["') or gen_tags[1].startswith("['"):
                    print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} if: {Fore.BLUE}{gen_tags[1]}{Style.RESET_ALL}")
                    print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} {Fore.GREEN}correct format, moving on.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} else: {Fore.BLUE}{gen_tags[1]}{Style.RESET_ALL}")
                    retry2 += 1
                    print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} {Fore.RED}{Style.BRIGHT}incorrect format, recalling function{Style.RESET_ALL}")

            seo_tags = gen_tags[1]
            print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} tags: {Fore.BLUE} {seo_tags} {Style.RESET_ALL}")

            tag_message.append(seo_tags)

            # calculate CHATGPT API cost
            mj_tokens, mj_cost = tc([mj_message], "gpt-3.5-turbo")
            mj_total_cost = mj_total_cost + mj_cost

            tag_tokens, tag_cost = tc([tag_message], "gpt-3.5-turbo")
            tag_total_cost = tag_total_cost + tag_cost

            print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} MJ Cost of this iteration: {Fore.YELLOW} {mj_cost} {Style.RESET_ALL}")
            print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} Tags cost this iteration: {Fore.YELLOW} {tag_cost} {Style.RESET_ALL}")
            print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} Cost of whole session: {Fore.YELLOW} {mj_total_cost + tag_total_cost} {Style.RESET_ALL}")

            # split the generated user message for adding into db
            print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} request: {request}")
            split_request = {}

            # Use regular expressions to extract key-value pairs
            pattern = r"(\w+):\s\[(.*?)\]"
            matches = re.findall(pattern, request)

            # Iterate over the matches and populate the split_request dictionary
            for match in matches:
                key = match[0]
                value = match[1].split(', ')
                split_request[key] = value

            print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} split: {split_request}")

            # create our db items for upload
            item1 = {
                "material": split_request["material"],
                "shape": split_request["shapes"],
                "colors": split_request["colors"],
                "medium": split_request["medium"],
                "prompt": chat1,
                "tags": seo_tags
            }
            #print("item1: ", item1)
            item2 = {
                "material": split_request["material"],
                "shape": split_request["shapes"],
                "colors": split_request["colors"],
                "medium": split_request["medium"],
                "prompt": chat2,
                "tags": seo_tags
            }
            #print("item2 :", item2)
            collection_name.insert_many([item1, item2])

            # increment the run counter.
            run += 1
            time.sleep(4)
        except Exception as e:
            if 'That model is currently overloaded with other requests.' in str(e):
                retry += 1
                errors.append(str(e))
                print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} {Fore.RED}Rate limit reached.  Retrying in 40 seconds. Retry count: {retry}{Style.RESET_ALL}")
                time.sleep(40)
            elif 'The server had an error while processing your request.' in str(e):
                retry += 1
                errors.append(str(e))
                print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} {Fore.RED}There was an error processing. Retrying in 40 seconds. Retry count: {retry}{Style.RESET_ALL}")
                time.sleep(40)
            elif 'The server is overloaded or not ready yet.' in str(e):
                retry += 1
                errors.append(str(e))
                print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} {Fore.RED}Server is overloaded or not ready yet. Retrying in 40 seconds. Retry count: {retry}{Style.RESET_ALL}")
                time.sleep(40)
            elif 'HTTP code 502 from API' in str(e):
                retry += 1
                errors.append(str(e))
                print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} {Fore.RED}Server is overloaded or not ready yet. Retrying in 40 seconds. Retry count: {retry}{Style.RESET_ALL}")
                time.sleep(40)
            else:
                print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} {Fore.MAGENTA}An undocumented error occurred: {str(e)}{Style.RESET_ALL}")
                errors.append(str(e))
                break
    print(f"{Fore.LIGHTCYAN_EX}{curfile}{Style.RESET_ALL} Last 5 errors:  = ", errors[-5:])
if __name__ == "__main__":
    the_loop()