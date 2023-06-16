from subprocess import *
import os
import json
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--chain_path')
parser.add_argument('--outpath')
parser.add_argument('--bucket')
args = parser.parse_args()
chain_path = os.path.join(os.getcwd(),"static", "8192.chn")
outpath = args.outpath
bucket = args.bucket
chainner_path = "C:\\Users\\andmarst\\AppData\\Local\\chainner\\app-0.18.9"


def run_chainner(chain_path, chainner_path, overrides=None):
    command = [os.path.join(chainner_path, "chainner.exe"), "run", chain_path]


    if overrides is not None:
        # Create a temporary file for the input overrides
        with open('temp.json', 'w') as f:
            json.dump({'inputs': overrides}, f)

        command.append("--override")
        command.append('temp.json')

    print(command)
    result = run(command, capture_output=True)

    # Remove the temporary file if it was created
    if overrides is not None:
        os.remove('temp.json')

    if result.returncode == 0:
        print("Chain ran successfully.")
    else:
        print(f"Chain failed with exit code {result.returncode}.")
        print(f"Output: {result.stdout.decode('utf-8')}")

# Example usage
#     run_chainner("static/8192.chn", overrides={"input_id": "value"})
if __name__ == "__main__":
    print(os.getcwd())
    images_dir = os.path.join("static", "images", bucket)
    all_images = set(image for image in os.listdir(images_dir)
                     if os.path.isfile(os.path.join(images_dir, image)))
    print(images_dir)
    files = list(all_images)
    print(files)

    for filename in files:
        image_path = os.path.join(os.getcwd(),images_dir, filename)
        overrides = {
            "#440d1a81-acc6-47a4-9aaf-83bf778dd3c7:0": image_path,
        }
        print(overrides)
        run_chainner(chain_path, chainner_path, overrides)