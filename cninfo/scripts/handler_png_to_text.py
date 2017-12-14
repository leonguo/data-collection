# -*- coding: utf-8 -*-
try:
    import Image
except ImportError:
    from PIL import Image

import imutils
import pytesseract
import requests
from io import BytesIO
import numpy as np
import cv2
from skimage.morphology import disk
from skimage.filters import rank


# 分析图片数字


if __name__ == "__main__":

    tessdata_dir_config = '--tessdata-dir "C:/Program Files (x86)/Tesseract-OCR/"'
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

    img_src = "http://img.58921.com/sites/all/movie/files/protec/90c2429118563ab2784b91a7bf7e8f32.png"
    response = requests.get(img_src)
    img = Image.open(BytesIO(response.content))
    # img = Image.open('temp2.png')

    print(pytesseract.image_to_string(img, lang='chi_sim', config=tessdata_dir_config))
