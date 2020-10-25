import requests
from zipfile import ZipFile
import os
import cv2
from glob import glob
from tqdm import tqdm
import numpy as np

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

def download_dataset(file_name):
    URL = 'http://localhost:3000/datasets/'
    FOLDER_NAME = 'DATA'
    print("Downloading", file_name)
    r = requests.get(URL + file_name, allow_redirects=True)
    try:
        os.mkdir(FOLDER_NAME)
    except FileExistsError:
        pass
    
    open(FOLDER_NAME + "/" + file_name, 'wb').write(r.content)

    # Create a ZipFile Object and load sample.zip in it
    with ZipFile(FOLDER_NAME + "/" + file_name, 'r') as zipObj:
        print("Unzipping", file_name)
        # Extract all the contents of zip file in current directory
        zipObj.extractall(FOLDER_NAME + "/" + file_name.split(".")[0])
        os.remove(FOLDER_NAME + "/" + file_name)

def read_data(path, im_size=(128,128)):
    tag2idx = {tag:i for i, tag in enumerate(os.listdir(path))}
    im_path = path + "*/*"
    print("Reading data...")
    X = np.array([cv2.resize(cv2.imread(im_file), im_size) 
                    for im_file in tqdm(glob(im_path))
                    if is_picture(im_file)])
    y = [tag2idx[im_file.split("/")[1]] 
                                 for im_file in tqdm(glob(im_path))
                                 if is_picture(im_file)]
    
    y = np.array(to_categorical(y, num_classes=len(np.unique(y))))
    
    return X, y

#['Black nightsade-22-MAY-2019-v1', 'Broccoli-02-SEP-2019-v1']
def load_datasets(file_names=[],
                 im_size=(128, 128)):
    for file_name in file_names:
        download_dataset(file_name + ".zip")
    
    X, y = read_data(path="DATA/")
    return X, y