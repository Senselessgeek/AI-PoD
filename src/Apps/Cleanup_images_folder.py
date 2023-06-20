import os

print(os.getcwd())
def Cleanup_images_folder():
    worked_images_dir = os.path.join("static", "images")
    Redbubble_path = os.path.join("static", "images", "Redbubble")
    Stockphoto_path = os.path.join("static", "images", "StockPhoto")
    worked_images = set(image for image in os.listdir(worked_images_dir)
                     if os.path.isfile(os.path.join(worked_images_dir, image)))

    RB_images = set(image for image in os.listdir(Redbubble_path)
                     if os.path.isfile(os.path.join(Redbubble_path, image)))

    SP_images = set(image for image in os.listdir(Stockphoto_path)
                     if os.path.isfile(os.path.join(Stockphoto_path, image)))

    files = list(worked_images)
    RBfiles = list(RB_images)
    SPfiles = list(SP_images)

    for file in files:
        if file in files and RBfiles or SPfiles:
            if file == "no_more_images.png":
                print("not moving", file)
            else:
                try:
                    os.remove(os.path.join(worked_images_dir, file))
                except Exception as e:
                    print(e)
                print(file, "removed")

if __name__ == "__main__":
    Cleanup_images_folder()