try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import requests
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

img_src = "http://img.58921.com/sites/all/movie/files/protec/eeba4743c229d809b3205de018a60ee6.png"
response = requests.get(img_src)
print response.content
img = Image.open(BytesIO(response.content))
print img
print(pytesseract.image_to_string(img))
