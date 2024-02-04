from pathlib import Path
from source.api.management.json_manager import JsonManager
from source.api.management.sound_manager import SoundManager
from data.constants import PROJECT_PATH

# Singelton
class OptionsManager:
    """
    Singleton class to represent the options.

    A class to represent the options.

    This class is a singleton and can be accessed by calling Options().

    Attributes:
        asf (float): The application scale factor.
        master_volume (float): The master volume.
        music_volume (float): The music volume.
        sfx_volume (float): The sound effects volume.

    Methods:
        __new__(cls) -> 'Options'
        init(self) -> None
        load(self) -> None
        save(self) -> None
    """

    _instance = None

    def __new__(cls) -> 'OptionsManager':
        """
        Create a new instance of the Options class if it does not exist yet.

        Returns:
            Options: The instance of the Options class.
        """
        if cls._instance is None:
            cls._instance = super(OptionsManager, cls).__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self) -> None:
        """
        Initializes a new instance of the Options class.

        This method loads the options from the JSON file.

        Returns:
            None
        """
        self.sound_manager = SoundManager()
        self.json_manager = JsonManager(PROJECT_PATH  / Path("data/options.json"))
        self.load()

    def load(self) -> None:
        """
        Loads the options from the JSON file.

        Returns:
            None
        """

        data: dict = self.json_manager.load_json() # Load the JSON file
        # ASF = Application Scale Factor
        self.asf = data.get('asf', 1)  # Default to 1 if 'acf' is not in the JSON file
        self.resolution = (666 * self.asf, 1000 * self.asf) # Default to 666x1000 if 'acf' is not in the JSON file

        self.master_volume = data.get('master_volume', 50)  # Default to 50 if 'master_volume' is not in the JSON file
        self.music_volume = data.get('music_volume', 50)  # Default to 50 if 'music_volume' is not in the JSON file
        self.sfx_volume = data.get('sfx_volume', 50)  # Default to 50 if 'sfx_volume' is not in the JSON file
        self.user_name = data.get('user_name', 'Player') # Default to 'Player' if 'user_name' is not in the JSON file
        if(self.user_name == ''):
            self.user_name = 'Player'

    def save(self) -> None:
        """
        Saves the options to the JSON file.

        Returns:
            None
        """

        data: dict = {
            'asf': self.asf,
            'master_volume': self.master_volume,
            'music_volume': self.music_volume,
            'sfx_volume': self.sfx_volume,
            'user_name': self.user_name
        }
        self.sound_manager.update_volume()
        self.resolution = (666 * self.asf, 1000 * self.asf)
        self.json_manager.save_json(data)