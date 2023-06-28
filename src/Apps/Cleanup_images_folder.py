import os

print(os.getcwd())
def Cleanup_images_folder():
    worked_images_dir = os.path.join("static", "images")
    Redbubble_Upload_path = os.path.join("static", "images", "Redbubble_Upload")
    Stockphoto_Upload_path = os.path.join("static", "images", "StockPhoto_Upload")
    Redbubble_Edit_path = os.path.join("static", "images", "Redbubble_Edit")
    Stockphoto_Edit_path = os.path.join("static", "images", "StockPhoto_Edit")

    worked_images = set(image for image in os.listdir(worked_images_dir)
                     if os.path.isfile(os.path.join(worked_images_dir, image)))

    RBE_images = set(image for image in os.listdir(Redbubble_Edit_path)
                     if os.path.isfile(os.path.join(Redbubble_Edit_path, image)))

    SPE_images = set(image for image in os.listdir(Stockphoto_Edit_path)
                     if os.path.isfile(os.path.join(Stockphoto_Edit_path, image)))

    RBU_images = set(image for image in os.listdir(Redbubble_Upload_path)
                     if os.path.isfile(os.path.join(Redbubble_Upload_path, image)))

    SPU_images = set(image for image in os.listdir(Stockphoto_Upload_path)
                     if os.path.isfile(os.path.join(Stockphoto_Upload_path, image)))

    files = list(worked_images)

    RBEfiles = list(RBE_images)
    SPEfiles = list(SPE_images)
    RBUfiles = list(RBU_images)
    SPUfiles = list(SPU_images)

    removecount = 0

    for file in files:
        if file in files and RBEfiles or SPEfiles or RBUfiles or SPUfiles:
            if file == "no_more_images.png":
                print("not moving", file)
            else:
                try:
                    os.remove(os.path.join(worked_images_dir, file))
                    removecount += 1
                except Exception as e:
                    print(e)
                print(file, "removed")
    print(f'Removed {removecount} files')

if __name__ == "__main__":
    Cleanup_images_folder()