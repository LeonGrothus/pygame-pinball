import os
import json

class JsonManager:
    """
    This class is used to save and load JSON data to and from a JSON file.

    Attributes:
        json_file: str, the path to the JSON file

    Methods:
        __init__(self, default_path)
        create_file(self) -> bool
        get_path(self) -> str
        save_json(self, data) -> bool
        load_json(self) -> dict
    """

    def __init__(self, default_path) -> None:
        """
        Inits JsonManager with default_path

        Arguments:
            default_path: str, the path to the JSON file
        """

        self.json_file = default_path
        os.makedirs(os.path.dirname(self.json_file), exist_ok=True) # Create the directory if it doesn't exist
        if not os.path.isfile(self.json_file): # Create the file if it doesn't exist
            self.create_file() 
            self.save_json({}) # Save an empty JSON object to the file

    def get_path(self):
        """
        Gets the path to the JSON file

        Returns:
            str: the path to the JSON file
        """
        return os.path.abspath(self.json_file)

    def save_json(self, data) -> bool:
        """
        Saves JSON data to the JSON file

        Arguments:
            data: dict, the data to save

        Returns:
            bool: whether the data was saved successfully
        """

        path = self.get_path() # Get the path to the file
        try:
            with open(path, 'w') as content: # Open the file with write permissions
                json.dump(data, content) # Write the data to the file
            return True 
        except Exception as e: # If an error occurs, print it and return False
            print(e) # Print the error
            return False

    def load_json(self) -> dict:
        """
        Loads JSON data from the JSON file

        Returns:
            dict: the data loaded from the file
        """

        path = self.get_path() # Get the path to the file
        if not os.path.exists(self.json_file): # If the file doesn't exist, create it and return an empty dict
            print("Created new file: " + path) # Print that the file was created
            self.save_json({}) # Save an empty JSON object to the file
            return {} # Return an empty dict

        try:
            with open(self.json_file, 'r') as reader: # Open the file with read permissions
                data = reader.read() # Read the data from the file
                if not data: # If the data is empty, return an empty dict
                    self.save_json({}) # Save an empty JSON object to the file
                    return {} # Return an empty dict
                return json.loads(data) # Return the data loaded from the file
        except Exception as _: # If an error occurs, print it and return None
            print(f"File {path} was not found!") # Print that the file was not found
            return None # type: ignore

    def create_file(self) -> bool:
        """
        Creates the JSON file

        Returns:
            bool: whether the file was created successfully
        """

        try:
            with open(self.json_file, 'w') as f: # Open the file with write permissions
                pass # Do nothing
            return True # Return True
        except Exception as e: # If an error occurs, print it and return False
            print(e) # Print the error
            return False # Return False