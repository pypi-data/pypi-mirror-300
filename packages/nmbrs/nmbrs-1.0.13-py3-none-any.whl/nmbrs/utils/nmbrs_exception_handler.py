"""Exception Handling Decorators for Nmbrs SOAP API"""

import logging
import time

import zeep.exceptions

from .get_module_path import get_module_path
from ..exceptions import (
    AuthenticationException,
    AuthorizationException,
    AuthorizationDataException,
    NoValidSubscriptionException,
    InvalidHourComponentException,
    InvalidWageComponentException,
    UnauthorizedEmployeeException,
    UnauthorizedCompanyException,
    InvalidPeriodException,
    UnauthorizedDebtorException,
    UnknownNmbrsException,
    UnknownException,
    LoginSecurityFailureException,
    MultipleEnvironmentAccountsException,
    DomainNotFoundException,
    InvalidCredentialsException,
    InvalidBankAccountIbanException,
    NotAvailableOnFreeTrialException,
    WageTaxDeclarationAlreadySentException,
    ProtectedModeException,
    InvalidLeaveTypeException,
    InvalidTaskResultException,
    TaskStatusNotAvailable2Exception,
    TaskStatusNotAvailableException,
    InvalidLeaveIdException,
    InvalidLabourAgreementIdException,
    InvalidBankAccountTypeException,
    InvalidBankAccountNumberException,
    TimeSlotsOverlapException,
    StartTimeAfterEndTimeException,
    InvalidTaxTypeException,
    TaxTypeRequiredException,
    BankAccountIbanRequiredException,
    InvalidSetOfValuesException,
    TaxFormRequiredException,
    FileTooLargeException,
    ProvideExtensionException,
    DuplicatedCostCenterCodeExceptionException,
    InvalidCostCenterCode,
    InvalidCostCenterIdException,
    InvalidTaxFormException,
    InvalidNameException,
    InvalidEndpointException,
    NotFoundException,
    InvalidDocumentTypeException,
)

logger = logging.getLogger(__name__)


def nmbrs_exception_handler(resource: str):
    """
    Decorator to handle exceptions raised by Nmbrs SOAP API.

    Args:
        resource (str): Resources being called.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                start_time = time.time()
                response = func(*args, **kwargs)
                end_time = time.time()

                logger.name = get_module_path(func)
                logger.debug("%s execution time: %s seconds", resource, end_time - start_time)

                if response is None:
                    logger.debug("Used resource: %s, was not able to retrieve anything.", resource)
                elif isinstance(response, list):
                    logger.debug("Used resource: %s, retrieved %s entries.", resource, len(response))
                else:
                    logger.debug("Used resource: %s, retrieved %s entries.", resource, 1)

                return response
            except zeep.exceptions.Fault as e:
                error_map = {
                    1001: AuthenticationException,
                    1002: AuthorizationException,
                    1003: AuthorizationDataException,
                    1004: NoValidSubscriptionException,
                    1006: LoginSecurityFailureException,
                    2001: InvalidHourComponentException,
                    2002: InvalidWageComponentException,
                    2003: UnauthorizedEmployeeException,
                    2004: UnauthorizedCompanyException,
                    2006: InvalidPeriodException,
                    2009: UnauthorizedDebtorException,
                    2011: ProtectedModeException,
                    2012: WageTaxDeclarationAlreadySentException,
                    2013: NotAvailableOnFreeTrialException,
                    2014: InvalidBankAccountIbanException,
                    2015: InvalidBankAccountNumberException,
                    2016: InvalidBankAccountTypeException,
                    2017: InvalidLabourAgreementIdException,
                    2018: InvalidLeaveIdException,
                    2019: TaskStatusNotAvailableException,
                    2020: TaskStatusNotAvailable2Exception,
                    2021: InvalidTaskResultException,
                    2022: InvalidLeaveTypeException,
                    2028: StartTimeAfterEndTimeException,
                    2029: TimeSlotsOverlapException,
                    2030: InvalidSetOfValuesException,
                    2032: BankAccountIbanRequiredException,
                    2033: TaxTypeRequiredException,
                    2034: InvalidTaxTypeException,
                    2035: TaxFormRequiredException,
                    2036: InvalidTaxFormException,
                    2037: InvalidCostCenterIdException,
                    2038: InvalidCostCenterCode,
                    2039: DuplicatedCostCenterCodeExceptionException,
                    2040: ProvideExtensionException,
                    2041: FileTooLargeException,
                    2042: MultipleEnvironmentAccountsException,
                    2043: DomainNotFoundException,
                    2044: InvalidEndpointException,
                    2045: InvalidNameException,
                    2046: NotFoundException,
                    2047: InvalidDocumentTypeException,
                    9999: UnknownNmbrsException,
                }
                exception_str = str(e)

                # Log the exception
                logger.error("Exception occurred in %s. Exception: %s", func.__name__, exception_str)

                # Exceptions without code
                if "---> Invalid combination email/password" in exception_str:
                    raise InvalidCredentialsException(resource=resource) from e

                for error_code, exception_class in error_map.items():
                    if f"---> {error_code}:" in exception_str:
                        raise exception_class(resource=resource) from e
                raise UnknownException(resource=resource) from e

        return wrapper

    return decorator
