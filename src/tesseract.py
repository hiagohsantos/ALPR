from PIL import Image
import pytesseract
import cv2
import numpy as np


imagem_modelo = cv2.cvtColor(cv2.imread("../images/img8.jpeg"), cv2.COLOR_BGR2GRAY)
img_resized = cv2.resize(imagem_modelo, (150,50), interpolation = cv2.INTER_AREA)
imagem_limiarizada  = cv2.adaptiveThreshold(img_resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

cv2.imshow("Display window", imagem_limiarizada)
img = Image.fromarray(imagem_limiarizada)

text =  pytesseract.image_to_data(img, config = "--oem 3 --psm 13" )
print(text)
k = cv2.waitKey(0) # Wait for a keystroke in the window