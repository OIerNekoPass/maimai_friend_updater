import os
import json

with open("./song_data/error.txt", "r") as f:
    ori_str = f.read()
    ids = ori_str.split('\n')
    for i in ids:
        while i[0] == '0': i = i[1:]
        print(i)

with open("./song_data/mai.json", "r") as f:
    songs = json.load(f)
    
    for i in songs:
        id = i["id"]

        if id in ["185", "524", "1235"]:
            print(f'"{i["title"]}", {id}')