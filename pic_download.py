from PIL import Image
import requests
from io import BytesIO
import csv
import os
import json

error_list = []

def download_photo(url, save_path, file_name):
    os.makedirs(save_path, exist_ok=True)
    print(f'Downloading photo from {url}')
    file_name = os.path.join(save_path, file_name)
    try:
        rsp = requests.get(url, stream=True, timeout=30)
    except Exception as e:
        error_list.append(save_path)
        error_list.append(url)
        error_list.append("************************")
        print(f'Failed to download {url}: {type(e)}')
        return
    if 200 == rsp.status_code:
        try:
            img = Image.open(BytesIO(rsp.content))
            img = img.resize((130, 130))
            img.save(file_name)
            print(f'Saved to {file_name}')
        except Exception as e:
            print(e)
            error_list.append(save_path)
            error_list.append(url)
            error_list.append("************************")
    else:
        error_list.append(save_path)
        error_list.append(url)
        error_list.append("************************")
        print(f'Failed to download {url}. HTTP {rsp.status_code}')


with open("./song_data/mai.json", "r") as f:
    songs = json.load(f)
    
    for i in songs:
        id = i["id"]
        file_name = f"{id}.png"
        while len(file_name) < 9:
            file_name = "0" + file_name
        url = "https://www.diving-fish.com/covers/" + file_name
        download_photo(url, "song_pic", f"{id}.png")
    
    for e in error_list:
        print(e)