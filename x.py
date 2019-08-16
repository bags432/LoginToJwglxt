import requests
import urllib.request
from lxml import etree
class LoginVpn():
    def __init__(self,stu,pwd,login_url):
        self.stu = stu;
        self.pwd = pwd;
        self.login_url = login_url;

    def Get_authenticity_token(self):
        # 获取到csrftoken
        request = urllib.request.Request('https://webvpn.fjut.edu.cn/users/sign_in')
        response = urllib.request.urlopen(request)
        self.response = response.read().decode("utf-8")
        lxml = etree.HTML(self.response)
        self.authenticity = lxml.xpath("/html/head/meta[12]/@content")[0]
        print(self.authenticity)

    def Login_Home(self):
        # 登录主页,成功返回session对象
        self.Get_authenticity_token()

        login_data = [("utf8", "✓"), ("authenticity_token", self.authenticity), ("user[login]", self.stu), ("user[password]", self.pwd), ("commit", "登录 Login")]
        login_html = requests.post(self.login_url, data=login_data)

        # 当提交的表单是正确的，url会跳转到主页，所以此处根据url有没有跳转来判断是否登录成功
        if login_html.url.find("sign_in") == -1: # -1没找到，说明已经跳转到主页
            print("登录成功")

        else:
            print("用户名或密码不正确，登录失败")
            exit()

if __name__ == "__main__":

    login_url = "https://webvpn.fjut.edu.cn/users/sign_in"
    f = LoginVpn('3171911234', 'AA550100', login_url)
    #f.Get_authenticity_token()
    response_cookies = f.Login_Home()


















