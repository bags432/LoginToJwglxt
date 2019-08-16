# -*- coding=utf-8 -*-
import requests
import time
from lxml import etree
from hex2b64 import HB64
import RSAJS

class Login():

    def __init__(self,user,password,login_url,login_KeyUrl):
        # 初始化程序数据
        self.Username = user
        self.Password = password
        nowTime = lambda:str(round(time.time()*1000))
        self.now_time = nowTime()

        self.login_url = login_url
        self.login_Key = login_KeyUrl

    def Get_indexHtml(self):
        # 获取教务系统网站
        self.session = requests.session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Referer": "http://jwxt.fjut.edu.cn/jwglxt/xtgl/login_slogin.html",
            "Upgrade-Insecure-Requests": "1"
        })

        self.response = self.session.get(self.login_url+ self.now_time).content.decode("utf-8")

    def Get_csrftoken(self):
        # 获取到csrftoken
        lxml = etree.HTML(self.response)
        self.csrftoken = lxml.xpath("//input[@id='csrftoken']/@value")[0]

    def Get_PublicKey(self):
        # 获取到加密公钥
        key_html = self.session.get(self.login_Key + self.now_time)
        key_data = key_html.json()
        print(key_data)
        self.modulus = key_data["modulus"]
        self.exponent = key_data["exponent"]

    def Get_RSA_Password(self):
        # 生成RSA加密密码
        rsaKey = RSAJS.RSAKey()
        rsaKey.setPublic(HB64().b642hex(self.modulus),HB64().b642hex(self.exponent))
        self.enPassword = HB64().hex2b64(rsaKey.encrypt(self.Password))

    def Login_Home(self):
        # 登录信息门户,成功返回session对象
        self.Get_indexHtml()
        self.Get_csrftoken()
        self.Get_PublicKey()
        self.Get_RSA_Password()
        login_data = [("csrftoken", self.csrftoken),("yhm", self.Username),("mm", self.enPassword),("mm", self.enPassword)]
        login_html = self.session.post(self.login_url + self.now_time,data=login_data)

        # 当提交的表单是正确的，url会跳转到主页，所以此处根据url有没有跳转来判断是否登录成功
        if login_html.url.find("login_slogin.html") == -1: # -1没找到，说明已经跳转到主页
            print("登录成功")
            return self.session
        else:
            print("用户名或密码不正确，登录失败")
            exit()

class TimeTable():
    def __init__(self,session,table_url,xnm,xqm):
        data = {"xnm":xnm,"xqm":xqm}
        table_info = session.post(table_url,data = data).json()
        print(table_info)
        #print(table_info["sjkList"]) #实践课程 网络课程
        # for each in table_info["kbList"]:
        #     print(each["xqjmc"], each["jc"], each["cdmc"], each["zcd"], each["kcmc"])

class MarkTable():
    def __init__(self,session,mark_url,xnm,xqm):
        data = {"xnm":xnm,"xqm":xqm,"queryModel.showCount":"100"}
        mark_info = session.post(mark_url,data = data).json()
        print(mark_info)
        if mark_info['items'] == []:
            print("本学期暂无成绩")
        else:
            for each in mark_info["items"]:
                print(each['kcmc'], each['cj'],each['xf'])

class ExamTable():
    def __init__(self,session,exam_url,xnm,xqm):
        data = {"xnm":xnm,"xqm":xqm,"queryModel.showCount":"100"}
        exam_info = session.post(exam_url,data = data).json()
        print(exam_info)
        if exam_info['items'] == []:
            print("本学期暂无考试信息")
        else:
            for each in exam_info["items"]:
                print(each['kcmc'], each['cdmc'], each['kssj'],each['zwh'])


if __name__ == "__main__":
    # 登录主页url
    login_url = "http://jwxt.fjut.edu.cn/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t="
    # 请求PublicKey的URL
    login_KeyUrl = "http://jwxt.fjut.edu.cn/jwglxt/xtgl/login_getPublicKey.html?time="
    # 课表URL
    table_url = "http://jwxt.fjut.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151"
    # 成绩的URL
    mark_url = "http://jwxt.fjut.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005"
    # 考试信息的URL
    exam_url = "http://jwxt.fjut.edu.cn/jwglxt/kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N358105"

    user = "3171911234"
    password = ""
    xnm = "2019"
    xqm = "3"

    f = Login(user,password, login_url, login_KeyUrl)
    response_cookies = f.Login_Home()
    table = TimeTable(response_cookies, table_url,xnm,xqm)
    mark = MarkTable(response_cookies, mark_url,xnm,xqm)
    exam = ExamTable(response_cookies, exam_url,xnm,xqm)