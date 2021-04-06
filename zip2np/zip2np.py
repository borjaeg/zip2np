from zipfile import ZipFile
import os
from os import path
import cv2
from glob import glob
from tqdm import tqdm
import numpy as np

FOLDER_NAME = 'DATA/'

def is_picture(file):
    if file.lower().endswith("jpg") or file.lower().endswith("jpeg"):
        return True
    else:
        return False

def unzip_folder(zip_name):
    # Create a ZipFile Object and load sample.zip in it
    with ZipFile(FOLDER_NAME + file_name, 'r') as zipObj:
        print("Unzipping", file_name)
        # Extract all the contents of zip file in current directory
        zipObj.extractall(FOLDER_NAME + file_name.split(".")[0])
        os.remove(FOLDER_NAME + file_name)

def read_data(path, im_size=(128,128)):
    tag2idx = {tag:i for i, tag in enumerate(os.listdir(path))}
    im_path = path + "*/*"
    print("Loading data...")
    X = np.array([cv2.resize(cv2.imread(file_path), im_size) 
                    for file_path in tqdm(glob(im_path))
                    if is_picture(file_path)])
    y = [tag2idx[file_path.split("/")[1]] 
                                 for file_path in glob(im_path)
                                 if is_picture(file_path) and
                                    is_included(file_path, included_datasets)]

    #y = np.array(to_categorical(y, num_classes=len(np.unique(y))))
    y = np.eye(len(np.unique(y)))[y].astype(np.uint8)
    
    return X, y

def load_datasets(file_names=[],
                  im_size=(128, 128)):
        
    X, y = read_data(path=FOLDER_NAME, included_datasets=web_file_names)
    return X, y