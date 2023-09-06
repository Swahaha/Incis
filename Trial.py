from PIL import Image
from pytesseract import pytesseract

#Define path to tesseract.exe 
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#Define path to image
image_path = r'C:\Users\Swarajh Mehta\Desktop\Projects\Incisus\trial.jpg'

#Define tesseract_cmd to tesseract.exe
pytesseract.tesseract_cmd = tesseract_path

#Open image with PIL
img = Image.open(image_path)

#Extract text from image
text = pytesseract.image_to_string(img)

print(text)
