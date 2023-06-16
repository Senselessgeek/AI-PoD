from playwright.sync_api import sync_playwright
import src.Modules.keys as keys
from src.Databases.MJDB import get_database
import os
import openai
import random
import re
import requests
import time
import uuid
print("from flask")
# Set OpenAI API key.
openai.api_key = keys.AIPoDkey

#connect to MJ-DB
dbname = get_database()
collection_name = dbname["MJ_prompts"]

# Constants.
BOT_COMMAND = "/imagine"
CHANNEL_URL = "https://discord.com/channels/1104854992545923264/1104854992545923267"

# Login to Discord
def open_discord_channel(page):
    # Go to appropriate channel.
    page.goto(f"{CHANNEL_URL}")
    time.sleep(random.randint(1, 5))
    page.wait_for_load_state("networkidle")  # This waits for the "networkidle"
    print("Opened appropriate channel.")
    return page

# Click all the buttons
def select_upscale_option(page, option_text):
    # Click the last button on the page that contains the option text.
    page.locator(f"button:has-text('{option_text}')").locator("nth=-1").click()
    print(f"Clicked {option_text} upscale option.")


# Save the images
def download_upscaled_images(page, name):
    # Wait for all four images to complete rendering by checking the contents of the last 4 messages to see if it
    # contains the phrase 'Make Variations', and 'Web'.
    name = name
    print("inside download_upscale_options", name)
    #Create a list of all the messages
    messages = page.query_selector_all(".messageListItem-ZZ7v6g")
    last_four_messages = messages[-4:]
    # Get the inner text of the last four messages by evaluating the innerText property of the node.
    for message in last_four_messages:
        message = message.evaluate_handle('(node) => node.innerText')
        message = str(message)
    # Check to see if string contains the 'Make Variation' and 'Web'.
    if 'Make Variations' and 'Web' in message:
        try:
            print('Downloading upscaled images.')
            try:
                # Download last 4 images.
                last_image = page.query_selector_all('.originalLink-Azwuo9')[-1]
                second_last_image = page.query_selector_all('.originalLink-Azwuo9')[-2]
                third_last_image = page.query_selector_all('.originalLink-Azwuo9')[-3]
                fourth_last_image = page.query_selector_all('.originalLink-Azwuo9')[-4]

                # Loop and download all 4 images with the same name as the prompt, along with last_image, second_last_image, etc.
                for image in [last_image, second_last_image, third_last_image, fourth_last_image]:
                    src = image.get_attribute('href')
                    url = src
                    # Remove all special characters from the response using regex.
                    response = re.sub(r'[^a-zA-Z0-9\s]', '', str(name))
                    # Replace all commas and spaces with underscores.
                    response = response.replace(',', '_').replace(' ', '_')

                    # If having issue saving the file geting "FileNotFoundError: [Errno 2] No such file or directory:"
                    # see this article on Windows Long File Paths.
                    # https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry
                    response = response[:200]
                    r = requests.get(url, stream=True)

                    # Generate a unique filename using a UUID
                    filename = f"{response}_{uuid.uuid1()}.png"
                    curpath = os.path.abspath(os.curdir)
                    filepath = os.path.join(curpath, "../static/images", filename)

                    with open(filepath, "wb") as outfile:
                        outfile.write(r.content)
                        print(f"Image saved successfully: {filename}")
            except IOError as e:
                    print(f"Error saving image: {e}")
        except Exception as e:
            print(e)
        print(f"File path: {filepath}")
    else:
        # Call the function again.
        download_upscaled_images(page, name)


# Function to get the last message.
def get_last_message(page):
    # Obtain the list of all messages.
    # Create a list of all the messages
    messages = page.query_selector_all(".messageListItem-ZZ7v6g")
    # Select the last message.
    last_message = messages[-1]
    # Get the text of the last message.
    last_message = last_message.evaluate_handle('(node) => node.innerText')
    last_message = str(last_message)
    return last_message


# Function to wait for page to fully load and select all upscale options.
def wait_and_select_upscale_options(page, prompt_text, name):
    prompt_text = prompt_text.lower()
    name = name
    print("inside wait_and_select_upscale_options", name)
    try:
        last_message = get_last_message(page)
        # Check to see if string contains the 'U1'.
        if 'U1' in last_message:
            print("Found upscale options.")
            print("Attempting to upscale all generated images.")
            try:
                # Select the 'U1' upscale option
                select_upscale_option(page, 'U1')
                time.sleep(random.randint(3, 5))
                # Select the 'U2' upscale option
                select_upscale_option(page, 'U2')
                time.sleep(random.randint(3, 5))
                # Select the 'U3' upscale option
                select_upscale_option(page, 'U3')
                time.sleep(random.randint(3, 5))
                # Select the 'U4' upscale option
                select_upscale_option(page, 'U4')
                time.sleep(random.randint(3, 5))
            except Exception as e:
                print("An error occured while selecting upscale options:", e)
            download_upscaled_images(page, name)
        else:
            print("Photos not fully loaded. Waiting 10 seconds.")
            time.sleep(10)
            wait_and_select_upscale_options(page, prompt_text, name)
    except Exception as e:
        print("An error occurred while finding the last message:", e)


# Function to generate prompt and sumbit command.
def generate_prompt_and_submit_command(page, prompt, name):
    try:
        # Generate prompt.
        name = name
        print("inside generate prompt and submit command", name)
        prompt_text = prompt
        time.sleep(random.randint(2, 5))
        pill_value = page.locator(
            'xpath=//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div/main/form/div/div[2]/div/div[2]/div/div/div/span[2]/span[2]')
        pill_value.fill(prompt_text)
        # Submit prompt.
        time.sleep(random.randint(2, 5))
        # Press the Enter key.
        page.keyboard.press("Enter")
        print(f'Successfully submitted prompt: {prompt_text}')
        wait_and_select_upscale_options(page, prompt_text, name)
    except Exception as e:
        print("An error occurred while submitting the prompt:", e)


# Start calling Midjourney
def bot_command(page, command):
    try:
        print("Clicking on chat bar.")
        chat_bar = page.locator(
            'xpath=//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div[2]/main/form/div/div[1]/div/div[3]/div/div[2]/div')
        time.sleep(random.randint(2, 5))
        print("Typing in bot command")
        chat_bar.fill(command)
        time.sleep(random.randint(2, 5))
        print("Selecting the prompt option in the suggestions menu")
        # Select the first option in the pop-up menu.
        prompt_option = page.locator(
            'xpath=/html/body/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div[2]/main/form/div/div[2]/div/div/div[2]/div[1]/div/div/div')
        time.sleep(random.randint(2, 5))
        # Click on the prompt option.
        prompt_option.click()
        print("Grab random sample from database.")
        for sample in collection_name.aggregate([{"$sample": {"size": 1}}]):
            prompt = sample["prompt"]
            material = sample["material"]
            shape = sample["shape"]
            colors = sample["colors"]
            medium = sample["medium"]
            name = [material, shape, colors, medium]
            print("inside bot command", prompt)
            print("inside bot command", name)
        generate_prompt_and_submit_command(page, prompt, name)
    except Exception as e:
        print("An error occurred while entering in the prompt:", e)


# Main function to log in to Discord and run the bot.
if __name__ == "__main__":
    with sync_playwright() as p:
        print("starting from with sync")
        browser = p.chromium.launch(headless=False)
        # Create a new incognito browser context.
        page = browser.new_page()
        # Go to Discord login page.
        page.goto("https://www.discord.com/login")
        # # Open credentials file and read in email and password.
        email = keys.demail
        password = keys.dpass
        # # Fill in email and password fields.
        print("Entering email")
        page.fill("input[name='email']", email)
        time.sleep(random.randint(2, 5))
        print("Entering password")
        page.fill("input[name='password']", password)
        time.sleep(random.randint(2, 5))
        # # Click login button.
        print("Logging into Discord, have your 2fa ready to enter.")
        page.click("button[type='submit']")
        time.sleep(random.randint(5, 10))
        # # Wait for page URL to change for 15 seconds.
        page.wait_for_url("https://discord.com/channels/@me", timeout=15000)
        print("Successfully logged into Discord.")
        time.sleep(random.randint(2, 5))

        # Run the bot for 10 iterations.
        for i in range(10):
            # Open Discord and go to appropriate channel.
            open_discord_channel(page)
            page.goto(f"{CHANNEL_URL}")
            time.sleep(random.randint(2, 5))
            page.wait_for_load_state("networkidle")  # This waits for the "networkidle"
            print("Opened appropriate channel.")
            print("Entering in the specified bot command.")
            bot_command(page, BOT_COMMAND)
            # Print the number of iterations completed.
            print(f"Iteration {i + 1} completed.")






