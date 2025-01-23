import sys
import asyncio
import maisql
from maimai_py import MaimaiClient, MaimaiPlates, MaimaiScores, MaimaiSongs, PlayerIdentifier, LXNSProvider, DivingFishProvider, ArcadeProvider 

async def get_score(NickName, qrstr):
    maisql.init()
    uid, maid = maisql.find_user(NickName)

    maimai = MaimaiClient()
    my_account = await maimai.qrcode(qrstr)

    scores = await maimai.scores(my_account, provider = ArcadeProvider(), kind = 1)
    for i in scores.scores:
        if maisql.insert_record(uid, i.id, i.achievements, i.dx_rating, i.level_index.value) == False:
            print('错误终止喵')
            return
    maisql.close()
    print('更新成功喵')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('参数缺失 需要2个参数')
    else:
        asyncio.run(get_score(sys.argv[1], sys.argv[2]))
