import pymysql

host = "localhost"      # 数据库地址
user = "root"           # 数据库用户名
password = "password"   # 数据库密码
database = "Mai_Data"   # 数据库名

def init():
    try:
        globals()['connection'] = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return True

    except pymysql.MySQLError as e:
        print("数据库连接失败：", e)
        return False

def find_user(qq):
    try:
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM user WHERE QQ = '{qq}';")
        res = cursor.fetchone()
        cursor.close()

        if res == None:
            print('用户未注册')
            return 'empty', 'empty'

        return res[0], res[2]

    except pymysql.MySQLError as e:
        print("查询失败：", e)
        return 'err', 'err'

def find_record(uid, sid, level):
    try:
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM play_record WHERE uid = '{uid}' AND sid = '{sid}' AND level = {level};")
        res = cursor.fetchone()
        cursor.close()

        if res == None:
            return False
        return True

    except pymysql.MySQLError as e:
        print("查询失败：", e)
        return False

def insert_record(uid, sid, score, rating, level):
    try: 
        cursor = connection.cursor()
        
        if find_record(uid, sid, level):
            cursor.execute(f"UPDATE play_record SET score = {score}, rating = {rating} WHERE uid = '{uid}' AND sid = '{sid}' AND level = {level};")
        else:
            cursor.execute(f"INSERT INTO play_record (uid, sid, score, rating, level) VALUES('{uid}', '{sid}', {score}, {rating}, {level});")

        connection.commit()
        cursor.close()
        return True

    except pymysql.MySQLError as e:
        print("插入失败：", e)
        return False

def set_sys_var(vname, val):
    try:
        cursor = connection.cursor()
        cursor.execute(f"UPDATE sysvar SET val = '{val}' WHERE vname = '{vname}';")
        connection.commit()
        cursor.close()
        return 

    except pymysql.MySQLError as e:
        print("更新失败：", e)
        return 

def get_sys_var(vname):
    try:
        cursor = connection.cursor()

        cursor.execute(f"SELECT val FROM sysvar WHERE vname = '{vname}';")
        res = cursor.fetchone()
        cursor.close()

        if res == None:
            return "not found"
        return res[0]

    except pymysql.MySQLError as e:
        print("查询失败：", e)
        return "err"

def update_song(sid, sname, isNew, level, ds, mtype):
    try: 
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO song_data (sid, sname, isNew, level, ds, type) 
            VALUES(%s, %s, %s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE 
            sname = VALUES(sname), 
            isNew = VALUES(isNew), 
            level = VALUES(level), 
            ds = VALUES(ds), 
            type = VALUES(type);
        """, (sid, sname, isNew, level, ds, mtype))
        connection.commit()
        cursor.close()
        return True

    except pymysql.MySQLError as e:
        print("插入失败：", e)
        return False

def close():
    connection.close()