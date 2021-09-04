import os
import shutil
import sys

EXISTENT_PHOTOS_PATH = sys.argv[1]  # '/home/username/photos/'
IPHONE_PHOTOS_PATH = sys.argv[2]  # '/home/username/iPhone8/DCIM/' - mounted folder
SAVE_PHOTOS_PATH = sys.argv[3]   # '/home/username/new_photos/'

existing_files = set(os.listdir(EXISTENT_PHOTOS_PATH))

photos_folders = os.listdir(IPHONE_PHOTOS_PATH)
for folder in photos_folders:
    current_folder_path = IPHONE_PHOTOS_PATH + f'{folder}/'
    photos_name = os.listdir(current_folder_path)
    print(f'COPYING FROM {folder}')
    for photo in photos_name:
        current_photo_path = IPHONE_PHOTOS_PATH + f'{folder}/{photo}'
        if not os.path.isfile(current_photo_path):
            continue
        if photo not in existing_files:
            print(f'Copying file {photo}')
            shutil.copy(current_photo_path, SAVE_PHOTOS_PATH + f'{photo}')
        else:
            print(f'Skipping file {photo}')
