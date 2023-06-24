from aip import AipOcr


import os
APP_ID = '28462625'
API_KEY = 'sM9FzUM8ppx91OwONhkdCFu9'
SECRET_KEY = 'MvpCucP7EWEhOeAVADU4nig7eydOuGW4'
#百度识别车牌
filename = 'file/key.txt'


client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

client.setSocketTimeoutInMillis(5000)
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def getcn():
    with open(r'D:\360安全浏览器下载\carnumber\file\test05.jpg', 'rb') as fp:
        image = fp.read()
    results = client.licensePlate(image)
    a = results['words_result']['number']
    return a
