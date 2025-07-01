from PIL import Image


class Image_Loader:
    def __init__(self, path):
        self.path = path

    def load(self):
        image = Image.open(self.path).convert("RGBA")

        width, height = image.size
        pixel_data = list(image.getdata())

        image_data = bytes([value for pixel in pixel_data for value in pixel])

        return (width, height, 4, image_data)
