try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import requests
from io import BytesIO

tessdata_dir_config = '--tessdata-dir "C:/Program Files (x86)/Tesseract-OCR/"'
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

img_src = "http://img.58921.com/sites/all/movie/files/protec/eeba4743c229d809b3205de018a60ee6.png"
response = requests.get(img_src)
img = Image.open(BytesIO(response.content))
print(pytesseract.image_to_string(img, lang='chi_sim', config=tessdata_dir_config))
