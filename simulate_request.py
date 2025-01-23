import json
import requests
from bs4 import BeautifulSoup
import re
import maisql

def Get_VS_html(bot_uid, friend_uid, diff):
    url = f"https://maimai.wahlap.com/maimai-mobile/friend/friendGenreVs/battleStart/?scoreType=2&genre=99&diff={diff}&idx={friend_uid}"
    # print("visiting ", url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': f'https://maimai.wahlap.com/maimai-mobile/friend/friendGenreVs/battleStart/?scoreType=2&genre=99&diff=4&idx={friend_uid}',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': f'userId={bot_uid};'
    }
    result = requests.get(url, headers=headers)

    if result.status_code != 200:
        # return Error
        print(f"Error: {result.status_code}")
        return None

    set_cookie = result.headers.get('Set-Cookie')
    # print("new cookies:", set_cookie)

    match = re.search(r'userId=([^;]+)', set_cookie)
    if match:
        user_id = match.group(1)
        # print("new uid:", user_id)
        maisql.init()
        maisql.set_sys_var("uid", str(user_id))
        maisql.close()

    return BeautifulSoup(result.text, 'html.parser')