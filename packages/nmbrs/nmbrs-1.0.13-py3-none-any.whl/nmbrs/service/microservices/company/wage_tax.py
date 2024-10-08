"""Microservice responsible for managing wage tax-related actions on the company level."""

import logging

from zeep import Client
from zeep.helpers import serialize_object

from ....auth.token_manager import AuthManager
from ....data_classes.company import WageTax, WageTaxXML
from ..micro_service import MicroService
from ....utils.nmbrs_exception_handler import nmbrs_exception_handler
from ....utils.return_list import return_list

logger = logging.getLogger(__name__)


class CompanyWageTaxService(MicroService):
    """Microservice responsible for managing wage tax-related actions on the company level."""

    def __init__(self, auth_manager: AuthManager, client: Client):
        super().__init__(auth_manager, client)

    @return_list
    @nmbrs_exception_handler(resource="CompanyService:WageTax_GetList")
    def get_all_wagetax(self, company_id: int, year: int) -> list[WageTax]:
        """
        Retrieve all wage taxes for a specific company and year.

        For more information, refer to the official documentation:
            [WageTax_GetList](https://api.nmbrs.nl/soap/v3/CompanyService.asmx?op=WageTax_GetList)

        Args:
            company_id (int): The ID of the company.
            year (int): The year for which wage taxes are retrieved.

        Returns:
            list[WageTax]: A list of WageTax objects for the specified company and year.
        """
        wage_taxes = self.client.service.WageTax_GetList(CompanyId=company_id, intYear=year, _soapheaders=self.auth_manager.header)
        wage_taxes = [WageTax(company_id=company_id, data=wage_tax) for wage_tax in serialize_object(wage_taxes)]
        return wage_taxes

    @nmbrs_exception_handler(resource="CompanyService:WageTax_GetXML")
    def get_wagetax_details(self, company_id: int, loonaangifte_id: int) -> WageTaxXML:
        """
        Retrieve wage tax details for a specific company and loonaangifte ID.

        For more information, refer to the official documentation:
            [WageTax_GetXML](https://api.nmbrs.nl/soap/v3/CompanyService.asmx?op=WageTax_GetXML)

        Args:
            company_id (int): The ID of the company.
            loonaangifte_id (int): The loonaangifte ID.

        Returns:
            WageTaxXML: An wage tax object detailing the specified company and loonaangifte ID.
        """
        wage_tax_details = self.client.service.WageTax_GetXML(
            CompanyId=company_id,
            LoonaangifteID=loonaangifte_id,
            _soapheaders=self.auth_manager.header,
        )
        wage_tax_details = WageTaxXML(wage_tax_details)
        return wage_tax_details

    @nmbrs_exception_handler(resource="CompanyService:WageTax_SetSentExternal")
    def set_send_as_external(self, company_id: int, loonaangifte_id: int) -> bool:
        """
        Set the wage tax status to Sent as External.

        For more information, refer to the official documentation:
            [WageTax_SetSentExternal](https://api.nmbrs.nl/soap/v3/CompanyService.asmx?op=WageTax_SetSentExternal)

        Args:
            company_id (int): The ID of the company.
            loonaangifte_id (int): The loonaangifte ID.

        Returns:
            bool: A boolean indicating if the wage tax was send externally.
        """
        response = self.client.service.WageTax_SetSentExternal(
            CompanyId=company_id,
            LoonaangifteID=loonaangifte_id,
            _soapheaders=self.auth_manager.header,
        )
        return response
