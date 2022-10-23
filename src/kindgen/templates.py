from pathlib import Path
from os.path import dirname as up
import os

class Templates:
    def __init__(self) -> None:
        self._tpl_path = self._detect_template_path()

    def _detect_template_path(self) -> str:
        file_path = os.path.realpath(__file__)
        file_dir = os.path.dirname(file_path)
        upper = os.path.dirname(os.path.dirname(file_dir)) # 2 level up
        tpl_dir = os.path.join(upper, "kindgen_templates")
        return tpl_dir

    def get_tpl_path(self) -> str:
        return self._tpl_path