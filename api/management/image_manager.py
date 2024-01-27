from PIL import Image
import os
import json

class ImageManager:
    def __init__(self, default_path, scale_factor=5) -> None:
        self.image_file = default_path
        self.scale_factor = scale_factor
        os.makedirs(os.path.dirname(self.image_file), exist_ok=True)
        if not os.path.isfile(self.image_file):
            self.create_file()
            self.save_json({})

    def create_file(self) -> None:
        image = Image.new('1', (self.scale_factor, self.scale_factor))  # Create a new black image
        image.save(self.image_file)

    def get_path(self) -> str:
        return os.path.abspath(self.image_file)

    def save_json(self, data) -> bool:
        binary_string = ''.join(format(ord(i), '08b') for i in json.dumps(data))
        binary_string += '00000000'  # Add a null character as the end-of-message marker
        size = int(len(binary_string)**0.5) + 1
        image = Image.new('1', (size*self.scale_factor, size*self.scale_factor))
        pixels = image.load()

        for i in range(size):
            for j in range(size):
                if i*size + j < len(binary_string):
                    for x in range(self.scale_factor):
                        for y in range(self.scale_factor):
                            pixels[i*self.scale_factor + x, j*self.scale_factor + y] = int(binary_string[i*size + j])
                else:
                    break

        try:
            image.save(self.get_path())
            return True
        except Exception as e:
            print(e)
            return False

    def load_json(self) -> dict:
        image = Image.open(self.get_path()).convert('1')
        pixels = image.load()
        size = image.size[0] // self.scale_factor

        binary_string = ''
        for i in range(size):
            for j in range(size):
                binary_value = 0 if pixels[i*self.scale_factor, j*self.scale_factor] == 0 else 1
                binary_string += str(binary_value)

        json_string = ''
        for i in range(0, len(binary_string), 8):
            char = chr(int(binary_string[i:i+8], 2))
            if char == '\x00':  # Stop if the end-of-message marker is encountered
                break
            json_string += char

        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            return {}