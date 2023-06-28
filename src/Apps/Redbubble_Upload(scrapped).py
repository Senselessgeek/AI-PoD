from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from src.Modules.keys import redbubble_user as username
from src.Modules.keys import redbubble_pass as password
from src.Databases.MJDB import get_database
from src.Modules.Functions import oid_from_filename as oid
from src.Modules.Functions import make_title
from src.Modules.Functions import listToString
import os
import time
import glob
import random

#connect to MJ-DB
dbname = get_database()
collection_name = dbname["MJ_prompts"]

print(os.getcwd())
images_dir = os.path.join("..", "static", "images", "Redbubble_Upload")
all_images = set(image for image in os.listdir(images_dir)
                 if os.path.isfile(os.path.join(images_dir, image)))
print(images_dir)
files = list(all_images)
#print(files)
design_upload = list(all_images)
main_page_url = 'https://www.redbubble.com/auth/login'
base_design_url = 'https://www.redbubble.com/portfolio/images/145963638-abstract-foreboding-paint-dripping/duplicate'

for i in design_upload:
    # Take the design name and removing the extension
    img_name = i.split('.')[0]
    url_img = os.path.join(images_dir, i)

    mongo_id = oid(i)
    item = collection_name.find({"_id": mongo_id})

    for item in item:
        tags = item["tags"]
        print(item)


    title = listToString(make_title(i))
    tags = tags.replace('"','').replace('[', '').replace(']', '')
    desc = title

    print(i)
    print(f'title: {title}')
    print(f'tags: {tags}')
    print(f'description: {desc}')

