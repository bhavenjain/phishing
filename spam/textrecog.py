import cv2
import pytesseract


pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'
img = cv2.imread('quote.png')
text = pytesseract.image_to_string(img)
print(text)
