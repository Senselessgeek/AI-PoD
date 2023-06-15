from flask import Flask, render_template, request, redirect, url_for
import os
import subprocess
app = Flask(__name__)

# Get the directory of the current file
dir_path = os.path.dirname(os.path.realpath(__file__))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/midjourney_automator')
def midjourney_automator():
    return render_template('midjourney_automator.html')


@app.route('/MJ_to_mongo')
def mj_to_mongo():
    return render_template('MJ_to_mongo.html')


@app.route('/run_script', methods=['POST'])
def run_script():
    script_name = request.form.get('script')  # Get the name of the script from the form data
    print(script_name)

    if script_name == 'midjourney_automator':
        try:
            subprocess.run(['python', 'Apps/midjourney_automator.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Script failed with exit code: {e.returncode}")
            print(f"Output: {e.output}")

    elif script_name == 'MJ_to_mongo':
        try:
            subprocess.run(['python', 'Apps/MJ_to_mongo.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Script failed with exit code: {e.returncode}")
            print(f"Output: {e.output}")

    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
