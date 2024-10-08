"""
Module for handling the Debtor Nmbrs services.
"""

import logging
from datetime import datetime

from zeep import Client
from zeep.helpers import serialize_object

from .microservices.debtor import DebtorDepartmentService, DebtorFunctionService, DebtorTitleService, DebtorWebHooksService
from .service import Service
from ..auth.token_manager import AuthManager
from ..utils.nmbrs_exception_handler import nmbrs_exception_handler
from ..utils.return_list import return_list
from ..data_classes.debtor import (
    Debtor,
    AbsenceVerzuim,
    Address,
    BankAccount,
    ContactInfo,
    LabourAgreementSettings,
    Manager,
    ServiceLevel,
    Tag,
    Domain,
)

logger = logging.getLogger(__name__)


class DebtorService(Service):
    """
    A class representing Debtor Service for interacting with Nmbrs debtor-related functionalities.

    Not implemented calls:
        1 [Converter_GetDebtors_IntToGuid](https://api.nmbrs.nl/soap/v3/DebtorService.asmx?op=Converter_GetDebtors_IntToGuid)
    """

    def __init__(self, auth_manager: AuthManager, sandbox: bool = True):
        super().__init__(auth_manager, sandbox)

        # Initialize nmbrs services
        self.client = Client(f"{self.base_uri}{self.debtor_uri}")

        # Micro services
        self._department = None
        self._function = None
        self._webhook = None
        self._title = None

        logger.info("DebtorService initialized.")

    @property
    def department(self):
        """
        Lazily initializes and returns the DebtorDepartmentService instance.
        """
        if self._department is None:
            self._department = DebtorDepartmentService(self.auth_manager, self.client)
        return self._department

    @property
    def function(self):
        """
        Lazily initializes and returns the DebtorFunctionService instance.
        """
        if self._function is None:
            self._function = DebtorFunctionService(self.auth_manager, self.client)
        return self._function

    @property
    def webhook(self):
        """
        Lazily initializes and returns the DebtorWebHooksService instance.
        """
        if self._webhook is None:
            self._webhook = DebtorWebHooksService(self.auth_manager, self.client)
        return self._webhook

    @property
    def title(self):
        """
        Lazily initializes and returns the DebtorTitleService instance.
        """
        if self._title is None:
            self._title = DebtorTitleService(self.auth_manager, self.client)
        return self._title

    @nmbrs_exception_handler(resource="DebtorService:Environment_Get")
    def get_domain(self, username: str, token: str) -> Domain:
        """
        Generate authentication header for standard token-based authentication.

        For more information, refer to the official documentation:
            [Soap call WebhookSettings_Insert](https://api.nmbrs.nl/soap/v3/DebtorService.asmx?op=Environment_Get)

        Args:
            username (str): A string representing the username for authentication.
            token (str): A string representing the token for authentication.

        Returns:
            Domain: The domain object associated with the token.
        """
        env = self.client.service.Environment_Get(_soapheaders={"AuthHeader": {"Username": username, "Token": token}})
        return Domain(data=serialize_object(env))

    @return_list
    @nmbrs_exception_handler(resource="DebtorService:List_GetAll")
    def get_all(self) -> list[Debtor]:
        """
        Retrieve all debtors.

        For more information, refer to the official documentation:
            [Soap call List_GetAll](https://api.nmbrs.nl/soap/v3/DebtorService.asmx?op=List_GetAll)

        Returns:
            list[Debtor]: A list of Debtor objects representing all debtors.
        """
        debtors = self.client.service.List_GetAll(_soapheaders=self.auth_manager.header)
        debtors = [Debtor(debtor) for debtor in serialize_object(debtors)]
        return debtors

    @return_list
    @nmbrs_exception_handler(resource="DebtorService:List_GetByNumber")
    def get_all_by_number(self, number: str) -> list[Debtor]:
        """
        Retrieve all debtors by number.

        For more information, refer to the official documentation:
            [Soap call List_GetByNumber](https://api.nmbrs.nl/soap/v3/DebtorService.asmx?op=List_GetByNumber)

        Args:
            number (str): The debtor number.

        Returns:
            list[Debtor]: A list of Debtor objects representing all debtors.
        """
        debtors = self.client.service.List_GetByNumber(Number=number, _soapheaders=self.auth_manager.header)
        debtors = [Debtor(debtor) for debtor in serialize_object(debtors)]
        return debtors

    @nmbrs_exception_handler(resource="DebtorService:Debtor_Get")
    def get(self, debtor_id: int) -> Debtor | None:
        """
        Retrieve a debtor by ID.

        For more information, refer to the official documentation:
            [Soap call Debtor_Get](https://api.nmbrs.nl/soap/v3/DebtorService.asmx?op=Debtor_Get)

        Args:
            debtor_id (int): The ID of the debtor.

        Returns:
            Debtor | None: A Debtor object representing the debtor if found, otherwise None.
        """
        debtor = self.client.service.Debtor_Get(DebtorId=debtor_id, _soapheaders=self.auth_manager.header)
        if debtor is None:
            logger.debug("No debtor found, ID: %s.", debtor_id)
            return None
        return Debtor(serialize_object(debtor))

    @nmbrs_exception_handler(resource="DebtorService:Debtor_Insert")
    def post(self, debtor_id: int, number: str, name: str) -> int:
        """
        Insert a new debtor.

        For more information, refer to the official documentation:
            [Soap call Debtor_Insert](https://api.nmbrs.nl/soap/v3/DebtorService.asmx?op=Debtor_Insert)

        Args:
            debtor_id (int): The ID of the debtor.
            number (str): The number of the debtor.
            name (str): The name of the debtor.

        Returns:
            int: The ID of the inserted debtor if successful.
        """
        data = {"Debtor": {"Id": debtor_id, "Number": number, "Name": name}}
        inserted = self.client.service.Debtor_Insert(**data, _soapheaders=self.auth_manager.header)
        return inserted

    @nmbrs_exception_handler(resource="DebtorService:Debtor_Update")
    def update(self, debtor_id: int, number: str, name: str) -> None:
        """
        Update an existing debtor.

        For more information, refer to the official documentation:
            [Soap call Debtor_Update](https://api.nmbrs.nl/soap/v3/DebtorService.asmx?op=Debtor_Update)

        Args:
            debtor_id (int): The ID of the debtor.
            number (str): The new number of the debtor.
            name (str): The new name of the debtor.
        """
        data = {"Debtor": {"Id": debtor_id, "Number": number, "Name": name}}
        self.client.service.Debtor_Update(**data, _soapheaders=self.auth_manager.header)

    @return_list
    @nmbrs_exception_handler(resource="DebtorService:AbsenceXML_Get")
    def get_absence_xml(self, debtor_id: int, start_date: datetime, end_date: datetime) -> list[AbsenceVerzuim]:
        """
        Retrieve absence data for a debtor within a specified date range.

        For more information, refer to the official documentation:
            [Soap call AbsenceXML_Get](https://api.nmbrs.nl/soap/v3/DebtorService.asmx?op=AbsenceXML_Get)

        Args:
            debtor_id (int): An integer representing the debtor's ID.
            start_date (datetime): A datetime representing the start date of the period to retrieve data.
            end_date (datetime): A datetime representing the end date of the period to retrieve data.

        Returns:
            list[AbsenceVerzuim]: A list of AbsenceVerzuim objects representing the absence data.
        """
        data = {"DebtorId": debtor_id, "from": start_date, "to": end_date}
        absences = self.client.service.AbsenceXML_Get(**data, _soapheaders=self.auth_manager.header)
        absences = [AbsenceVerzuim(absence) for absence in serialize_object(absences)]
        return absences

    @return_list
    @nmbrs_exception_handler(resource="DebtorService:AccountantContact_GetList")
    def get_all_accountant_contact_info(self, debtor_id: int) -> list[ContactInfo]:
        """
        Retrieve all accountant contact information.

        For more information, refer to the official documentation:
            [Soap call AccountantContact_GetList](https://api.nmbrs.nl/soap/v3/DebtorService.asmx?op=AccountantContact_GetList)

        Args:
            debtor_id (int): The ID of the debtor.

        Returns:
            list[ContactInfo]: A list of ContactInfo objects representing the accountant contact information.
        """
        accountants = self.client.service.AccountantContact_GetList(DebtorId=debtor_id, _soapheaders=self.auth_manager.header)
        accountants = [ContactInfo(debtor_id=debtor_id, data=accountant) for accountant in serialize_object(accountants)]
        return accountants

    @nmbrs_exception_handler(resource="DebtorService:Address_Get")
    def get_address(self, debtor_id: int) -> Address | None:
        """
        Retrieve address information for a debtor.

        For more information, refer to the official documentation:
            [Soap call Address_Get](https://api.nmbrs.nl/soap/v3/DebtorService.asmx?op=Address_Get)

        Args:
            debtor_id (int): The ID of the debtor.

        Returns:
            Address | None: An Address object representing the address if found, otherwise None.
        """
        address = self.client.service.Address_Get(DebtorId=debtor_id, _soapheaders=self.auth_manager.header)
        if address is None:
            logger.debug("No address found for debtor, ID: %s.", debtor_id)
            return None
        return Address(debtor_id=debtor_id, data=serialize_object(address))

    @nmbrs_exception_handler(resource="DebtorService:BankAccount_Get")
    def get_bank_account(self, debtor_id: int) -> BankAccount | None:
        """
        Retrieve bank account information for a debtor.

        For more information, refer to the official documentation:
            [Soap call BankAccount_Get](https://api.nmbrs.nl/soap/v3/DebtorService.asmx?op=BankAccount_Get)

        Args:
            debtor_id (int): The ID of the debtor.

        Returns:
            BankAccount | None: A BankAccount object representing the bank account if found, otherwise None.
        """
        bank_account = self.client.service.BankAccount_Get(DebtorId=debtor_id, _soapheaders=self.auth_manager.header)
        if bank_account is None:
            logger.debug("No bank account found for debtor, ID: %s.", debtor_id)
            return None
        return BankAccount(debtor_id=debtor_id, data=serialize_object(bank_account))

    @nmbrs_exception_handler(resource="DebtorService:ContactPerson_Get")
    def get_contact_person(self, debtor_id: int) -> ContactInfo | None:
        """
        Retrieve contact person information for a debtor.

        For more information, refer to the official documentation:
            [Soap call ContactPerson_Get](https://api.nmbrs.nl/soap/v3/DebtorService.asmx?op=ContactPerson_Get)

        Args:
            debtor_id (int): The ID of the debtor.

        Returns:
            ContactInfo | None: A ContactInfo object representing the contact person if found, otherwise None.
        """
        contact_person = self.client.service.ContactPerson_Get(DebtorId=debtor_id, _soapheaders=self.auth_manager.header)
        if contact_person is None:
            logger.debug("No contact person found for debtor, ID: %s.", debtor_id)
            return None
        return ContactInfo(debtor_id=debtor_id, data=serialize_object(contact_person))

    @nmbrs_exception_handler(resource="DebtorService:Debtor_IsOwner")
    def is_owner(self) -> bool:
        """
        Check if the current user is the owner of the debtor.

        For more information, refer to the official documentation:
            [Soap call Debtor_IsOwner](https://api.nmbrs.nl/soap/v3/DebtorService.asmx?op=Debtor_IsOwner)

        Returns:
            bool: True if the current user is the owner of the debtor, otherwise False.
        """
        is_owner = self.client.service.Debtor_IsOwner(_soapheaders=self.auth_manager.header)
        return is_owner

    @return_list
    @nmbrs_exception_handler(resource="DebtorService:LabourAgreementSettings_GetList")
    def get_all_labour_agreements(self, debtor_id: int, period: int, year: int) -> list[LabourAgreementSettings]:
        """
        Retrieve all labour agreement settings for a debtor.

        For more information, refer to the official documentation:
            [Soap call LabourAgreementSettings_GetList](https://api.nmbrs.nl/soap/v3/DebtorService.asmx?op=LabourAgreementSettings_GetList)

        Args:
            debtor_id (int): The ID of the debtor.
            period (int): The period for which to retrieve labour agreement settings.
            year (int): The year for which to retrieve labour agreement settings.

        Returns:
            list[LabourAgreementSettings]: A list of LabourAgreementSettings objects representing all labour
            agreement settings.
        """
        labour_agreements = self.client.service.LabourAgreementSettings_GetList(
            DebtorId=debtor_id, Year=year, Period=period, _soapheaders=self.auth_manager.header
        )
        labour_agreements = [
            LabourAgreementSettings(debtor_id=debtor_id, data=labour_agreement) for labour_agreement in serialize_object(labour_agreements)
        ]
        return labour_agreements

    @return_list
    @nmbrs_exception_handler(resource="DebtorService:Manager_GetList")
    def get_all_managers(self, debtor_id: int) -> list[Manager]:
        """
        Retrieve all managers for a debtor.

        For more information, refer to the official documentation:
            [Soap call Manager_GetList](https://api.nmbrs.nl/soap/v3/DebtorService.asmx?op=Manager_GetList)

        Args:
            debtor_id (int): The ID of the debtor.

        Returns:
            list[Manager]: A list of Manager objects representing all managers for the debtor.
        """
        managers = self.client.service.Manager_GetList(DebtorId=debtor_id, _soapheaders=self.auth_manager.header)
        managers = [Manager(debtor_id=debtor_id, data=manager) for manager in serialize_object(managers)]
        return managers

    @nmbrs_exception_handler(resource="DebtorService:ServiceLevel_Get")
    def get_service_level(self, debtor_id: int) -> ServiceLevel | None:
        """
        Retrieve service level information for a debtor.

        For more information, refer to the official documentation:
            [Soap call ServiceLevel_Get](https://api.nmbrs.nl/soap/v3/DebtorService.asmx?op=ServiceLevel_Get)

        Args:
            debtor_id (int): The ID of the debtor.

        Returns:
            ServiceLevel | None: A ServiceLevel object representing the service level information if found, otherwise
            None.
        """
        service_level = self.client.service.ServiceLevel_Get(DebtorId=debtor_id, _soapheaders=self.auth_manager.header)
        if service_level is None:
            logger.debug("No service level found for debtor, ID: %s.", debtor_id)
            return None
        return ServiceLevel(debtor_id=debtor_id, data=serialize_object(service_level))

    @return_list
    @nmbrs_exception_handler(resource="DebtorService:Tags_Get")
    def get_tags(self, debtor_id: int) -> list[Tag]:
        """
        Retrieve all tags for a debtor.

        For more information, refer to the official documentation:
            [Soap call Tags_Get](https://api.nmbrs.nl/soap/v3/DebtorService.asmx?op=Tags_Get)

        Args:
            debtor_id (int): The ID of the debtor.

        Returns:
            list[Tag]: A list of Tag objects representing all tags associated with the debtor.
        """
        tags = self.client.service.Tags_Get(DebtorId=debtor_id, _soapheaders=self.auth_manager.header)
        tags = [Tag(debtor_id=debtor_id, data=tag) for tag in serialize_object(tags)]
        return tags
