# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
import base64

CHARS = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

def text_to_num(text): #text like this "hello-fuck-shit"
    words = text.split("-")
    str1 = ""
    for word in words:
        letters = list(word)
        str2 = ""
        for letter in letters:
            pos = CHARS.index(letter)
            pos = pos+1
            str2 = str2 + str(pos) + "."
        str1 = str1 + "-" + str2[:-1]
    return str1[1:]
def num_to_text(num):
    text = num.split("-")
    str1 = ""
    for word in text:
        letters = word.split(".")
        str2 = ""
        for letter in letters:
            char = CHARS[int(letter)-1]
            str2 = str2 + char
        str1 = str1 + str2 + " "
    return str1[:-1]
 
class aescrypt():
    # 初始化对象
    def __init__(self, key, model, iv, encode_):
        self.encode_ = encode_
        self.model = {'ECB': AES.MODE_ECB, 'CBC': AES.MODE_CBC}[model]
        self.key = self.add_16(key)
        # CBC加密需要初始化向量IV，必须是16位，ECB模式不需要。
        self.iv = iv.encode()
        if model == 'ECB':
            self.aes = AES.new(self.key, self.model)
        elif model == 'CBC':
            self.aes = AES.new(self.key, self.model, self.iv)
 
    # 秘钥长度必须为16、24、32，目前16位足够
    def add_16(self, par):
        par = par.encode(self.encode_)
        while len(par) % 16 != 0:
            par += b'\x00'
        return par
 
    # 加密
    def aesencrypt(self, text):
        text = self.add_16(text)
        self.encrypt_text = self.aes.encrypt(text)
        return base64.encodebytes(self.encrypt_text).decode().strip()
 
    # 解密
    def aesdecrypt(self, text):
        ''' 两种解密方式不通用 '''
        if self.model == AES.MODE_CBC:
            self.aes = AES.new(self.key, self.model, self.iv)
            text = base64.decodebytes(text.encode(self.encode_))
            self.decrypt_text = self.aes.decrypt(text)
            return self.decrypt_text.decode(self.encode_).strip('\0')
        elif self.model == AES.MODE_ECB:
            text = base64.decodebytes(text.encode(self.encode_))
            self.decrypt_text = self.aes.decrypt(text)
            return self.decrypt_text.decode(self.encode_).strip('\0')
 
 
if __name__ == '__main__':
    print("############################我的加解密脚本############################")
    print("############################初始化密钥############################")
    my_name = input("请输入我的名字拼音，比如我叫王自如，就输入wangziru:")
    print("你输入的是:",my_name)
    key_bank = input("请输入我的银行取款密码六位数字:")
    print("你输入的是:",key_bank)
    first_love_name = input("请输入我第一个喜欢女孩的名字拼音:")
    print("你输入的是:",first_love_name)
    first_love_birthday = input("请输入我第一个喜欢女孩的生日(我曾用它和我的生日组合做过密码)，格式MM-DAY如0721:")
    print("你输入的是:",first_love_birthday)
    roomate_code = input("请输入我大学室友学号(我们曾将它作为宿舍的WiFi密码813104--)的最后两位:")
    print("你输入的是:",roomate_code)
    key = my_name + key_bank + first_love_name + first_love_birthday + roomate_code  # 秘钥
    #限制key最长不超过32
    if len(key) > 32:
        key = key[0:32]
    print("你输入的key:",key)
    # CBC  需要初始化向量IV
    IV = key[0:16] #偏移量 16 位！！
    while True:
        pattern_cbc = aescrypt(key, 'CBC', IV, 'utf8') #第一个参数为秘钥 第二参数为加密模式 第三个为偏移量 第四个你懂得不解释
        print("############################功能选择############################")
        print("1、输入1回车进入加密程序。   ")
        print("2、输入2回车进入解密程序。")
        print("3、输入其它字符回车退出解密程序。")
        select = input("请选择:")
        if select == "1":
            text = input("输入待加密的文本格式如very-beautiful-day:")
            num = text_to_num(text)
            cbc_text = pattern_cbc.aesencrypt(num)#text就是你要加密的内容
            #对加密后的密文进行base64编码方便保存传输
            cbc_text = base64.b64encode(cbc_text.encode())
            print('加密后密文：',cbc_text.decode())
        elif select == "2":
            cbc_text = input("请输入待解密的文本:")
            #先进行base64解码
            cbc_text = base64.b64decode(cbc_text)
            cbc_data = pattern_cbc.aesdecrypt(cbc_text.decode())
            text = num_to_text(cbc_data)
            print('解密文:', text)
        else:
            break
 
