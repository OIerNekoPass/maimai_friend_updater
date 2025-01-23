import maisql
from mitmproxy import http
from mitmproxy import ctx
import requests

local = "127.0.0.1"

# 过滤指定的URL并输出Cookie
def request(flow: http.HTTPFlow) -> None:
    # flow.request.host = local
    # 如果URL匹配目标网址
    if "maimai.wahlap.com/maimai-mobile/home/" in flow.request.url:
        # 获取请求头中的Cookie并输出
        cookies = flow.request.headers.get('cookie')
        if cookies:
            for cookie in cookies.split(';'):
                if 'userId=' in cookie:
                    userid = cookie.split('=')[1].strip()
                    print(f"-------------\n\nuserid: {userid}\n\n-------------")
                    maisql.init()
                    maisql.set_sys_var("uid", userid)
                    maisql.close()
                    return
            print("No 'userid' found in cookies.")
        else:
            print("No cookies found.")

# 通过mitmproxy启动脚本
def start():
    ctx.log.info("Start intercepting requests for cookies.")
    return request

# 2226098905586969
# 2226098905586969
