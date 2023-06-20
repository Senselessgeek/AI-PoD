from playwright.sync_api import sync_playwright
from src.Modules.keys import redbubble_user as username
from src.Modules.keys import redbubble_pass as password
import os
import time
import glob
import random


print(os.getcwd())
images_dir = os.path.join("..", "static", "images", "Redbubble")
all_images = set(image for image in os.listdir(images_dir)
                 if os.path.isfile(os.path.join(images_dir, image)))
print(images_dir)
files = list(all_images)
print(files)
design_upload = list(all_images)
main_page_url = 'https://www.redbubble.com/auth/login'
base_design_url = 'https://www.redbubble.com/portfolio/images/145963638-abstract-foreboding-paint-dripping/duplicate'


with sync_playwright() as p:
    '''
    print("starting from with sync")
    browser = p.chromium.launch(headless=False)
    # Create a new incognito browser context.
    page = browser.new_page()
    # Go to Discord login page.
    page.goto(main_page_url)
    print("Entering email")
    page.fill('id=ReduxFormInput1', username)
    time.sleep(random.randint(2, 5))
    print("Entering password")
    page.click('id=ReduxFormInput2')
    page.fill('id=ReduxFormInput2', password)
    time.sleep(random.randint(2,5))
    page.keyboard.press('Enter')
    time.sleep(random.randint(5, 10))
    print("pausing to enter captchas")
    page.pause()
    '''

    for i in design_upload:
        # Take the design name and removing the extension
        img_name = i.split('.')[0]
        print(i)

        url_img = os.path.join(images_dir, i)
        print(url_img)
        title = '{Your design title and the img_name}'
        print(title)
        tags = '{Your intended Tags}'
        print(tags)
        desc = '{Your design description and the img_name}'
        print(desc)


        page.goto(base_design_url)
        time.sleep(random.randint(2,5))

        '''
        # Filling the title form
        element = driver.find_element_by_id('work_title_en')
        element.clear()
        element.send_keys(title)
        '''

        '''
        # Filling the tag form
        element = driver.find_element_by_id('work_tag_field_en')
        element.clear()
        element.send_keys(tags)
        '''

        '''
        # Filling the description form
        element = driver.find_element_by_id('work_description_en')
        element.clear()
        element.send_keys(desc)
        '''

        '''
        # Upload the image design
        driver.find_element_by_id('select-image single').send_keys(url_img)
        '''

        '''
        # Click the Declaration form
        driver.find_element_by_id('rightsDeclaration').click()
        '''

        '''
        # Let the design upload process finished
        time.sleep(30)
        '''

        '''
        # Submit the work
        driver.find_element_by_id('submit-work').click()
        '''

        '''
        # Let the whole process finish before move on to the next design
        time.sleep(30)
        '''