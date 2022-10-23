from os.path import dirname as up
import os
from configparser import ConfigParser
from itertools import chain

from kindgen import templates

class ConfigCreate:
    def __init__(self, tpl: templates.Templates) -> None:
        self._tpl = tpl
        self._cfg = ClusterConfig(tpl)

    def create_content(self) -> str:
        result = ""
        try:
            self._cfg.parse()

            cluster_name = self._cfg.cluster_name()
            print(f"cluster_name: {cluster_name}")

            internal_registry = self._cfg.internal_registry()
            print(f"internal_registry: {internal_registry}")

            external_registry = self._cfg.external_registry()
            print(f"external_registry: {external_registry}")

            worker_nodes = self._cfg.worker_nodes()
            print(f"worker_nodes: {worker_nodes}")

            mountpoints = self._cfg.mountpoints()
            print(f"mountpoints: {mountpoints}")

            data_dir = self._cfg.data_dir()
            print(f"data_dir: {data_dir}")

            #self._tpl.copy_file("cluster-configuration", "config")
            a = 1
            a = a +1
        except Exception as err:
            result = str(err)
        return result


class ClusterConfig:
    def __init__(self, tpl: templates.Templates) -> None:
        self._tpl = tpl
        self._cfg = ClusterConfigRaw(tpl)

    def parse(self) -> None:
        self._cfg.parse()

    def cluster_name(self) -> str:
        return self._cfg.get("cluster_name", "kind")

    def internal_registry(self) -> bool:
        return self._cfg.getboolean("internal_registry", True)

    def external_registry(self) -> bool:
        return self._cfg.getboolean("external_registry", False)

    def worker_nodes(self) -> int:
        return self._cfg.getint("worker_nodes", 0)

    def mountpoints(self) -> bool:
        return self._cfg.getboolean("mountpoints", True)

    def data_dir(self) -> str:
        data_dir = self._cfg.get("data_dir", "")
        if not data_dir:
            data_dir = os.getcwd()
            data_dir = os.path.join(data_dir, "data")
        return data_dir

class ClusterConfigRaw:
    def __init__(self, tpl: templates.Templates) -> None:
        self._tpl = tpl

    def parse(self) -> None:
        self._parser = ConfigParser()

        # https://stackoverflow.com/questions/2885190/using-configparser-to-read-a-file-without-section-name
        with open(self._tpl.get_cluster_config_file()) as stream:
            stream = chain(("[dummy_section]",), stream)
            self._parser.read_file(stream)

    def get(self, key: str, default: str = "") -> str:
        try:
            res = self._parser.get("dummy_section", key)
            if not res:
                res = default
            return res
        except Exception:
            return default

    def getboolean(self, key: str, default: bool = False) -> bool:
        try:
            return self._parser.getboolean("dummy_section", key)
        except Exception:
            return default

    def getint(self, key: str, default: int = 0) -> int:
        try:
            return self._parser.getint("dummy_section", key)
        except Exception:
            return default

    def getfloat(self, key: str, default: float = 0) -> float:
        try:
            return self._parser.getfloat("dummy_section", key)
        except Exception:
            return default
