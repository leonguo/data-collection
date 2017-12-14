# -*- coding: UTF-8 -*-

from aip import AipOcr
import json
import requests
from io import BytesIO
try:
    import Image
except ImportError:
    from PIL import Image

# 定义常量
APP_ID = '9851066'
API_KEY = 'LUGBatgyRGoerR9FZbV4SQYk'
SECRET_KEY = 'fB2MNz1c2UHLTximFlC4laXPg7CVfyjV'

# 初始化AipFace对象
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# img_src = "http://img.58921.com/sites/all/movie/files/protec/90c2429118563ab2784b91a7bf7e8f32.png"
# response = requests.get(img_src)
# img = BytesIO(response.content)

filePath = "./img/t.png"
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

options = {
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
}

# 调用通用文字识别接口
result = aipOcr.basicGeneral(get_file_content(filePath), options)
print(json.dumps(result))