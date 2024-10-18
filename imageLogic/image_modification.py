from io import BytesIO
from PIL import Image


class Image_modification():

    def reach_1024(self, file_path):
        #OCR API free plan takes only image smaller than 1024kb
        #First we turn them to grayscale, then we reduce resolution until ready.
        img = Image.open(file_path).convert('L')
        image_size_kb = self.get_image_size(img)
        while image_size_kb > 1024:
            img = self.resize_image(img)
            image_size_kb = self.get_image_size(img)
        return img
    
    def get_image_size(self, img):
        buffer = BytesIO()
        img.save(buffer, 'jpeg', quality=90)
        image_size_kb = buffer.tell() / 1024
        return image_size_kb

    def resize_image(self, img):
        w, h = img.size
        new_w = int(w * 0.9)
        new_h = int(h * 0.9)
        resized_img = img.resize((new_w, new_h))
        return resized_img