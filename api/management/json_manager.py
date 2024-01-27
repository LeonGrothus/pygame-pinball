import os
import json

class JsonManager:
    def __init__(self, default_path) -> None:
        self.json_file = default_path
        os.makedirs(os.path.dirname(self.json_file), exist_ok=True)
        if not os.path.isfile(self.json_file):
            self.create_file()
            self.save_json({})

    def get_path(self):
        return os.path.abspath(self.json_file)

    def save_json(self, data) -> bool:
        path = self.get_path()
        try:
            with open(path, 'w') as content:
                json.dump(data, content)
            return True
        except Exception as e:
            print(e)
            return False

    def load_json(self) -> dict:
        path = self.get_path()
        if not os.path.exists(self.json_file):
            print("Created new file: " + path)
            self.save_json({})
            return {}

        try:
            with open(self.json_file, 'r') as reader:
                data = reader.read()
                if not data:
                    self.save_json({})
                    return {}
                print(data)
                return json.loads(data)
        except Exception as e:
            print(f"File {path} was not found!")
            return None # type: ignore

    def create_file(self) -> bool:
        try:
            with open(self.json_file, 'w') as f:
                pass
            return True
        except Exception as e:
            print(e)
            return False