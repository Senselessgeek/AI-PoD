from flask import Flask, render_template, request, redirect, url_for
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
bucket_names = ['Redbubble', 'StockPhoto', 'Uncategorized']
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


@app.route('/upload_to_pod')
def upload_to_pod():
    return render_template('upload_to_pod.html')


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
    images_folder = 'static/images'

    # Create a list of all images in the main folder
    all_images = set(image for image in os.listdir(images_folder)
                     if os.path.isfile(os.path.join(images_folder, image)))

    # For each bucket, remove the images in that bucket from the main list
    for bucket in bucket_names:
        bucket_path = os.path.join(images_folder, bucket)
        if os.path.exists(bucket_path):
            bucket_images = set(os.listdir(bucket_path))
            all_images -= bucket_images  # remove bucket images from the main list

    # Convert the set back to a list
    remaining_images = list(all_images)

    # Choose a random image from the remaining images
    if remaining_images:
        random_image = random.choice(remaining_images)
    else:
        random_image = None

    return render_template('sorter.html',
                           random_image=random_image,
                           bucket_names=bucket_names)


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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
