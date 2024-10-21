from io import BytesIO
from PIL import Image

class Image_modification():

    def reach_1024(self, file_path, page2):
        # OCR API free plan only takes image smaller than 1024kb
        # In order to reduce image size, we first save it to jpeg with a 90% quality, then we reduce resolution until ready.
        img = Image.open(file_path)
        buffer = BytesIO()
        # First we save in buffer a jpeg at 90% quality
        img.save(buffer, 'jpeg', quality=90)

        # We check the size
        image_size_kb = self.get_image_size(img)

        # If it is still above 1024, we reduce the h and w by 10% until we can send it
        while image_size_kb > 1024 and page2.break_thread == False:
            img = self.resize_image(img)
            image_size_kb = self.get_image_size(img)  
        return img
    
    def get_image_size(self, img):
        buffer = BytesIO()
        img.save(buffer, 'jpeg')
        image_size_kb = buffer.tell() / 1024
        return image_size_kb

    def resize_image(self, img):
        w, h = img.size
        new_w = int(w * 0.9)
        new_h = int(h * 0.9)
        resized_img = img.resize((new_w, new_h))
        return resized_img