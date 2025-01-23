import maisql
import json
import sys

def update(json_dir = "./song_data/mai.json"):
    with open(json_dir, "r") as f:
        songs = json.load(f)

    maisql.init()
    for i in songs:
        lstr = ""
        dstr = ""
        for l in i['level']:
            lstr = lstr + l + ","
        for d in i['ds']:
            dstr = dstr + str(d) + ","
        # print(i['id'], i['title'], i['basic_info']['is_new'], lstr, dstr, i['type'])
        maisql.update_song(i['id'], i['title'], i['basic_info']['is_new'], lstr, dstr, i['type'])
    
    maisql.close()
    return "Success"

if __name__ == "__main__":
    print(update())