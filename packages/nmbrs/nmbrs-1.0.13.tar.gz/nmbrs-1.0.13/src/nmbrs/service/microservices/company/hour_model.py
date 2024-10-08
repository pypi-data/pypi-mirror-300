"""Microservice responsible for hour model related actions on the company level."""

import logging

from zeep import Client
from zeep.helpers import serialize_object

from ..micro_service import MicroService
from ....auth.token_manager import AuthManager
from ....data_classes.company import HourCode
from ....utils.nmbrs_exception_handler import nmbrs_exception_handler
from ....utils.return_list import return_list

logger = logging.getLogger(__name__)


class CompanyHourModelService(MicroService):
    """Microservice responsible for hour model related actions on the company level."""

    def __init__(self, auth_manager: AuthManager, client: Client):
        super().__init__(auth_manager, client)

    @return_list
    @nmbrs_exception_handler(resource="CompanyService:HourModel_GetHourCodes")
    def get_current(self, company_id: int) -> list[HourCode]:
        """
        Get hour codes that belong to a company's hour model.

        For more information, refer to the official documentation:
            [HourModel_GetHourCodes](https://api.nmbrs.nl/soap/v3/CompanyService.asmx?op=HourModel_GetHourCodes)

        Args:
            company_id (int): The ID of the company.

        Returns:
            list[HourCode]: A list of hour code objects.
        """
        hour_codes = self.client.service.HourModel_GetHourCodes(CompanyId=company_id, _soapheaders=self.auth_manager.header)
        return [HourCode(company_id=company_id, data=hour_code) for hour_code in serialize_object(hour_codes)]

    @return_list
    @nmbrs_exception_handler(resource="CompanyService:HourModel2_GetHourCodes")
    def get_current_2(self, company_id: int) -> list[HourCode]:
        """
        Get hour codes that belong to a company's hour model 2.

        For more information, refer to the official documentation:
            [HourModel2_GetHourCodes](https://api.nmbrs.nl/soap/v3/CompanyService.asmx?op=HourModel2_GetHourCodes)

        Args:
            company_id (int): The ID of the company.

        Returns:
            list[HourCode]: A list of hour code objects.
        """
        hour_codes = self.client.service.HourModel2_GetHourCodes(CompanyId=company_id, _soapheaders=self.auth_manager.header)
        return [HourCode(company_id=company_id, data=hour_code) for hour_code in serialize_object(hour_codes)]
