import easyocr
import PIL
from PIL import ImageDraw

reader = easyocr.Reader(['en'])


im = PIL.Image.open("img.jpeg")

bounds = reader.readtext(im)
