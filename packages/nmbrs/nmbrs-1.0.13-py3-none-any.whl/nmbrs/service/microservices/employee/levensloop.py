"""Microservice responsible for levens loop related actions on the employee level."""

import logging

from zeep import Client

from ..micro_service import MicroService
from ....auth.token_manager import AuthManager
from ....utils.nmbrs_exception_handler import nmbrs_exception_handler

logger = logging.getLogger(__name__)


class EmployeeLevensLoopService(MicroService):
    """Microservice responsible for levens loop related actions on the employee level."""

    def __init__(self, auth_manager: AuthManager, client: Client):
        super().__init__(auth_manager, client)

    @nmbrs_exception_handler(resource="EmployeeService:Levensloop_Get")
    def get(self):
        """
        Get the active levensloop for given period.

        For more information, refer to the official documentation:
            [Levensloop_Get](https://api.nmbrs.nl/soap/v3/EmployeeService.asmx?op=Levensloop_Get)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="EmployeeService:Levensloop_Insert")
    def post(self):
        """
        Start levensloop for given date and amount.

        For more information, refer to the official documentation:
            [Levensloop_Insert](https://api.nmbrs.nl/soap/v3/EmployeeService.asmx?op=Levensloop_Insert)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="EmployeeService:Levensloop_Delete")
    def delete(self):
        """
        Delete the given levensloop. This action can not be undone.

        For more information, refer to the official documentation:
            [Levensloop_Delete](https://api.nmbrs.nl/soap/v3/EmployeeService.asmx?op=Levensloop_Delete)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="EmployeeService:Levensloop_Stop")
    def stop(self):
        """
        Stop the active levensloop for given date.

        For more information, refer to the official documentation:
            [Levensloop_Stop](https://api.nmbrs.nl/soap/v3/EmployeeService.asmx?op=Levensloop_Stop)
        """
        raise NotImplementedError()  # pragma: no cover
