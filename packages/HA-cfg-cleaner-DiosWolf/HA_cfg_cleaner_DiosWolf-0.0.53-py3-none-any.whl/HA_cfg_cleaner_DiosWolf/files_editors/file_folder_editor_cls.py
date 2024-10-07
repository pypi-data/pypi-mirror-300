import os
import shutil


class FileFoldersEditor:
    def delete_objects(self, path: str):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

    def clean_folders(self, folder_path: str):
        for files in os.scandir(folder_path):
            if files.is_dir():
                shutil.rmtree(files.path)
            elif files.is_file():
                os.remove(files)

    def clean_files(self, path: str):
        with open(path, "wb") as _:
            pass
