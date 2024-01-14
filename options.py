from pathlib import Path
from api.management.json_manager import JsonManager
from constants import PROJECT_PATH

# Singelton
class Options:
    """
    A class to represent the options.

    This class is a singleton and can be accessed by calling Options().

    Attributes:
        asf (float): The application scale factor.
        master_volume (float): The master volume.
        music_volume (float): The music volume.
        sfx_volume (float): The sound effects volume.
    """

    _instance = None

    def __new__(cls) -> 'Options':
        """
        Create a new instance of the Options class if it does not exist yet.

        Returns:
            Options: The instance of the Options class.
        """
        if cls._instance is None:
            cls._instance = super(Options, cls).__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self) -> None:
        """
        Initializes a new instance of the Options class.

        This method loads the options from the JSON file.

        Returns:
            None
        """
        self.json_manager = JsonManager(PROJECT_PATH  / Path("options.json"))
        self.load_entries()

    def load_entries(self) -> None:
        """
        Loads the entries from the JSON file.

        Returns:
            None
        """

        data: dict = self.json_manager.load_json()
        # ASF = Application Scale Factor
        self.asf = data.get('acf', 1)  # Default to 1 if 'acf' is not in the JSON file
        self.resolution = (666 * self.asf, 1000 * self.asf)

        self.master_volume = data.get('master_volume', 50)  # Default to 50 if 'master_volume' is not in the JSON file
        self.music_volume = data.get('music_volume', 50)  # Default to 50 if 'music_volume' is not in the JSON file
        self.sfx_volume = data.get('sfx_volume', 50)  # Default to 50 if 'sfx_volume' is not in the JSON file

    def save_entries(self) -> None:
        """
        Saves the entries to the JSON file.

        Returns:
            None
        """

        data: dict = {
            'acf': self.asf,
            'master_volume': self.master_volume,
            'music_volume': self.music_volume,
            'sfx_volume': self.sfx_volume
        }
        self.resolution = (666 * self.asf, 1000 * self.asf)
        self.json_manager.save_json(data)