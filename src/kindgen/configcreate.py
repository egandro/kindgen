from configparser import ConfigParser
from itertools import chain
import os
from subprocess import check_output

from kindgen import templates

class ConfigCreate:
    def __init__(self, tpl: templates.Templates) -> None:
        self._tpl = tpl
        self._cfg = ClusterConfig(tpl)

    def create_content(self) -> str:
        result = ""
        try:
            cfg_data = self._get_cfg_data()
            self._render_tpl_configs(cfg_data)
            self._copy_configs()

        except Exception as err:
            result = str(err)
        return result

    def _render_tpl_configs(self, cfg_data: dict[str, str]) -> None:
        self._tpl.render_template(cfg_data, "config.j2.yaml", "config", "config.yaml")
        self._tpl.render_template(cfg_data, "Makefile.j2", "", "Makefile")
        return None

    def _copy_configs(self) -> None:
        #self._tpl.copy_file("cluster-configuration", "config")
        return None

    def _get_cfg_data(self) -> dict[str, str]:
        self._cfg.parse(self._tpl.get_dest_dir())

        data = {}

        data["cluster_name"] = self._cfg.cluster_name()
        data["internal_registry"] = self._cfg.internal_registry()
        data["internal_registry_name"] = self._cfg.internal_registry_name()
        data["internal_registry_port"] = self._cfg.internal_registry_port()
        data["external_registry"] = self._cfg.external_registry()
        data["ingress"] = self._cfg.ingress()
        data["loadbalancer"] = self._cfg.loadbalancer()
        data["public_http_port"] = self._cfg.public_http_port()
        data["public_https_port"] = self._cfg.public_https_port()
        data["worker_nodes"] = self._cfg.worker_nodes()
        data["mountpoints"] = self._cfg.mountpoints()
        data["data_dir"] = self._cfg.data_dir()
        data["api_server_address"] = self._cfg.api_server_address()

        return data


class ClusterConfig:
    def __init__(self, tpl: templates.Templates) -> None:
        self._tpl = tpl
        self._cfg = ClusterConfigRaw(tpl)

    def parse(self, dest_dir:str) -> None:
        self._cfg.parse()
        self._dest_dir = dest_dir

    def cluster_name(self) -> str:
        return self._cfg.get("cluster_name", "kind")

    def internal_registry(self) -> bool:
        return self._cfg.getboolean("internal_registry", True)

    def internal_registry_name(self) -> str:
        return self._cfg.get("internal_registry_name", "kind-registry")

    def internal_registry_port(self) -> int:
        return self._cfg.getint("internal_registry_port", 5001)

    def external_registry(self) -> bool:
        return self._cfg.getboolean("external_registry", False)

    def ingress(self) -> bool:
        return self._cfg.getboolean("ingress", False)

    def loadbalancer(self) -> bool:
        return self._cfg.getboolean("loadbalancer", False)

    def public_http_port(self) -> int:
        return self._cfg.getint("public_http_port", 8000)

    def public_https_port(self) -> int:
        return self._cfg.getint("public_https_port", 8443)

    def worker_nodes(self) -> int:
        return self._cfg.getint("worker_nodes", 0)

    def mountpoints(self) -> bool:
        return self._cfg.getboolean("mountpoints", True)

    def data_dir(self) -> str:
        data_dir = self._cfg.get("data_dir", "")
        if not data_dir:
            data_dir = os.path.join(os.path.realpath(self._dest_dir), "data")
        return data_dir

    def api_server_address(self) -> str:
        api_server_address = self._cfg.get("api_server_address", "")
        if not api_server_address:
            ip = self._get_ip(ignore_local_ips=False)
            api_server_address = ip
        return api_server_address

    # https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-from-a-nic-network-interface-controller-in-python
    def _get_ip(self, ip_addr_proto="ipv4", ignore_local_ips=True):
        ip = ""
        try:
            # bash style of getting a "cool" ip address
            # will fail on macOS / Windows / and a lot of Linux versions - help is welcome!
            # hack works for me... go edit your files not this code...
            ips = check_output(['hostname', '--all-ip-addresses'])
            ips = ips.decode('ascii')
            ip_arr = ips.split()
            ip = ip_arr[0]
        except Exception:
            # bad luck...
            pass
        return ip


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
