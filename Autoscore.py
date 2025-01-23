import mai_request
import sys
import maisql
import time


def current_uid():
    maisql.init()
    uid = maisql.get_sys_var("uid")
    maisql.close()
    return str(uid)

if __name__ == "__main__":
    for i in range(2, 5):
        ret = mai_request.update(bot_uid = current_uid(), qq = sys.argv[1], json_dir = sys.argv[2], level = i)
        if ret != "Success":
            print(ret, end = "")
            exit(0)
        time.sleep(2)
        
    print("更新完成喵", end = "")