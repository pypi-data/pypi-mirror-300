# pylint: disable=line-too-long
"""Microservice responsible for spaarloon related actions on the employee level."""
import logging

from zeep import Client

from ..micro_service import MicroService
from ....auth.token_manager import AuthManager
from ....utils.nmbrs_exception_handler import nmbrs_exception_handler

logger = logging.getLogger(__name__)


class EmployeeSpaarloonService(MicroService):
    """Microservice responsible for spaarloon related actions on the employee level."""

    def __init__(self, auth_manager: AuthManager, client: Client):
        super().__init__(auth_manager, client)

    @nmbrs_exception_handler(resource="EmployeeService:Spaarloon_Get")
    def get(self):
        """
        Get the active spaarloon for given period.

        For more information, refer to the official documentation:
            [Spaarloon_Get](https://api.nmbrs.nl/soap/v3/EmployeeService.asmx?op=Spaarloon_Get)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="EmployeeService:Spaarloon_GetList")
    def get_all(self):
        """
        Get a list of spaarloonvalues.

        For more information, refer to the official documentation:
            [Spaarloon_GetList](https://api.nmbrs.nl/soap/v3/EmployeeService.asmx?op=Spaarloon_GetList)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="EmployeeService:Spaarloon_Insert")
    def post(self):
        """
        Start spaarloon for given date and amount. If the startdate is before the company's current period, unprotected mode flag is required.

        For more information, refer to the official documentation:
            [Spaarloon_Insert](https://api.nmbrs.nl/soap/v3/EmployeeService.asmx?op=Spaarloon_Insert)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="EmployeeService:Spaarloon_Delete")
    def delete(self):
        """
        Delete the given spaarloon from the system. This action can not be undone.

        For more information, refer to the official documentation:
            [Spaarloon_Delete](https://api.nmbrs.nl/soap/v3/EmployeeService.asmx?op=Spaarloon_Delete)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="EmployeeService:Spaarloon_Stop")
    def stop(self):
        """
        Stop the active spaarloon for given date.

        For more information, refer to the official documentation:
            [Spaarloon_Stop](https://api.nmbrs.nl/soap/v3/EmployeeService.asmx?op=Spaarloon_Stop)
        """
        raise NotImplementedError()  # pragma: no cover
