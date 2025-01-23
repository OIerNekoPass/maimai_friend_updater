import requests
import json
import os
import sys

def get_song(type = "mai", save_path = "./song_data"):
    filename = type + ".json"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    with open(os.path.join(save_path, filename), "w") as f:
        url = ""
        if type == "mai":
            url = "https://www.diving-fish.com/api/maimaidxprober/music_data"
        elif type == "chu":
            url = "https://www.diving-fish.com/api/chunithmprober/music_data"
        else:
            print("Invalid type")
            return
        response = requests.get(url)
        data = json.loads(response.text)
        json.dump(data, f)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        get_song(sys.argv[1])
    else:
        get_song()
