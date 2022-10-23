from os.path import dirname as up
import os
from configparser import ConfigParser
from itertools import chain

from kindgen import templates

class ConfigCreate:
    def __init__(self, tpl: templates.Templates) -> None:
        self._tpl = tpl

    def create_content(self) -> str:
        parser = ConfigParser()

        # https://stackoverflow.com/questions/2885190/using-configparser-to-read-a-file-without-section-name
        with open(self._tpl.get_cluster_config_file()) as stream:
            stream = chain(("[default]",), stream)
            parser.read_file(stream)

        cluster_name = parser.get("default", "cluster_name")
        print(f"cluster_name: {cluster_name}")

        internal_registry = parser.getboolean("default", "internal_registry")
        print(f"internal_registry: {internal_registry}")

        worker_nodes = parser.getint("default", "worker_nodes")
        print(f"worker_nodes: {worker_nodes}")

        data_dir = parser.get("default", "data_dir")
        print(f"data_dir: {data_dir}")


        result = ""
        try:
            #self._tpl.copy_file("cluster-configuration", "config")
            a = 1
            a = a +1
        except Exception as err:
            result = str(err)
        return result
