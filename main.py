import threading

from PIL import Image
import os
import shutil
import re
import math


class Thread(threading.Thread):
    def __init__(self, threadID, filepath, mode):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.filepath = filepath
        self.mode = mode

    def run(self):
        process_image(self.filepath, self.mode)


def inject_optimized_directory_into_path(directory_name, file_path):
    new_file_path_list = []
    separator = "/"
    should_inject = 0
    for index, sub_path in enumerate(file_path.split(separator)):
        if should_inject == 1:
            new_file_path_list.append(directory_name)
            should_inject = should_inject + 1
        if sub_path == "images":
            should_inject = should_inject + 1

        new_file_path_list.append(sub_path)

    return separator.join(new_file_path_list)


def prepare_main_directories():
    # create directory for minified images
    if not os.path.exists("./public/images/progressive"):
        print("[DEBUG] Progressive directory doesn't exist, creating now.")
        os.makedirs("./public/images/progressive", exist_ok=True)

    if not os.path.exists("./public/images/webp"):
        print("[DEBUG] Webp directory doesn't exist, creating now.")
        os.mkdir("./public/images/webp")
        os.makedirs("./public/images/webp", exist_ok=True)


def is_supported_file(file_name):
    return file_name.endswith(".png") or file_name.endswith(".jpg") or file_name.endswith(".jpeg")


def create_directory(file_name):
    directory_paths = []
    for sub_path in file_name.split('/'):
        if re.search("(.png)|(.jpg)|(.jpeg)|(.webp)$", sub_path):
            break
        directory_paths.append(sub_path)

    directory_path = "/".join(directory_paths)
    if not os.path.exists(directory_path):
        print("[DEBUG] Trying to create sub directory:", directory_path)
        try:
            os.makedirs(directory_path, exist_ok=True)
            print("[DEBUG] Directory: '" + directory_path + "' has been created.")
        except Exception as error:
            print("[ERROR] Failed creating sub directory:", error)


def make_progressive(file_path, image):
    min_filename = inject_optimized_directory_into_path("progressive", file_path)
    create_directory(min_filename)
    width, height = image.size
    percent = 0.03
    width = math.floor(width * percent)
    if width == 0:
        width = 1
    height = math.floor(height * percent)
    if height == 0:
        height = 1
    dimensions = (width, height)
    image.resize(dimensions).save(min_filename, optimize=True, quality=60)
    print("[INFO] Created file:", min_filename)


def make_webp(file_path, image):
    webp_filename = inject_optimized_directory_into_path("webp", file_path)
    webp_filename = re.sub(r"(.png)|(.jpg)|(.jpeg)", ".webp", webp_filename)
    create_directory(webp_filename)
    image.save(webp_filename, "webp", optimize=True, quality=100)
    print("[INFO] Created a webp file:", webp_filename)


def through_files(file_set, root_directory):
    thread_list = []
    for index, filename in enumerate(file_set):
        if not is_supported_file(filename):
            continue

        # get full file path
        filepath = os.path.join(root_directory, filename)
        if "webp" in filepath or "progressive" in filepath:
            continue

        thread = Thread(index, filepath, get_image_mode(filename))
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()


def get_image_mode(filename):
    mode = "RGB"
    if filename.endswith(".png"):
        mode = "RGBA"
    return mode


def process_image(filepath, mode):
    with Image.open(filepath).convert(mode) as img:
        # create minified copy
        make_progressive(filepath, img)
        # create WebP version
        make_webp(filepath, img)


def ask_for_directory_to_fetch():
    while True:
        result = input("Insert path to images directory: ")
        if not os.path.exists(result):
            print("[ERROR] You've entered non existent path, try again.")
        else:
            break

    return result


def fetch_directory(directory_name):
    shutil.rmtree("./public")
    print("[DEBUG] removing existing public directory")
    shutil.copytree(directory_name, "./public/images")
    print("[DEBUG] copied images from: '" + directory_name + "'")


def upload_to_fetched_directory(directory_name):
    shutil.rmtree(directory_name)
    shutil.copytree("./public/images", directory_name)
    print("[DEBUG] uploaded images to: '" + directory_name + "'")


def get_working_mode():
    result = 0
    while result != '1' and result != '2':
        result = input("Select mode of minification:\n1. Only one file.\n2. Whole directory\nYour choice: ")

    return int(result)


def single_file_minification():
    while True:
        file = input("Pass file to minify: ")
        if not os.path.exists(file):
            print("[DEBUG] file doesn't exist")
        else:
            break

    process_image(file, get_image_mode(file))


if __name__ == '__main__':
    working_mode = get_working_mode()
    if working_mode == 1:
        single_file_minification()
    elif working_mode == 2:
        directory_to_fetch = ask_for_directory_to_fetch()
        fetch_directory(directory_to_fetch)
        prepare_main_directories()
        # loop through images in public/images directory and subdirectories
        for root, dirs, files in os.walk("./public/images"):
            through_files(files, root)

        upload_to_fetched_directory(directory_to_fetch)
    else:
        print("[ERROR] unknown mode")
