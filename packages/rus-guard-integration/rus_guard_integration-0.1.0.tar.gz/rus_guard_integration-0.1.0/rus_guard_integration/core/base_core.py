import ssl
from abc import ABC
from typing import Callable

import urllib3
from loguru import logger
from requests import Session
from zeep import Client
from zeep.transports import Transport
from zeep.wsse.username import UsernameToken

from rus_guard_integration.dto.config import RusGuardConfig
from rus_guard_integration.dto.acs_methods import _RusGuardMethod


class BaseRusGuardCore(ABC):

    def __init__(self, core_config: RusGuardConfig):
        self.client = None
        self.core_config = core_config
        self.service_config = None

    async def init(self):
        urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
        session = Session()
        session.verify = False
        transport = Transport(session=session)
        self.client = Client(f'http://{self.core_config.sever_ip}/LNetworkServer/LNetworkService.svc?wsdl',
                             wsse=UsernameToken(self.core_config.rus_guard_login, self.core_config.rus_guard_password),
                             transport=transport)
        self.service_config = self.client.bind('LNetworkService', 'BasicHttpBinding_ILNetworkConfigurationService')

    async def _call_methods_get(self, method_name: _RusGuardMethod) -> Callable:
        return getattr(self.client.service, method_name)

    async def _read_all(self, method_name: _RusGuardMethod):
        result = None
        logger.info(f"_RusGuardMethod: {method_name}")
        try:
            result = (await self._call_methods_get(method_name))()
        except Exception as e:
            logger.error(f"RusGuard error _read_all\n Method: {method_name},\n args: {args}\n Error: {e} ")
        return result

    async def _read(self, method_name: _RusGuardMethod, entity_id: str):
        result = None
        logger.info(f"_RusGuardMethod: {method_name}, Entity_ID: {entity_id}")
        try:
            result = (await self._call_methods_get(method_name))(entity_id)
        except Exception as e:
            logger.error(f"RusGuard error _read\n Method: {method_name},\n args: {args}\n Error: {e} ")
        return result

    async def _create_or_update_or_delete(self, method_name: _RusGuardMethod, *args):
        result = None
        logger.info(f"_RusGuardMethod: {method_name}, args: {args}")
        try:
            result = getattr(self.service_config, method_name)(*args)
        except Exception as e:
            logger.error(f"RusGuard error _create_or_update_or_delete\n Method: {method_name},\n args: {args}\n Error: {e} ")
        return result

    async def read(self, method_name: _RusGuardMethod, entity_id: str):
        return await self._read(method_name=method_name, entity_id=entity_id)

    async def read_all(self, method_name: _RusGuardMethod):
        return await self._read_all(method_name=method_name)

    async def create(self, method_name: _RusGuardMethod, *args):
        return await self._create_or_update_or_delete(method_name=method_name, *args)

    async def update(self, method_name: _RusGuardMethod, *args):
        return await self._create_or_update_or_delete(method_name=method_name, *args)

    async def delete(self, method_name: _RusGuardMethod, *args):
        return await self._create_or_update_or_delete(method_name=method_name, *args)
