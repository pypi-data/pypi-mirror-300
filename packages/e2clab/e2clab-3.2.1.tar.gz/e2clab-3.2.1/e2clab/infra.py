"""
This file defines all functions and utilities needded to enforce the 'workflow'
of our experiment
"""

import copy
from ipaddress import IPv4Network, IPv6Network
from pathlib import Path
from typing import Optional, Tuple, Type

from enoslib import Dstat, Networks, Roles, TIGMonitoring, TPGMonitoring

import e2clab.constants.default as default
from e2clab.config import InfrastructureConfig
from e2clab.constants import MonitoringType
from e2clab.constants.layers_services import (
    ID,
    MONITORING_NETWORK_ROLE,
    MONITORING_SERVICE_ROLE,
    PROVENANCE_SERVICE_ROLE,
    ROLES_MONITORING,
    ROLES_PROVENANCE,
    SERVICE_PLUGIN_NAME,
)
from e2clab.errors import E2clabError
from e2clab.log import get_logger
from e2clab.providers import Provider, get_available_providers, load_providers
from e2clab.providers.plugins.Iotlab import Iotlab
from e2clab.services import Service, get_available_services, load_services
from e2clab.services.provenance.Provenance import Provenance
from e2clab.utils import load_yaml_file


class Infrastructure:
    """
    Enforce Layers & Services definitions
    a.k.a. Layers & Services manager
    """

    def __init__(self, config: Path, optimization_id: Optional[str] = None) -> None:
        """Create a new experiment architecture

        Args:
            config (Path): Path to 'layers_services.yaml' file
            optimization_id (Optional[str], optional): Optimization id. Defaults to None
        """
        self.logger = get_logger(__name__, ["INFRA"])
        self.config = self._load_config(config)
        self.optimization_id: int = optimization_id

        # TODO: check if we can do without this
        # Registering extra information from services
        self.all_serv_extra_inf = {}

    def _load_config(self, config_path: Path) -> InfrastructureConfig:
        c = load_yaml_file(config_path)
        return InfrastructureConfig(c)

    # User Methods

    def prepare(self) -> None:
        """Prepare infrastructure deployment"""
        self.logger.debug("Preparing infrastructure deployment")
        self.prov_to_load = self.config.get_providers_to_load()
        self.serv_to_load = self.config.get_services_to_load()

        self.logger.debug(f"[AVAILABLE PROVIDERS]: {get_available_providers()}")
        self.logger.debug(f"[PROVIDERS TO LOAD] {self.prov_to_load}")
        self.logger.debug(f"[AVAILABLE SERVICES]: {get_available_services()}")
        self.logger.debug(f"[SERVICES TO LOAD] {self.serv_to_load}")

    def deploy(
        self, artifacts_dir: Path, remote_working_dir: str
    ) -> Tuple[Roles, Networks]:
        """Deploys infrastructure

        Args:
            artifacts_dir (Path): Path to artifacts of the experiment
            remote_working_dir (str): Directory to output monitoring data
                on remote hosts

        Returns:
            Tuple[Roles, Networks]: Roles and Networks associated
                with the infrastructure
        """
        # self.providers = self._load_create_providers()
        loaded_providers = self._load_providers()
        self.providers = self._create_providers(loaded_providers)
        self.roles, self.networks = self._init_providers_merge_resources()

        loaded_services = self._load_services()
        self._create_services(loaded_services)

        # TODO: change this
        self.iotlab_prov = self._get_iotlab_provider()

        # Manage Monitoring service
        self.monitoring_type = self._get_monitoring_provider()
        self.monitoring_svc = self._get_monitoring_service(
            artifacts_dir, remote_working_dir
        )

        self.logger.debug(f"[MONITORING TYPE] {self.monitoring_type}")
        self.logger.debug(f"[MONITORING SVC] {self.monitoring_svc}")

        if self.monitoring_svc:
            self.logger.info("Deploying monitoring service")
            self.monitoring_svc.deploy()
            self.logger.info("Done deploying monitoring service")

        # Manage Provider service
        self.prov_prov = self._get_provenance_provider()
        self.prov_serv = self._get_provenance_service(artifacts_dir)

        self.logger.debug(f"[PROVENANCE PROV] {self.prov_prov}")
        self.logger.debug(f"[PROVENANCE SVC] {self.prov_serv}")

        if self.prov_serv:
            self.logger.debug("Deploying provenance server...")
            self.prov_serv.deploy()
            self.logger.debug("Provenance server deployed")

        self.logger.debug(f"[SERVICE EXTRA INFO] = {self.all_serv_extra_inf}")
        self.logger.debug(f"[ROLES] = {self.roles}")
        self.logger.debug(f"[ALL NETWORKS] = {self.networks}")

        self.logger.info("Infrastructure deployed !")

        return self.roles, self.networks

    def finalize(self, output_dir: Path):
        """Backup and destroy Monitoring and Provenance services

        Args:
            output_dir (Path): Path to output backup data
        """
        # Finalize Monitring service
        if self.monitoring_svc:
            self.logger.info(f"Backing up monitoring data in {output_dir}")
            monitoring_ouptut_dir = output_dir / default.MONITORING_DATA
            self.monitoring_svc.backup(backup_dir=monitoring_ouptut_dir)
            self.logger.info(f"Monitoring data in {monitoring_ouptut_dir}")
            self.monitoring_svc.destroy()
            self.logger.info("Done finalizing monitoring serive")

        # Finalize Provenance service
        if self.prov_serv:
            self.logger.info(f"Backing up provenance data in {output_dir}")
            provenance_output_dir = output_dir / default.PROVENANCE_DATA
            self.logger.info(f"Provenance data in {provenance_output_dir}")
            self.prov_serv.backup(backup_dir=provenance_output_dir)
            self.prov_serv.destroy()
            self.logger.info("Done finalizing provenance service")

        if self.iotlab_prov is not None and self.iotlab_prov.monitoring_provider:
            self.logger.info("Backing up Iotlab monitoring data")
            iot_out_dir = (
                output_dir / default.MONITORING_DATA / default.MONITORING_IOT_DATA
            )
            iot_out_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Iotlab monitoring data in {iot_out_dir}")
            self.iotlab_prov.provider.collect_data_experiment(iot_out_dir)
            self.logger.info("Done backing up Iotlab monitoring data")

    def destroy(self) -> None:
        """Destroys all providers resources"""
        for environment, provider in self.providers.items():
            self.logger.debug(f"[DESTROYING PROVIDER] {environment}")
            provider.destroy()

    # End User Methods

    def _load_providers(self) -> dict[str, Type[Provider]]:
        """
        Loads providers
        """
        # TODO: change this implicit behaviour of the capitalization of environments
        # Maybe change module name to lowercase
        environments = [env.capitalize() for env in self.prov_to_load]
        loaded_providers = load_providers(environments)

        return loaded_providers

    def _create_providers(
        self, loaded_providers: dict[str, Provider]
    ) -> dict[str, Provider]:

        providers = {}
        for environment, provider_class in loaded_providers.items():
            providers[environment] = provider_class(
                infra_config=copy.deepcopy(self.config),
                optimization_id=self.optimization_id,
            )

        return providers

    def _init_providers_merge_resources(self) -> Tuple[Roles, Networks]:
        """Init all resources and merges all of them in a Roles and a Networks object
        Also adds global roles "provider_name"

        Returns:
            Tuple[Roles, Networks]: All resources
        """
        # Inspired by the Providers.init() method from enoslib
        roles = Roles()
        networks = Networks()
        for provider_name, provider in self.providers.items():
            _roles, _networks = provider.init()
            roles.extend(_roles)
            roles[provider_name] = _roles.all()
            networks.extend(_networks)
            networks[provider_name] = _networks.all()
            # if not roles and not networks:
            #     roles.update(_roles)
            #     networks.update(_networks)
            #     continue
            # self._merge_dict(roles, _roles)
            # self._merge_dict(networks, _networks)
        return roles, networks

    # @staticmethod
    # def _merge_dict(collection: RolesDict, provider_collection: RolesDict) -> None:
    #     for key in provider_collection.keys():
    #         if key in collection.keys():
    #             collection[key] = set(collection[key]).union(
    #                 set(provider_collection[key])
    #             )
    #         else:
    #             collection[key] = provider_collection[key]

    def _load_services(self) -> dict[str, Service]:
        """Loads needed services"""
        loaded_services = load_services(self.serv_to_load)
        return loaded_services

    def _create_services(self, loaded_services: dict[str, Service]):
        """
        Loads services from the infrastructure configuration and deploys them
        """
        for service in self.config.iterate_services():
            service_name = service[SERVICE_PLUGIN_NAME]
            # Get class definition and instantiate
            try:
                class_service = loaded_services[service_name]
            except KeyError:
                self.logger.error(f"Failed importing service: {service_name}")
                raise E2clabError
            # Create service instance
            inst_service: Service = class_service(
                hosts=self.roles[service[ID]],
                service_metadata=service,
            )
            # Deploy
            service_extra_info, service_roles = inst_service._init()
            self.all_serv_extra_inf.update(service_extra_info)
            # TODO: This does nothing ?
            service["metadata"] = service_extra_info
            self.roles.update(service_roles)

    def _get_iotlab_provider(self) -> Optional[Iotlab]:
        return self.providers.get("Iotlab", None)

    def _get_monitoring_provider(self) -> Optional[MonitoringType]:
        for provider in self.providers.values():
            if provider.is_monitoring_provider():
                # Updating the extra info with the monitoring data
                _monitoring_extra_info = provider.get_monitoring()
                self.all_serv_extra_inf.update(_monitoring_extra_info)
        return self.config.get_monitoring_type()

    def _get_monitoring_service(self, artifacts_path: Path, remote_working_dir: str):
        monitor = None

        filtered_nets = self._get_nets(self.networks, IPv6Network)
        if not filtered_nets:
            filtered_nets = self._get_nets(self.networks, IPv4Network)

        if MONITORING_NETWORK_ROLE in self.networks.keys():
            monitor_networks = self.networks[MONITORING_NETWORK_ROLE]
        else:
            monitor_networks = filtered_nets

        nodes_to_monitor = self.roles[ROLES_MONITORING]

        if self.monitoring_type == MonitoringType.TIG:
            agent_conf = self._get_monitoring_agent_conf(artifacts_path)

            self.logger.debug(f"[MONITORING AGENT CONf] {agent_conf}")

            monitor = TIGMonitoring(
                collector=self.roles[MONITORING_SERVICE_ROLE][0],
                ui=self.roles[MONITORING_SERVICE_ROLE][0],
                agent=nodes_to_monitor,
                networks=monitor_networks,
                agent_conf=agent_conf,
                remote_working_dir=remote_working_dir,
            )
        elif self.monitoring_type == MonitoringType.TPG:
            monitor = TPGMonitoring(
                collector=self.roles[MONITORING_SERVICE_ROLE][0],
                ui=self.roles[MONITORING_SERVICE_ROLE][0],
                agent=nodes_to_monitor,
                networks=monitor_networks,
                remote_working_dir=remote_working_dir,
            )
        elif self.monitoring_type == MonitoringType.DSTAT:
            dstat_opt = self.config.get_dstat_options()
            monitor = Dstat(nodes=nodes_to_monitor, options=dstat_opt)
        return monitor

    def _get_monitoring_agent_conf(self, artifacts_path: Path):
        agent_conf = None
        agent_conf_file_name = self.config.get_monitoring_agent_conf()
        if agent_conf_file_name:
            agent_conf_file = artifacts_path / agent_conf_file_name
            if agent_conf_file.exists():
                agent_conf = agent_conf_file
        return agent_conf

    def _get_nets(self, networks, net_type):
        """Aux method to filter networs from roles"""
        return [
            n
            for net_list in networks.values()
            for n in net_list
            if isinstance(n.network, net_type)
        ]

    def _get_provenance_provider(self) -> Optional[Provider]:
        prov_prov = None
        for prov_name, provider in self.providers.items():
            if provider.provenance_provider and not prov_prov:
                self.logger.debug(f"Provenance provider: {prov_name}")
                prov_prov = provider
        if not prov_prov:
            self.logger.debug("No provenance provider found")
        return prov_prov

    def _get_provenance_service(self, artifacts_dir: Path) -> Provenance:

        if not self.prov_prov:
            self.logger.debug("No provenance provider to deploy")
            return None
        dataflow_file_spec = self.config.get_provenance_dataflow_spec()
        dataflow_spec_file_path = str(artifacts_dir / dataflow_file_spec)
        parallelism = self.config.get_provenance_parallelism()
        e2clab_provenance = Provenance(
            host=self.roles[PROVENANCE_SERVICE_ROLE][0],
            agent=self.roles[ROLES_PROVENANCE],
            dataflow_spec=dataflow_spec_file_path,
            parallelism=parallelism,
        )
        return e2clab_provenance
