import requests

EXCHANGE_SUPPORTED_CURRENCIES = [
    "ARS", "AUD", "BCH", "BGN", "BNB", "BRL", "BTC", "CAD", "CHF", "CNY", 
    "CYP", "CZK", "DKK", "DOGE", "DZD", "EEK", "ETH", "EUR", "GBP", "GRD", 
    "HKD", "HRK", "HUF", "IDR", "ILS", "INR", "ISK", "JPY", "KRW", "LTC", 
    "LTL", "LVL", "MAD", "MTL", "MXN", "MYR", "NOK", "NZD", "PHP", "PLN", 
    "RON", "RUB", "SEK", "SGD", "SIT", "SKK", "THB", "TRY", "TWD", "USD", 
    "XRP", "ZAR"
]


VAT_SUPPORTED_COUNTRIES = [
    "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES", "FI", "FR", "HR",
    "HU", "IR", "IT", "LT", "LU", "LV", 
    "MT", "NL", "PL", "PT", "RO", "SE", "SI", "SK", "XI",
]
        

class VatAPI:
    def __init__(self, api_key):
        self.api_key: str = api_key
        self.__vatURL: str = "https://vat.abstractapi.com/v1/"

    def __type_validation(self, type_, arg):
        if not isinstance(arg, type_):
            raise TypeError(f"Expected '{type_}' but got {type(arg).__name__}")
    
    def validate(self, vat_number: str) -> dict:
        self.__type_validation(str, vat_number)
        params = {"api_key": self.api_key}
        params["vat_number"] = vat_number
        url = self.__vatURL + "validate"
        response = requests.get(url, params=params)
        json_response = response.json()
        json_response["status"] = response.status_code
        return json_response
    
    def calculate(self, amount: str, country_code: str, **kwargs) -> dict:
        params = {"api_key": self.api_key}
        self.__type_validation(str, amount)
        self.__type_validation(str, country_code)
        params["amount"] = amount
        params["country_code"] = country_code
        is_vat_incl = kwargs.get("is_vat_incl", None)
        vat_category = kwargs.get("vat_category", None)

        if is_vat_incl is not None:
            self.__type_validation(bool, is_vat_incl)
            params["is_vat_incl"] = is_vat_incl
        if vat_category:
            self.__type_validation(str, vat_category)
            params["vat_category"] = vat_category

        url = self.__vatURL + "calculate"
        response = requests.request("GET", url, params=params)
        json_response = response.json()
        json_response["status"] = response.status_code
        return json_response

    def categories(self, country_code: str):
        params = {"api_key": self.api_key}
        self.__type_validation(str, country_code)
        params["country_code"] = country_code
        url = self.__vatURL + "categories"
        response = requests.request("GET", url, params=params)
        json_response = response.json()
        json_response.append({"status": response.status_code})
        return json_response


class IpAPI:
    def __init__(self, api_key):
        self.api_key: str = api_key
        self.__ipURL: str = "https://ipgeolocation.abstractapi.com/v1"

    def __type_validation(self, type_, arg):
        if not isinstance(arg, type_):
            raise TypeError(f"Expected '{type_}' but got {type(arg).__name__}")

    def ip_info(self, **kwargs):
        params = {"api_key": self.api_key}
        ip_address = kwargs.get("ip_address", None)
        fields = kwargs.get("fields", None)

        if ip_address:
            self.__type_validation(str, ip_address)
            params["ip_address"] = ip_address
        if fields:
            self.__type_validation(str, fields)
            params["fields"] = fields
         
        response = requests.request("GET", self.__ipURL, params=params)
        json_response = response.json()
        json_response["status"] = response.status_code
        return json_response


class ExchangeRatesAPI:
    def __init__(self, api_key):
        self.api_key: str = api_key
        self.__ratesURL: str = "https://exchange-rates.abstractapi.com/v1/"

    def __type_validation(self, type_, arg):
        if not isinstance(arg, type_):
            raise TypeError(f"Expected '{type_}' but got {type(arg).__name__}")
    
    def live(self, base: str, **kwargs):
        params = {"api_key": self.api_key}
        self.__type_validation(str, base)
        params["base"] = base
        target = kwargs.get("target", None)

        if target:
            self.__type_validation(str, target)
            params["target"] = target

        url = self.__ratesURL + "live"
        response = requests.request("GET", url, params=params)
        json_response = response.json()
        json_response["status"] = response.status_code
        return json_response

    def convert(self, base: str, target: str, **kwargs):
        params = {"api_key": self.api_key}
        self.__type_validation(str, base),
        self.__type_validation(str, target)
        params["base"] = base,
        params["target"] = target
        date = kwargs.get("date", None)
        base_amount = kwargs.get("base_amount", None)

        if date:
            self.__type_validation(str, date)
            params["date"] = date
        
        if base_amount:
            self.__type_validation(float, base_amount)
            params["base_amount"] = base_amount

        url = self.__ratesURL + "convert"
        response = requests.request("GET", url, params=params)
        json_response = response.json()
        json_response["status"] = response.status_code
        return json_response

    def historical(self, base: str, date: str, **kwargs):
        params = {"api_key": self.api_key}
        self.__type_validation(str, base)
        self.__type_validation(str, date)
        params["base"] = base
        params["date"] = date

        target = kwargs.get("target", None)

        if target:
            self.__type_validation(str, target)
            params["target"] = target

        url = self.__ratesURL + "historical"
        response = requests.request("GET", url, params=params)
        json_response = response.json()
        json_response["status"] = response.status_code
        return json_response



