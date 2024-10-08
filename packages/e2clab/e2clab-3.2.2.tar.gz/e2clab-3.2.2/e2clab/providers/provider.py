from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple

from enoslib import Networks, Roles

from e2clab.config import InfrastructureConfig
from e2clab.constants import MonitoringType, default
from e2clab.constants.layers_services import (
    CLUSTER,
    ENVIRONMENT,
    ID,
    LAYERS,
    MONITORING_SERVICE_ROLE,
    MONITORING_SVC_PORT,
    NAME,
    PROVENANCE_SERVICE_ROLE,
    PROVENANCE_SVC_PORT,
    QUANTITY,
    ROLES,
    SERVERS,
    SERVICES,
)
from e2clab.log import get_logger

logger = get_logger(__name__, ["PROV"])


class Provider:
    """
    Base class for the provider.
    """

    __metaclass__ = ABCMeta

    # Register for all loaded subclasses of 'Provider'
    _loaded_providers = {}

    def __init__(self, infra_config: InfrastructureConfig, optimization_id: int):
        self.infra_config = infra_config
        self.optimization_id = optimization_id
        self.roles = None
        self.networks = None
        self.monitoring_provider = False
        self.provenance_provider = False
        self.raw_provider = None

    def __init_subclass__(cls, **kwargs) -> None:
        """
        When a subclass of 'Provider' is defined, it is stored in a dict for easy
        programmatic imports and instanciation.
        """
        super().__init_subclass__(**kwargs)
        if cls.__name__ not in cls._loaded_providers.keys():
            cls._loaded_providers[cls.__name__] = cls

    @classmethod
    def get_loaded_providers(cls):
        return cls._loaded_providers

    @abstractmethod
    def init(self) -> Tuple[Roles, Networks]:
        """
        (abstract) Implement the logic of your custom Provider.
        Must return roles and networks.
        """
        pass

    @abstractmethod
    def destroy(self):
        """
        (abstract) Implement the logic to destroy (free)
        the resources of your custom Provider.
        """

    def get_provenance(self) -> dict:
        """Returns provenance extra information

        Returns:
            dict: provenance_extra_info
        """
        _provenance_extra_info = {}
        if self.roles and self.networks and self.provenance_provider:
            ui_address = self.roles[PROVENANCE_SERVICE_ROLE][0].address
            _provenance_extra_info = {
                PROVENANCE_SERVICE_ROLE: {
                    "__address__": f"{ui_address}",
                    "url": f"http://{ui_address}:{PROVENANCE_SVC_PORT}",
                }
            }
        return _provenance_extra_info

    # TODO: test
    def get_monitoring(self) -> dict:
        """Returns monitoring information

        Returns:
            Tuple[str, dict]: monitoring_type, monitoring_extra_info
        """
        _monitoring_extra_info = {}
        _monitoring_type = self.infra_config.get_monitoring_type()
        if None not in (self.roles, self.networks) and self.monitoring_provider:
            if _monitoring_type in (
                MonitoringType.TIG,
                MonitoringType.TPG,
            ):
                ui_address = self.roles[MONITORING_SERVICE_ROLE][0].address
                _monitoring_extra_info = {
                    MONITORING_SERVICE_ROLE: {
                        "__address__": f"{ui_address}",
                        "url": f"http://{ui_address}:{MONITORING_SVC_PORT}",
                    }
                }

        return _monitoring_extra_info

    def is_provenance_provider(self):
        return self.provenance_provider

    def is_monitoring_provider(self):
        return self.monitoring_provider

    def log_roles_networks(self, target_environment):
        logger.debug(f" Roles [{target_environment}] = {self.roles}")
        logger.debug(f" Networks [{target_environment}] = {self.networks}")

    @staticmethod
    def check_service_mapping(service):
        add_cluster = None
        add_servers = None
        if CLUSTER in service:
            add_cluster = service[CLUSTER]
        elif SERVERS in service:
            add_servers = service[SERVERS]
        return add_cluster, add_servers


class ProviderConfig(InfrastructureConfig):
    def __init__(self, data: dict) -> None:
        super().__init__(data, refined=True)

        # dict type validated by schema
        self.env: dict = self.get(ENVIRONMENT, {})
        self.layers: dict = self.get(LAYERS, {})

        self.monitoring_provider: bool = False
        self.provenance_provider: bool = False

    @staticmethod
    def opt_job_id(job_name: str, optimization_id: Optional[int] = None) -> str:
        if optimization_id:
            return f"{job_name}_{optimization_id}"
        else:
            return job_name

    @staticmethod
    def get_service_roles(layer_name: str, service: dict) -> list[str]:
        default_roles = [service[NAME], service[ID], layer_name]
        service_roles = service.get(ROLES, [])
        roles = default_roles + service_roles
        return roles

    @staticmethod
    def get_service_quantity(service: dict):
        return service.get(QUANTITY, default.NODE_QUANTITY)

    @staticmethod
    def check_service_mapping(service: dict) -> Tuple[str, list[str]]:
        add_cluster = service.get(CLUSTER)
        add_servers = None
        if not add_cluster:
            add_servers = service.get(SERVERS)
        return add_cluster, add_servers

    @staticmethod
    def _get_clusters_from_servers(servers: list[str]) -> list[str]:
        """
        In G5k a server is named like: '<cluster>-<index>.<site>.grid5000.fr'.
        """
        clusters = []
        for server in servers:
            cluster_name = server.split("-")[0]
            if cluster_name not in clusters:
                clusters.append(cluster_name)
        return clusters

    def check_cluster(self):
        cluster = self.env.get(CLUSTER)
        for layer in self.layers:
            for service in layer[SERVICES]:
                add_cluster, add_servers = self.check_service_mapping(service)
                if add_cluster is None and add_servers is None and cluster is None:
                    raise Exception(
                        "Fix your 'layers_services.yaml' file. "
                        "Specify a 'CLUSTER' or 'SERVERS' "
                        "for each 'service' or specify "
                        "a default 'CLUSTER' in 'g5k:'."
                    )
