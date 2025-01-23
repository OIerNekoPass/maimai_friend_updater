import json
import requests
import sys
import maisql
from simulate_request import Get_VS_html
from bs4 import BeautifulSoup

level_name = ['basic', 'advanced', 'expert', 'master', 'remaster']

def rate_factor(grade):
    ranges = [
        (100.5, 0.224),
        (100.4999, 0.222),
        (100, 0.216),
        (99.9999, 0.214),
        (99.5, 0.211),
        (99, 0.208),
        (98.9999, 0.206),
        (98, 0.203),
        (97, 0.2),
        (96.9999, 0.176),
        (94, 0.168),
        (90, 0.152),
        (80, 0.136),
        (79.9999, 0.128),
        (75, 0.12),
        (70, 0.112),
        (60, 0.096),
        (50, 0.08),
        (40, 0.064),
        (30, 0.048),
        (20, 0.032),
        (10, 0.016),
    ]
    for i in ranges:
        if grade >= i[0]:
            return i[1]

def update(bot_uid, qq, level, json_dir = "./song_data/mai.json"):
    maisql.init()
    uid, maid = maisql.find_user(qq)
    if uid == "empty":
        return "你没注册喵"
    elif uid == "err":
        return "Error: Inside error"
    maisql.close()

    with open(json_dir, "r") as f:
        songs = json.load(f)
    
    soup = Get_VS_html(bot_uid, maid, level)

    # with open("test.html", "w") as f:
    #     f.write(soup.text)

    results = soup.find_all('div', class_=f'music_{level_name[level]}_score_back w_450 m_15 p_3 f_0')
    if results == []:
        return "Error: No data found. Maybe is because bot_uid overtime"

    maisql.init()
    for i in results:
        sname = i.find('div', class_='music_name_block t_l f_13 break').get_text(strip=True)
        grade = i.find_all('td', class_=f'p_r {level_name[level]}_score_label w_120 f_b')[1].get_text(strip=True)
        type = i.find('img', class_='music_kind_icon f_r').get('src')

        if type == 'https://maimai.wahlap.com/maimai-mobile/img/music_dx.png':
            type = 'DX'
        elif type == 'https://maimai.wahlap.com/maimai-mobile/img/music_standard.png':
            type = 'SD'
        else:
            maisql.close()
            return "Error: Unknown type"

        if grade == "― %":
            continue
        grade = float(grade[:-1])

        find = False
        for j in songs:
            if j['title'] == sname and j['type'] == type:
                song_info = j
                find = True
                break
        if not find: 
            # print(f"Warning: Song {sname} not found in database!")
            continue
        #     print(f"Song {sname} not found in database")
        #     print(i.find('div', class_='music_name_block t_l f_13 break'))
        #     print("=====================================")
        
        fac = rate_factor(grade)
        g = grade
        if g > 100.5: g = 100.5
        rating = int(song_info['ds'][level] * g * fac)

        if maisql.insert_record(uid, song_info['id'], grade, rating, level) == False:
            maisql.close()
            return "Error: Update error when inserting mysql."
        # print(f"Song {sname} : {grade}% : {fac} : {rating}")
    
    maisql.close()
    return "Success"
    # print("Done")

if __name__ == "__main__":
    # get input file from command line
    if len(sys.argv) != 4:
        print("Usage: python mai_request.py [bot_uid] [NickName] [level]")
        sys.exit(1)
    update(bot_uid = sys.argv[1], NickName = sys.argv[2], level = int(sys.argv[3]))