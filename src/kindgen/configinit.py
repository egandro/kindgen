from pathlib import Path
from os.path import dirname as up
import os
import shutil

class ConfigInit:
    def __init__(self, tpl_path: Path, dest_dir: Path) -> None:
        self._tpl_path = tpl_path
        self._dest_dir = dest_dir

    def prepare_dest_dir(self) -> str:
        file_path = os.path.realpath(self._dest_dir)

        if os.path.exists(file_path):
            return f"error: directory '{file_path}' already exists."

        result=""
        try:
            os.makedirs(file_path)
            # this is now the main path
            self._dest_dir = file_path
        except Exception as err:
            result = str(err)
        return result

    def create_content(self) -> str:
        result = ""
        try:
            self._copy_file("cluster-configuration", "config")
        except Exception as err:
            result = str(err)
        return result

    def _copy_file(self, tpl_filename: str, dest_sub_dir: str) -> None:
        dest_file_path = os.path.join(self._dest_dir, dest_sub_dir)
        if not os.path.exists(dest_file_path):
            os.makedirs(dest_file_path)

        src_file = os.path.join(self._tpl_path, tpl_filename)
        dest_file = os.path.join(dest_file_path, tpl_filename)

        shutil.copyfile(src_file, dest_file)