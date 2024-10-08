# pylint: disable=line-too-long
"""Microservice responsible for journal related actions on the company level."""
import logging

from zeep import Client

from ..micro_service import MicroService
from ....auth.token_manager import AuthManager
from ....utils.nmbrs_exception_handler import nmbrs_exception_handler

logger = logging.getLogger(__name__)


class CompanyJournalService(MicroService):
    """Microservice responsible for journal related actions on the company level."""

    def __init__(self, auth_manager: AuthManager, client: Client):
        super().__init__(auth_manager, client)

    @nmbrs_exception_handler(resource="CompanyService:Journals_GetByRunCompany")
    def get_run_by_company(self):
        """
        Returns the Journal XML, takes year from active year of the company.

        For more information, refer to the official documentation:
            [Journals_GetByRunCompany](https://api.nmbrs.nl/soap/v3/CompanyService.asmx?op=Journals_GetByRunCompany)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="CompanyService:Journals_GetByRunCompany_v2")
    def get_run_by_company_2(self):
        """
        Returns the Journal XML.

        For more information, refer to the official documentation:
            [Journals_GetByRunCompany_v2](https://api.nmbrs.nl/soap/v3/CompanyService.asmx?op=Journals_GetByRunCompany_v2)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="CompanyService:Journals_GetByRunCostCenter")
    def get_run_by_cost_center(self):
        """
        Returns the Journal XML, takes year from active year of the company.

        For more information, refer to the official documentation:
            [Journals_GetByRunCostCenter](https://api.nmbrs.nl/soap/v3/CompanyService.asmx?op=Journals_GetByRunCostCenter)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="CompanyService:Journals_GetByRunCostCenter_v2")
    def get_run_by_cost_center_2(self):
        """
        Returns the Journal XML.

        For more information, refer to the official documentation:
            [Journals_GetByRunCostCenter_v2](https://api.nmbrs.nl/soap/v3/CompanyService.asmx?op=Journals_GetByRunCostCenter_v2)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="CompanyService:Journals_GetByRunCostCenterCostUnit")
    def get_run_by_cost_center_nad_cost_unit(self):
        """
        Returns the Journal XML with Cost Center/Cost Unit information, takes year from active year of the company.

        For more information, refer to the official documentation:
            [Journals_GetByRunCostCenterCostUnit](https://api.nmbrs.nl/soap/v3/CompanyService.asmx?op=Journals_GetByRunCostCenterCostUnit)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="CompanyService:Journals_GetByRunCostCenterCostUnitPerYear")
    def get_run_by_cost_center_nad_cost_unit_per_year(self):
        """
        Returns the Journal XML with Cost Center/Cost Unit information of the given year.

        For more information, refer to the official documentation:
            [Journals_GetByRunCostCenterCostUnitPerYear](https://api.nmbrs.nl/soap/v3/CompanyService.asmx?op=Journals_GetByRunCostCenterCostUnitPerYear)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="CompanyService:Journals_GetByRunDepartment")
    def get_run_by_department(self):
        """
        Returns the Journal XML, takes year from active year of the company.

        For more information, refer to the official documentation:
            [Journals_GetByRunDepartment](https://api.nmbrs.nl/soap/v3/CompanyService.asmx?op=Journals_GetByRunDepartment)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="CompanyService:Journals_GetByRunDepartment_v2")
    def get_run_by_department_2(self):
        """
        Returns the Journal XML.

        For more information, refer to the official documentation:
            [Journals_GetByRunDepartment_v2](https://api.nmbrs.nl/soap/v3/CompanyService.asmx?op=Journals_GetByRunDepartment_v2)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="CompanyService:Journals_GetByRunEmployee")
    def get_run_by_employee(self):
        """
        Returns the Journal XML, takes year from active year of the company.

        For more information, refer to the official documentation:
            [Journals_GetByRunEmployee](https://api.nmbrs.nl/soap/v3/CompanyService.asmx?op=Journals_GetByRunEmployee)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="CompanyService:Journals_GetByRunEmployee_v2")
    def get_run_by_employee_2(self):
        """
        Returns the Journal XML.

        For more information, refer to the official documentation:
            [Journals_GetByRunEmployee_v2](https://api.nmbrs.nl/soap/v3/CompanyService.asmx?op=Journals_GetByRunEmployee_v2)
        """
        raise NotImplementedError()  # pragma: no cover
