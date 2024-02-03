from PIL import Image
import os
import json

class ImageManager:
    """
    This class is used to save and load JSON data to and from an image file.

    Attributes:
        image_file: str, the path to the image file
        scale_factor: int, the scale factor of the image

    Methods:
        __init__(self, default_path, scale_factor=5)
        create_file(self) -> None
        get_path(self) -> str
        save_json(self, data) -> bool
        load_json(self) -> dict
    """

    def __init__(self, default_path, scale_factor=5) -> None:
        """
        Inits ImageManager with default_path and scale_factor

        Arguments:
            default_path: str, the path to the image file
            scale_factor: int, the scale factor of the image
        """

        self.image_file = default_path
        self.scale_factor = scale_factor
        os.makedirs(os.path.dirname(self.image_file), exist_ok=True) # Create the directory if it doesn't exist
        if not os.path.isfile(self.image_file): # Create the file if it doesn't exist
            self.create_file()
            self.save_json({}) # Save an empty JSON object to the file

    def create_file(self) -> None:
        """
        Creates the image file

        Returns:
            None
        """

        image = Image.new('1', (self.scale_factor, self.scale_factor))  # Create a new black image
        image.save(self.image_file) # Save the image

    def get_path(self) -> str:
        """
        Gets the path to the image file

        Returns:
            str: the path to the image file
        """
        return os.path.abspath(self.image_file)

    def save_json(self, data) -> bool:
        """
        Saves JSON data to the image file

        Arguments:
            data: dict, the JSON data to save

        Returns:
            bool: whether the data was saved successfully
        """
        binary_string = ''.join(format(ord(i), '08b') for i in json.dumps(data)) # Convert the JSON data to a binary string
        binary_string += '00000000'  # Add a null character as the end-of-message marker
        size = int(len(binary_string)**0.5) + 1 # Calculate the size of the image
        image = Image.new('1', (size*self.scale_factor, size*self.scale_factor)) # Create a new black image
        pixels = image.load() # Create the pixel map

        # i is the row, j is the column
        for i in range(size):
            for j in range(size): 
                if i*size + j < len(binary_string): # Check if the end of the binary string has been reached
                    # Set the pixel to 0 or 1 depending on the binary value
                    # Scale the image by self.scale_factor
                    for x in range(self.scale_factor):  
                        for y in range(self.scale_factor): 
                            pixels[i*self.scale_factor + x, j*self.scale_factor + y] = int(binary_string[i*size + j])
                else:
                    break

        try:
            image.save(self.get_path()) # Save the image
            return True # Return True if the image was saved successfully
        except Exception as e:
            print(e) # Print the error
            return False # Return False if the image was not saved successfully

    def load_json(self) -> dict:
        """
        Loads JSON data from the image file

        Returns:
            dict: the JSON data
        """

        image = Image.open(self.get_path()).convert('1') # Open the image and convert it to black and white
        pixels = image.load() # Create the pixel map
        size = image.size[0] // self.scale_factor # Calculate the size of the image

        binary_string = '' # Create an empty binary string
        for i in range(size): # i is the row, j is the column
            for j in range(size): 
                # Convert the pixel to 0 or 1 depending on the pixel value
                binary_value = 0 if pixels[i*self.scale_factor, j*self.scale_factor] == 0 else 1
                binary_string += str(binary_value) # Add the binary value to the binary string

        json_string = '' # Create an empty JSON string
        for i in range(0, len(binary_string), 8): # i is the start index of the substring
            char = chr(int(binary_string[i:i+8], 2)) # Convert the binary string to a character
            if char == '\x00':  # Stop if the end-of-message marker is encountered
                break
            json_string += char # Add the character to the JSON string

        try:
            return json.loads(json_string) # Return the JSON data
        except json.JSONDecodeError:
            return {} # Return an empty JSON object if the JSON data could not be loaded