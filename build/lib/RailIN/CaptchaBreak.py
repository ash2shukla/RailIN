from PIL import Image

from os import remove

from pytesseract import image_to_string as its

class Captcha:
    def _add_background(self,image):
        data = image.convert('RGBA').getdata()
        to_White = []
        for i in data:
            if i[3]==0:
                to_White.append((255,255,255,255))
            else:
                to_White.append(i)
        image.putdata(to_White)
        return image

    def decode(self,raw_image):
        file = open('/tmp/x.png','wb')
        file.write(raw_image)
        file.close()
        data = Image.open('/tmp/x.png')
        # adding background after scaling will create blurry image
        data = self._add_background(data)
        # resize the image to 300 x 128 for better recognition by tesseract
        data = data.resize((300,128),Image.ANTIALIAS)
        remove('/tmp/x.png')
        # convert all pixel's alpha to 255
        string = its(data)
        try:
            end = string.index('=')
        except ValueError:
            # if = doesn't exist in string then
            # sometimes = is recognized as semicolon
            end = string.index(':')
        finally:
            # return evaluated string before = or :
            # if neither = nor : is found then something wrong went
            # rather than raising an error return 0
            try:
                return str(eval(string[:end]))
            except NameError:
                # if end was undefined i.e. = or : isn't defined.
                return '0'
