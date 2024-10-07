from pathlib import Path


class ParseFileInfo:
    def get_type(self, path: str) -> str:
        type_file = Path(path).suffixes
        if type_file:
            return "".join(type_file)
        return ".json"
