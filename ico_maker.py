from PIL import Image

img = Image.open("images/icon.png")
img.save("images/icon.ico", sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
