from PIL import ImageGrab, Image
import pyperclip
import os, io

def main():
    img = ImageGrab.grabclipboard()
    tmpf = '/tmp/paste.png'
    # img_bytes = io.BytesIO()
    if isinstance(img, Image.Image):
        img.save(tmpf, 'PNG')
        os.system("pbcopy < {}".format(tmpf))
    else:
        print("images is None")

    # text = pyperclip.paste()
    # print(text)
if __name__ == '__main__':
    main()
