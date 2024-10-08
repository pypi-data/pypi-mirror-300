"""Microservice responsible for address-related actions on the company level."""

import logging
from zeep import Client
from zeep.helpers import serialize_object

from ....auth.token_manager import AuthManager
from ....data_classes.company import Address
from ....utils.nmbrs_exception_handler import nmbrs_exception_handler
from ..micro_service import MicroService

logger = logging.getLogger(__name__)


class CompanyAddressService(MicroService):
    """Microservice responsible for address-related actions on the company level."""

    def __init__(self, auth_manager: AuthManager, client: Client):
        super().__init__(auth_manager, client)

    @nmbrs_exception_handler(resource="CompanyService:Address_GetCurrent")
    def get_current(self, company_id: int) -> Address | None:
        """
        Get the current address of the company.

        For more information, refer to the official documentation:
            [Address_GetCurrent](https://api.nmbrs.nl/soap/v3/CompanyService.asmx?op=Address_GetCurrent)

        Args:
            company_id (int): The ID of the company.

        Returns:
            Address | None: An Address object if found, otherwise None.
        """
        address = self.client.service.Address_GetCurrent(CompanyId=company_id, _soapheaders=self.auth_manager.header)
        if address is None:
            logger.debug("No address found, for company, ID: %s.", company_id)
            return None
        return Address(company_id=company_id, data=serialize_object(address))

    @nmbrs_exception_handler(resource="CompanyService:Address_Insert")
    def post(
        self,
        company_id: int,
        address_id: int,
        default: bool,
        street: str,
        house_number: str,
        house_number_addon: str,
        postal_code: str,
        city: str,
        state_province: str,
        country_iso_code: str,
    ) -> int:
        """
        Insert a new address for the company.

        For more information, refer to the official documentation:
            [Address_Insert](https://api.nmbrs.nl/soap/v3/CompanyService.asmx?op=Address_Insert)

        Args:
            company_id (int): The ID of the company.
            address_id (int): The ID of the address.
            default (bool): Flag indicating if the address is default.
            street (str): Street name.
            house_number (str): House number.
            house_number_addon (str): House number addition (if any).
            postal_code (str): Postal code.
            city (str): City name.
            state_province (str): State or province name.
            country_iso_code (str): ISO code of the country.

        Returns:
            int: ID of the inserted address.
        """
        data = {
            "CompanyId": company_id,
            "Address": {
                "Id": address_id,
                "Default": default,
                "Street": street,
                "HouseNumber": house_number,
                "HouseNumberAddition": house_number_addon,
                "PostalCode": postal_code,
                "City": city,
                "StateProvince": state_province,
                "CountryISOCode": country_iso_code,
            },
        }
        response = self.client.service.Address_Insert(**data, _soapheaders=self.auth_manager.header)
        return response

    @nmbrs_exception_handler(resource="CompanyService:Address_Update")
    def update(
        self,
        company_id: int,
        address_id: int,
        default: bool,
        street: str,
        house_number: str,
        house_number_addon: str,
        postal_code: str,
        city: str,
        state_province: str,
        country_iso_code: str,
    ) -> None:
        """
        Update an existing address for the company.

        For more information, refer to the official documentation:
            [Address_Update](https://api.nmbrs.nl/soap/v3/CompanyService.asmx?op=Address_Update)

        Args:
            company_id (int): The ID of the company.
            address_id (int): The ID of the address.
            default (bool): Flag indicating if the address is default.
            street (str): Street name.
            house_number (str): House number.
            house_number_addon (str): House number addition (if any).
            postal_code (str): Postal code.
            city (str): City name.
            state_province (str): State or province name.
            country_iso_code (str): ISO code of the country.
        """
        data = {
            "CompanyId": company_id,
            "Address": {
                "Id": address_id,
                "Default": default,
                "Street": street,
                "HouseNumber": house_number,
                "HouseNumberAddition": house_number_addon,
                "PostalCode": postal_code,
                "City": city,
                "StateProvince": state_province,
                "CountryISOCode": country_iso_code,
            },
        }
        self.client.service.Address_Update(**data, _soapheaders=self.auth_manager.header)
