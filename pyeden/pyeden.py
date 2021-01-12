import requests
from zipfile import ZipFile
import os
from os import path
import cv2
from glob import glob
from tqdm import tqdm
import numpy as np

FOLDER_NAME = 'DATA/'

def to_categorical(y, num_classes=None, dtype='float32'):
  y = np.array(y, dtype='int')
  input_shape = y.shape
  if input_shape and input_shape[-1] == 1 and len(input_shape) > 1:
    input_shape = tuple(input_shape[:-1])
  y = y.ravel()
  if not num_classes:
    num_classes = np.max(y) + 1
  n = y.shape[0]
  categorical = np.zeros((n, num_classes), dtype=dtype)
  categorical[np.arange(n), y] = 1
  output_shape = input_shape + (num_classes,)
  categorical = np.reshape(categorical, output_shape)
  return categorical

def is_picture(file):
    if file.lower().endswith("jpg") or file.lower().endswith("jpeg"):
        return True
    else:
        return False

def is_included(file_path, included_datasets):
    for included_dataset in included_datasets:
        if included_dataset in file_path:
            return True
    return False

def download_dataset(file_name):
    URL = 'http://localhost:3000/datasets/'
    print("Downloading", file_name)
    print("This could take some seconds...")
    r = requests.get(URL + file_name, allow_redirects=True)
    try:
        os.mkdir(FOLDER_NAME)
    except FileExistsError:
        pass
    
    open(FOLDER_NAME + file_name, 'wb').write(r.content)

    # Create a ZipFile Object and load sample.zip in it
    with ZipFile(FOLDER_NAME + file_name, 'r') as zipObj:
        print("Unzipping", file_name)
        # Extract all the contents of zip file in current directory
        zipObj.extractall(FOLDER_NAME + file_name.split(".")[0])
        os.remove(FOLDER_NAME + file_name)

def read_data(path, im_size=(128,128), included_datasets= []):
    tag2idx = {dataset:i for i, dataset in enumerate(included_datasets)}
    im_path = path + "*/*"
    print("Loading data...")
    X = np.array([cv2.resize(cv2.imread(file_path), im_size) 
                    for file_path in tqdm(glob(im_path))
                    if is_picture(file_path) and 
                       is_included(file_path, included_datasets)])
    y = [tag2idx[file_path.split("/")[1]] 
                                 for file_path in glob(im_path)
                                 if is_picture(file_path) and
                                    is_included(file_path, included_datasets)]

    y = np.array(to_categorical(y, num_classes=len(np.unique(y))))
    
    return X, y

# List of Formal Names['Black nightsade-220519-Weed-zz-V1', 
#                      'Broccoli-020919-Healthy-zz-V1', 
#                      'Broccoli-080919-Healthy-zz-V1']
def load_datasets(file_names=[],
                  im_size=(128, 128)):
    
    if path.exists(FOLDER_NAME):
        current_datasets = [file_name for file_name in os.listdir(FOLDER_NAME)]
    else:
        current_datasets = []
    web_file_names = [file_name + "_min" for file_name in file_names]
    for file_name in web_file_names:
        if file_name not in current_datasets:
            download_dataset(file_name + ".zip")
        else:
            print(file_name, "is locally available")
    
    X, y = read_data(path=FOLDER_NAME, included_datasets=web_file_names)
    return X, y