from flask import Flask, render_template, request, redirect, url_for
from src.Modules.Functions import oid_from_filename as oid
from src.Modules.Functions import make_title
from src.Modules.Functions import listToString
from src.Databases.MJDB import get_database
import random
import os
import shutil
import subprocess
app = Flask(__name__)

## Definitions
# Get the directory of the current file
dir_path = os.path.dirname(os.path.realpath(__file__))

## Set folder structure for sorter app
# Define the folder names
bucket_names = ['Redbubble_Edit', 'Redbubble_Upload', 'StockPhoto_Edit', 'StockPhoto_Upload', 'Uncategorized']
# Define base folder
base_move_folder = 'static/images'
# Create folders if they don't exist
for folder in bucket_names:
    os.makedirs(os.path.join(base_move_folder, folder), exist_ok=True)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/midjourney_automator')
def midjourney_automator():
    return render_template('midjourney_automator.html')


@app.route('/MJ_to_mongo')
def mj_to_mongo():
    return render_template('MJ_to_mongo.html')


@app.route('/upscaler')
def upscale():
    return render_template('upscaler.html')


@app.route('/movefilehtml')
def movefilehtml():
    return render_template('movefile.html')


@app.route('/run_script', methods=['POST'])
def run_script():
    script_name = request.form.get('script')  # Get the name of the script from the form data
    print(script_name)

    if script_name == 'midjourney_automator':
        try:
            ask_value = request.form['ask']
            result = subprocess.run(['python', 'Apps/midjourney_automator.py', '--ask', ask_value], check=True)
            print('stdout:', result.stdout)
            print('stderr:', result.stderr)
            print('Exit status:', result.returncode)
        except subprocess.CalledProcessError as e:
            print(f"Script failed with exit code: {e.returncode}")
            print(f"Output: {e.output}")

    elif script_name == 'MJ_to_mongo':
        try:
            ask_value = request.form['ask']
            subprocess.run(['python', 'Apps/MJ_to_mongo.py', '--ask', ask_value],check=True)
        except subprocess.CalledProcessError as e:
            print(f"Script failed with exit code: {e.returncode}")
            print(f"Output: {e.output}")

    elif script_name == 'upscaler':
        try:
            chain_path, outpath, bucket = request.form['chain_info'].split(",")
            subprocess.run(['python', 'Apps/upscaler.py', '--chain_path', chain_path, '--outpath', outpath, "--bucket", bucket], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Script failed with exit code: {e.returncode}")
            print(f"Output: {e.output}")

    elif script_name == 'Cleanup_images_folder':
        try:
            result = subprocess.run(['python', 'Apps/Cleanup_images_folder.py'], check=True)
            print('stdout:', result.stdout)
            print('stderr:', result.stderr)
            print('Exit status:', result.returncode)
        except subprocess.CalledProcessError as e:
            print(f"Script failed with exit code: {e.returncode}")
            print(f"Output: {e.output}")

    return redirect('/')

@app.route('/sorter')
def sorter():
    stock_folder = 'static/images'

    # Create a list of all images in the main folder
    all_images = set(image for image in os.listdir(stock_folder)
                     if os.path.isfile(os.path.join(stock_folder, image)))

    # For each bucket, remove the images in that bucket from the main list
    for bucket in bucket_names:
        bucket_path = os.path.join(stock_folder, bucket)
        if os.path.exists(bucket_path):
            bucket_images = set(os.listdir(bucket_path))
            all_images -= bucket_images  # remove bucket images from the main list

    # Convert the set back to a list
    remaining_images = list(all_images)
    image_count = len(remaining_images)

    # Choose a random image from the remaining images
    if remaining_images:
        random_image = random.choice(remaining_images)
    else:
        random_image = None

    stock_folder = 'static/images/StockPhoto_Upload'
    stock_buckets = ["Good", "Bad", "Maybe"]

    # Create a list of all images in the main folder
    stock_images = set(stock_image for stock_image in os.listdir(stock_folder)
                     if os.path.isfile(os.path.join(stock_folder, stock_image)))

    # For each bucket, remove the images in that bucket from the main list
    for stock_bucket in stock_buckets:
        stock_bucket_path = os.path.join(stock_folder, stock_bucket)
        if os.path.exists(stock_bucket_path):
            stock_bucket_images = set(os.listdir(stock_bucket_path))
            stock_images -= stock_bucket_images  # remove bucket images from the main list

    # Convert the set back to a list
    stock_remaining_images = list(stock_images)
    stock_image_count = len(stock_remaining_images)

    # Choose a random image from the remaining images
    if stock_remaining_images:
        stock_random_image = random.choice(stock_remaining_images)
    else:
        stock_random_image = None

    return render_template('sorter.html',
                           random_image=random_image,
                           bucket_names=bucket_names,
                           count=image_count,
                           stock_random_image=stock_random_image,
                           stock_buckets=stock_buckets,
                           stock_image_count=stock_image_count)


@app.route('/movefile', methods=['POST'])
def movefile():
    file = request.files['file']
    bucket = request.form['bucket']

    if file == "no_more_images.png":
        return 'No More Images.'
    elif file and bucket in bucket_names:
        filename = file.filename
        # Set MOVE_FOLDER dynamically
        move_folder = os.path.join(base_move_folder, bucket)
        # Ensure the directory exists
        os.makedirs(move_folder, exist_ok=True)
        file_path = os.path.join(move_folder, filename)
        file.save(file_path)
        subprocess.run(['python', 'Apps/Update_mongo.py', '--bucket', bucket, '--filename', filename], check=True)
        return 'Image moved successfully!'
    return 'Image upload failed!'

@app.route('/Redbubble_Upload')
def Redbubble_Upload():
    dbname = get_database()
    collection_name = dbname["MJ_prompts"]
    images_dir = os.path.join("static", "images", "Redbubble_Upscaled8192x8192")
    all_images = set(image for image in os.listdir(images_dir)
                     if os.path.isfile(os.path.join(images_dir, image)))

    # For each bucket, remove the images in that bucket from the main list
    upload_path = os.path.join(images_dir, "Uploaded")
    if os.path.exists(upload_path):
        bucket_images = set(os.listdir(upload_path))
        all_images -= bucket_images  # remove bucket images from the main list

    # Convert the set back to a list
    remaining_images = list(all_images)

    # Choose a random image from the remaining images
    if remaining_images:
        random_image = random.choice(remaining_images)
        img_name = random_image.split('.')[0]
        url_img = os.path.join(images_dir, random_image)

        mongo_id = oid(random_image)
        item = collection_name.find({"_id": mongo_id})

        for item in item:
            tags = item["tags"]

        print(random_image)
        tags = tags.replace('"', '').replace('[', '').replace(']', '')
        title = listToString(make_title(random_image))
        desc = title

    else:
        random_image = None
        title = None
        tags = None
        desc = None

    return render_template('RedBubble_Upload.html',
                           random_image=random_image,
                           title=title,
                           tags=tags,
                           desc=desc)

@app.route('/movestockphoto', methods=['POST'])
def movestockphoto():
    file = request.files['file']
    bucket = request.form['bucket']
    print(bucket)
    fromfolder = os.path.join("static", "images", "StockPhoto_Upload")
    bucketpath = os.path.join("static", "images", "StockPhoto_Upload", bucket)

    if file == "no_more_images.png":
        return 'No More Images.'
    else:
        filename = file.filename
        # Ensure the directory exists
        os.makedirs(bucket, exist_ok=True)
        frompath = os.path.join(fromfolder, filename)
        topath = os.path.join(bucketpath, filename)
        shutil.move(frompath, topath)
        print("ha")
        return redirect("/sorter")

@app.route('/movefilewithoutmongo', methods=['POST'])
def movefilewithoutmongo():
    filename = request.form['ask']
    fromfolder = os.path.join("static", "images", "Redbubble_Upscaled8192x8192")
    bucket = os.path.join("static", "images", "Redbubble_Uploaded")

    if filename == "no_more_images.png":
        return 'No More Images.'
    else:
        # Ensure the directory exists
        os.makedirs(bucket, exist_ok=True)
        frompath = os.path.join(fromfolder, filename)
        topath = os.path.join(bucket, filename)
        shutil.move(frompath, topath)
        return redirect("/Redbubble_Upload")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
