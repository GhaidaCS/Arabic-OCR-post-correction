from PIL import Image
import pytesseract

image = Image.open("test.png")

text = pytesseract.image_to_string(
    image,
    lang="ara"
)

print(text)