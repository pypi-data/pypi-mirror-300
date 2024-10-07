import time
import requests
import json

from abc import abstractmethod

API_ROOT = "https://api.fivaldi.net/"


class BaseEndpoint:

    def __init__(self, client):
        self._client = client

    @abstractmethod
    def api_root(self):
        return

    def _get(self, endpoint, **kwargs):
        API_ENDPOINT = f"{self.api_root()}/{endpoint}"

        print(API_ENDPOINT)

        HTTP_METHOD = "GET"
        CONTENT_TYPE = "application/json"

        # body = open('body.json', 'r', encoding='utf8').read()
        # body = json.loads(body)
        # body = json.dumps(body)
        body = None

        # Get the current UNIX Epoch.
        epoch = str(int(time.time()))

        # Create the signature.
        signature = self._client.generate_signature(
            http_method=HTTP_METHOD,
            epoch=epoch,
            endpoint=API_ENDPOINT,
            body=body,
            content_type=CONTENT_TYPE
        )

        # Defining the headers that will be sent to the endpoint.
        HEADERS = {
            'Content-Type': CONTENT_TYPE,
            'X-Fivaldi-Partner': self._client.partner_id,
            'X-Fivaldi-Timestamp': epoch,
            'Authorization': signature,
        }

        if HTTP_METHOD == "GET":
            # Send the request.
            r = requests.get(url="https://api.fivaldi.net" + API_ENDPOINT, headers=HEADERS, timeout=360)

            if r.status_code != 200:
                raise RuntimeError(str(r.status_code) + " " + str(r.reason) + " | " + str(r.text))
            return r.json()

        if HTTP_METHOD == "POST":
            # Send the request.
            r = requests.post(url="https://api.fivaldi.net" + API_ENDPOINT, headers=HEADERS, data=body, timeout=360)

            if r.status_code != 200:
                raise RuntimeError(str(r.status_code) + " " + str(r.reason) + " | " + str(r.text))
            return r.json()

        raise RuntimeError("Invalid HTTP Method")


class CompanyEndPoint(BaseEndpoint):

    def __init__(self, cuid, client):
        super().__init__(client)
        self._cuid = cuid

    def api_root(self):
        return f'/customer/api/companies/{self._cuid}'


class CompanyProductEndpoint(CompanyEndPoint):

    def __init__(self, cuid, client):
        super().__init__(cuid=cuid, client=client)

    def api_root(self):
        return f"{super().api_root()}/products"

    def product_register_basic_details(self):
        return self._get(endpoint=f'getProductRegisterBasicDetails')

    def products(self):
        return self._get(endpoint=f'products')


class CompanyEstatePersonEndpoint(CompanyEndPoint):

    def __init__(self, cuid, client):
        super().__init__(cuid=cuid, client=client)

    def api_root(self):
        return f"{super().api_root()}/estate-person"

    def persons(self):
        return self._get(endpoint=f'persons')

    def person(self, id):
        return self._get(endpoint=f'person/{id}')


class CompanyChartOfAccountsEndpoint(CompanyEndPoint):

    def __init__(self, cuid, client):
        super().__init__(cuid=cuid, client=client)

    def api_root(self):
        return f"{super().api_root()}/chart-of-accounts"

    def get(self, dimension=0):
        return self._get(endpoint=f'?dimension={dimension}')


class CompanyEstatePreferencesEndpoint(CompanyEndPoint):

    def __init__(self, cuid, client):
        super().__init__(cuid=cuid, client=client)

    def api_root(self):
        return f"{super().api_root()}/estate-preferences"

    def housing_company_details(self):
        return self._get(endpoint=f'housingCompanyDetails')


class CompanyEstatePaymentTypesEndpoint(CompanyEndPoint):

    def __init__(self, cuid, client):
        super().__init__(cuid=cuid, client=client)

    def api_root(self):
        return f"{super().api_root()}/estate-payment-types"

    def payment_types(self):
        return self._get(endpoint=f'payment-types')


class CompanyEstateBondEndpoint(CompanyEndPoint):

    def __init__(self, cuid, client):
        super().__init__(cuid=cuid, client=client)

    def api_root(self):
        return f"{super().api_root()}/estate-bond"

    def bonds(self):
        return self._get(endpoint=f'bonds')

    def bond(self, reference_number):
        return self._get(endpoint=f'bonds/{reference_number}')

    def payment_types(self):
        return self._get(endpoint=f'bond_paymenttypes')


class CompanyEstateApartmentEndpoint(CompanyEndPoint):

    def __init__(self, cuid, client):
        super().__init__(cuid=cuid, client=client)

    def api_root(self):
        return f"{super().api_root()}/estate-apartment"

    def apartments(self):
        return self._get(endpoint=f'apartments')

    def apartment(self, apartment_id):
        return self._get(endpoint=f'apartments/{apartment_id}')

    def repairs(self, apartment_id=None):
        if apartment_id is None:
            return self._get(endpoint=f'repairs')
        return self._get(endpoint=f'repairs/apartments/{apartment_id}/repairs')

    def bonds(self, apartment_id):
        return self._get(endpoint=f'apartments/{apartment_id}/bonds')


class CompanyEstateMeterEndpoint(CompanyEndPoint):

    def __init__(self, cuid, client):
        super().__init__(cuid=cuid, client=client)

    def api_root(self):
        return f"{super().api_root()}/estate-meter"

    def meters(self):
        return self._get(endpoint=f'meters')

    def meter_readings(self, apartment_id):
        return self._get(endpoint=f'meter-readings/apartments/{apartment_id}')


class CompanyEstateRentLedgerEndpoint(CompanyEndPoint):

    def __init__(self, cuid, client):
        super().__init__(cuid=cuid, client=client)

    def api_root(self):
        return f"{super().api_root()}/estate-rent-ledger"

    def apartment(self, apartment_id):
        return self._get(endpoint=f'getReceivablesAndPrepayments/apartments/{apartment_id}')


class CompanyPurchasesEndpoint(CompanyEndPoint):

    def __init__(self, cuid, client):
        super().__init__(cuid=cuid, client=client)

    def api_root(self):
        return f"{super().api_root()}/purchases"

    def invoices(self):
        return self._get(endpoint=f'invoices')

    def invoice(self, id):
        return self._get(endpoint=f'invoices/{id}')

    def invoice_comments(self, id):
        return self._get(endpoint=f'invoices/{id}/comments')

    def invoice_rows(self, id):
        return self._get(endpoint=f'invoices/{id}/rows')

    def invoice_row(self, invoice_id, row_id):
        return self._get(endpoint=f'invoices/{invoice_id}/rows/{row_id}')


class CompanyBookkeepingEndpoint(CompanyEndPoint):

    def __init__(self, cuid, client):
        super().__init__(cuid=cuid, client=client)

    def api_root(self):
        return f"{super().api_root()}/bookkeeping"

    def budget(self, fiscal_year_id):
        return self._get(endpoint=f'budget?fiscalYearId={fiscal_year_id}')

    def account_balance(self, month: int):
        return self._get(endpoint=f'accountBalance?month={month}')

    def vat_codes(self):
        return self._get(endpoint=f'vatCodes')

    def fiscal_years(self):
        return self._get(endpoint=f'fiscalYears')


class CustomerApiEndpoint(BaseEndpoint):

    def __init__(self, client):
        super().__init__(client)

    def api_root(self):
        return ""

    @property
    def customers(self):
        return self._get(endpoint='customer/api/customers')

    def companies(self, customer_id: str) -> list:

        companies = self._get(endpoint=f'customer/api/companies?customerId={customer_id}')

        return [Company(json=company_json, client=self._client) for company_json in companies]


class Company:
    def __init__(self, json, client):
        self._json = json
        self._cuid = json['cuid']
        self._client = client

    @property
    def json(self) -> str:
        return self._json

    def chart_of_accounts(self, dimensions=0):
        return CompanyChartOfAccountsEndpoint(
            self._cuid,
            client=self._client).get(dimension=dimensions)

    @property
    def estate_preferences_housing_company_details(self):
        return CompanyEstatePreferencesEndpoint(
            self._cuid,
            client=self._client)

    @property
    def estate_apartment(self):
        return CompanyEstateApartmentEndpoint(
            self._cuid,
            client=self._client)

    @property
    def bookkeeping(self):
        return CompanyBookkeepingEndpoint(
            self._cuid,
            client=self._client)

    @property
    def product(self):
        return CompanyProductEndpoint(
            self._cuid,
            client=self._client)

    @property
    def estate_person(self):
        return CompanyEstatePersonEndpoint(
            self._cuid,
            client=self._client)

    @property
    def estate_payment_types(self):
        return CompanyEstatePaymentTypesEndpoint(
            self._cuid,
            client=self._client)

    @property
    def estate_meter(self):
        return CompanyEstateMeterEndpoint(
            self._cuid,
            client=self._client)

    @property
    def estate_rent_ledger(self):
        return CompanyEstateRentLedgerEndpoint(
            self._cuid,
            client=self._client)

    @property
    def estate_bond(self):
        return CompanyEstateBondEndpoint(
            self._cuid,
            client=self._client)

    @property
    def purchases(self):
        return CompanyPurchasesEndpoint(
            self._cuid,
            client=self._client)
