from pathlib import Path
from os.path import dirname as up
import os
import shutil

class Templates:
    def __init__(self) -> None:
        self._tpl_path = self._detect_template_path()
        self._dest_dir = None

    def _detect_template_path(self) -> str:
        file_path = os.path.realpath(__file__)
        file_dir = os.path.dirname(file_path)
        upper = os.path.dirname(os.path.dirname(file_dir)) # 2 level up
        tpl_dir = os.path.join(upper, "kindgen_templates")
        return tpl_dir

    def get_cluster_config_file(self) -> str:
        cfg = os.path.join(self._dest_dir, 'config')
        cfg = os.path.join(cfg, 'cluster-configuration')
        return cfg

    def has_valid_dest_dir(self, dest_dir: Path) -> str:
        self._dest_dir = dest_dir
        file_path = os.path.realpath(self._dest_dir)

        if not os.path.exists(file_path):
            return f"error: directory '{file_path}' does not exists."

        if not os.path.exists(self.get_cluster_config_file()):
            return f"error: directory '{file_path}' has no file 'config/cluster-configuration'."

        return ""

    def prepare_dest_dir(self, dest_dir: Path) -> str:
        self._dest_dir = dest_dir
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

    def copy_file(self, tpl_filename: str, dest_sub_dir: str) -> None:
        dest_file_path = os.path.join(self._dest_dir, dest_sub_dir)

        if not os.path.exists(dest_file_path):
            os.makedirs(dest_file_path)

        src_file = os.path.join(self._tpl_path, tpl_filename)
        dest_file = os.path.join(dest_file_path, tpl_filename)

        shutil.copyfile(src_file, dest_file)