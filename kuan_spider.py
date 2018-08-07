'''
为了避免二次伤害，没有代码
就思路进行整理如下：

1.使用到的库
import datetime  # 转换时间
import json  # 数据类型转换
import threading  # 多线程
import random  # 使用随机数
import pymongo  # 数据库
import requests  # 请求库
import time  # 主要使用休眠功能

2.代码结构
class GetHtml(object):  # 将网络请求抽离为一个类
    def get_one_page(self, url):
        # 做好各种异常的捕捉
        pass
class Parse(object):  # 主要负责解析获得的源数据
    def parse(self, response):
        # 可以做一个判断response是否为None
        # 由于返回的数据为json格式，使用常规的dict操作即可
        pass
class Save(object):  # 将获得的数据保存
    def mongodb(self):
        # 保存到mongodb数据库。也可以其他数据库或本地文件等
        pass
def run(uid):  # 主要实现逻辑
    # 拿uid与url结合发起request
    # 将response交由Parse解析处理
    # 将Parse处理后的数据交由Save入库
    pass
if __name__ == '__main__':
    for uid in range(10002, 9999999):
        # 可以在此处开启多线程
        run(uid)
        pass

3.难点
使用Charles配合MuMu模拟器抓包获得url
headers中有一参数至关重要，即x-app-token，目测是根据时间经过某种算法计算得来，
这里提供一个："eb2f51ceffc67e0d3ac00708336bd8fadb7471dd-739b-3569-9d1d-ea26e64edf235x5c6d7c47"（2018-8-4 22:10可用），具体什么时间不能用了我就不晓得了。
其他方面暂未遇到难点

4.原始返回数据结构
{'uid': 10002, 'username': '阿酷', 'admintype': 2, 'groupid': 2, 'usergroupid': 125, 'level': 25, 'status': 1, 'usernamestatus': 0, 'avatarstatus': 1479884946, 'logintime': '2018-07-31 23:12:49', 'entityType': 'user', 'entityId': 10002, 'displayUsername': '阿酷', 'url': '/u/10002', 'userAvatar': 'http://avatar.coolapk.com/data/000/01/00/02_avatar_big.jpg?1479884946', 'userBigAvatar': 'http://avatar.coolapk.com/data/000/01/00/02_avatar_big.jpg?1479884946', 'groupName': '主编', 'userGroupName': 'Lv.25', 'isBlackList': 0, 'isIgnoreList': 0, 'isLimitList': 0, 'gender': 1, 'province': '北京', 'city': '朝阳', 'astro': '水瓶座', 'weibo': 'boboweb', 'blog': '', 'bio': '微博/微信：boboweb', 'isDeveloper': 0, 'verify_type': '', 'verify_title': '', 'verify_status': 0, 'apkDevNum': 0, 'feed': 1918, 'follow': 292, 'fans': 9775, 'apkFollowNum': 48, 'apkRatingNum': 123, 'apkCommentNum': 0, 'albumNum': 11, 'albumFavNum': 0, 'discoveryNum': 162, 'replyNum': 0, 'isFollow': 0}

5.存储数据结构
{"uid": r.get("uid"),  # 用户id
  "username": r.get("username"),  # 用户昵称
  "admintype": r.get("admintype"),  # 管理类型，具体代表什么还不得而知
  "groupid": r.get("groupid"),  # 集团id，也不知道是做什么用的
  "usergroupid": r.get("usergroupid"),  # 用户组id，也不知道是做什么用的
  "level": r.get("level"),  # 翻译的意思是  水平/标准/平坦的
  "status": r.get("status"),  # 状态，不知指的什么状态
  "usernamestatus": r.get("usernamestatus"),  # 用户名的地位，不知指的什么地位
  "avatarstatus": r.get("avatarstatus"),  # 头像状态，不知指的什么状态
  "logintime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(r.get("logintime")))),  # 最后登录时间
  "entityType": r.get("entityType"),  # 实体类型，大致为账户类型
  "entityId": r.get("entityId"),  # 实体ip，估计和uid一致
  "displayUsername": r.get("displayUsername"),  # 对外显示name？难道和username不一样吗
  "url": r.get("url"),  # 个人中心url
  "userAvatar": r.get("userAvatar"),  # 头像url
  "userBigAvatar": r.get("userBigAvatar"),  # 头像url，这个是大图，Big
  "groupName": r.get("groupName"),  # 身份，其中有开发者，禁止发言，主编，编辑
  "userGroupName": r.get("userGroupName"),  # value是等级，这里不知道为什么是name
  "isBlackList": r.get("isBlackList"),  # 是否在黑名单中，0=false
  "isIgnoreList": r.get("isIgnoreList"),  # 是否被忽略？，0=false
  "isLimitList": r.get("isLimitList"),  # 是否被限制？，0=false
  "gender": r.get("gender"),  # 性别，1=男，0=女，-1=未填
  "province": r.get("province"),  # 省份/直辖市
  "city": r.get("city"),  # 城市/直辖市的区
  "astro": r.get("astro"),  # 星座
  "weibo": r.get("weibo"),  # 微博名字
  "blog": r.get("blog"),  # 博客
  "bio": r.get("bio"),  # 其他联系方式？
  "isDeveloper": r.get("isDeveloper"),  # 是否为开发者，0=false
  "verify_type": r.get("verify_type"),  # 验证类型？验证什么的类型？
  "verify_title": r.get("verify_title"),  # 验证标题？验证什么的标题？
  "verify_status": r.get("verify_status"),  # 验证状态？验证什么的状态？，0=false不是验证状态？
  "apkDevNum": r.get("apkDevNum"),  # 名下开发的app数量
  "feed": r.get("feed"),  # 动态数量
  "follow": r.get("follow"),  # 关注人数
  "fans": r.get("fans"),  # 粉丝数
  "apkFollowNum": r.get("apkFollowNum"),  # 关注的app的数量，等于说关注了多少app
  "apkRatingNum": r.get("apkRatingNum"),  # 评分的app的数量，等于说给多少app打过分
  "apkCommentNum": r.get("apkCommentNum"),  # 软件评论数？
  "albumNum": r.get("albumNum"),  # 应用集数量
  "albumFavNum": r.get("albumFavNum"),  # 关注的应用集数量？
  "discoveryNum": r.get("discoveryNum"),  # 发现的app数量，（提交的app数量）
  "replyNum": r.get("replyNum"),  # 回复的数量？
  "isFollow": r.get("isFollow"),  # 是否跟随/关注？，0=false
}

6.使用的url和headers
url = "https://api.coolapk.com/v6/user/profile?uid={}".format(uid)
headers = {
    "user-agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; HUAWEI MLA-AL10 Build/HUAWEIMLA-AL10) (#Build; HUAWEI; HUAWEI MLA-AL10; MLA-AL10-user 5.1.1 HUAWEIMLA-AL10 500180710 release-keys; 5.1.1) +CoolMarket/8.6",
    "x-requested-with": "XMLHttpRequest",
    "x-app-id": "com.coolapk.market",
    "x-app-token": "eb2f51ceffc67e0d3ac00708336bd8fadb7471dd-739b-3569-9d1d-ea26e64edf235x5c6d7c47",
}

(未使用代理、cookie)
希望对你有所帮助
'''
