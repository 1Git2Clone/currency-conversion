import json
import math

from requests import get
from requests.models import Response
from argparse import ArgumentParser
from datetime import datetime
from os import path


class CachedConversions:
    stored_values: dict[
        tuple[str, str],
        float,
    ]

    def __init__(self) -> None:
        self.stored_values = dict()

    def new_entry(
        self,
        from_currency: str,
        to_currency: str,
        coefficient: float,
    ) -> None:
        self.stored_values[(from_currency, to_currency)] = coefficient


class OutputJSON:
    date: str
    amount: float
    base_currency: str
    target_currency: str
    converted_amount: float

    output_json: list[dict[str, str | float]]

    def __init__(self) -> None:
        self.idx = 1
        self.output_json = list()

    def append(
        self, date, amount, base_currency, target_currency, converted_amount
    ) -> None:
        self.output_json.append(
            {
                "date": date,
                "amount": amount,
                "base_currency": base_currency,
                "target_currency": target_currency,
                "converted_amount": converted_amount,
            },
        )


ISO_4217_CURRENCY_CODES: set = {
    "AED",
    "AFN",
    "ALL",
    "AMD",
    "ANG",
    "AOA",
    "ARS",
    "AUD",
    "AWG",
    "AZN",
    "BAM",
    "BBD",
    "BDT",
    "BGN",
    "BHD",
    "BIF",
    "BMD",
    "BND",
    "BOB",
    "BOV",
    "BRL",
    "BSD",
    "BTN",
    "BWP",
    "BYN",
    "BZD",
    "CAD",
    "CDF",
    "CHE",
    "CHF",
    "CHW",
    "CLF",
    "CLP",
    "CNY",
    "COP",
    "COU",
    "CRC",
    "CUC",
    "CUP",
    "CVE",
    "CZK",
    "DJF",
    "DKK",
    "DOP",
    "DZD",
    "EGP",
    "ERN",
    "ETB",
    "EUR",
    "FJD",
    "FKP",
    "FOK",
    "GBP",
    "GEL",
    "GGP",
    "GHS",
    "GIP",
    "GMD",
    "GNF",
    "GTQ",
    "GYD",
    "HKD",
    "HNL",
    "HRK",
    "HTG",
    "HUF",
    "IDR",
    "ILS",
    "IMP",
    "INR",
    "IQD",
    "IRR",
    "ISK",
    "JEP",
    "JMD",
    "JOD",
    "JPY",
    "KES",
    "KGS",
    "KHR",
    "KID",
    "KMF",
    "KRW",
    "KWD",
    "KYD",
    "KZT",
    "LAK",
    "LBP",
    "LKR",
    "LRD",
    "LSL",
    "LYD",
    "MAD",
    "MDL",
    "MGA",
    "MKD",
    "MMK",
    "MNT",
    "MOP",
    "MRU",
    "MUR",
    "MVR",
    "MWK",
    "MXN",
    "MXV",
    "MYR",
    "MZN",
    "NAD",
    "NGN",
    "NIO",
    "NOK",
    "NPR",
    "NZD",
    "OMR",
    "PAB",
    "PEN",
    "PGK",
    "PHP",
    "PKR",
    "PLN",
    "PYG",
    "QAR",
    "RON",
    "RSD",
    "RUB",
    "RWF",
    "SAR",
    "SBD",
    "SCR",
    "SDG",
    "SEK",
    "SGD",
    "SHP",
    "SLE",
    "SLL",
    "SOS",
    "SRD",
    "SSP",
    "STN",
    "SVC",
    "SYP",
    "SZL",
    "THB",
    "TJS",
    "TMT",
    "TND",
    "TOP",
    "TRY",
    "TTD",
    "TVD",
    "TWD",
    "TZS",
    "UAH",
    "UGX",
    "USD",
    "USN",
    "UYI",
    "UYU",
    "UYW",
    "UZS",
    "VED",
    "VES",
    "VND",
    "VUV",
    "WST",
    "XAF",
    "XAG",
    "XAU",
    "XBA",
    "XBB",
    "XBC",
    "XBD",
    "XCD",
    "XDR",
    "XOF",
    "XPD",
    "XPF",
    "XPT",
    "XSU",
    "XTS",
    "XUA",
    "XXX",
    "YER",
    "ZAR",
    "ZMW",
    "ZWL",
}

SCRIPT_PATH = path.dirname(path.abspath(__file__))


def exit(output: OutputJSON):
    output_file_path = path.join(SCRIPT_PATH, "output/conversions.json")
    choice: str = "y"
    while True:
        if path.exists(output_file_path):
            print(
                f"Filename {output_file_path} already exists.\n",
                "Do you want to write to another file in 'output/'? y/n: ",
                end="",
                sep="",
            )
            choice = input()

        if choice.lower() == "y":
            output_file_name: str = input(
                "Enter your custom output file name for directory output/"
            )
            output_file_path: str = path.join(SCRIPT_PATH, "output", output_file_name)

            if path.exists(output_file_path):
                continue
            else:
                break

        print(
            "Do you want to: \n",
            "(1). override your existing file\n",
            f"(2). exit without saving to {output_file_path}?\n",
            "Default = None: ",
            end="",
            sep="",
        )
        choice: str = input()
        match choice:
            case "1":
                break
            case "2":
                quit(0)
            case _:
                print("Please make a correct choice.")

    with open(output_file_path, "w") as output_file:
        json.dump(
            obj=output.output_json,
            fp=output_file,
            ensure_ascii=False,
            indent=2,
        )

    print("Gracefully exiting...")


def parse_yyyy_mm_dd(date: datetime) -> str:
    parsed_month: str = str(date.month)
    if date.month < 10:
        parsed_month = "0" + parsed_month
    parsed_day: str = str(date.day)
    if date.day < 10:
        parsed_day = "0" + parsed_day
    return "-".join((str(date.year), parsed_month, parsed_day))


def parse_time(yyyy_mm_dd: str) -> str:
    if yyyy_mm_dd.lower().replace("'", "").replace('"', "") == "now":
        return parse_yyyy_mm_dd(datetime.now())

    separated_yyyy_mm_dd = yyyy_mm_dd.split("-")

    date: datetime

    if len(separated_yyyy_mm_dd) != 3:
        print("Please make sure to specify a --date / -d flag.")
        quit(1)

    try:
        date: datetime = datetime(
            year=int(separated_yyyy_mm_dd[0]),
            month=int(separated_yyyy_mm_dd[1]),
            day=int(separated_yyyy_mm_dd[2]),
        )
        if date.year < 2015:
            print("There's no data for anything before 2015-01-01.")
            quit(1)
        elif date > datetime.now():
            print(
                "This program doesn't have the capabilities to forsee future currency values... yet."
            )
            quit(1)
    except ValueError:
        print("Please make sure your YYYY-MM-DD format only uses integer values.")
        quit(1)

    return parse_yyyy_mm_dd(date)


def input_currency_value(prompt: str, output: OutputJSON) -> float:
    value_error = (
        "Please enter an integer or a decimal value with up to 2 floating points."
    )

    while True:
        amount: str = input(prompt)

        if not amount:
            print(value_error)
            continue

        if amount.lower() == "end":
            exit(output=output)
            quit(0)

        try:
            split = amount.split(".")
            if len(split) == 2 and len(split[1]) > 2:
                print(value_error)
                continue
            return float(amount)
        except ValueError:
            try:
                return float(amount + ".0")
            except ValueError:
                print(value_error)
                continue


def input_currency_type(prompt: str, output: OutputJSON):
    while True:
        currency: str = input(prompt)
        currency = currency.upper()

        if not currency:
            print("Please enter the 3 digit code of your target currency.")
            continue

        if currency.lower() == "end":
            exit(output)
            quit(0)

        if currency not in ISO_4217_CURRENCY_CODES:
            print("Please enter an ISO 4217 compliant currency code.")
            print(
                "https://en.wikipedia.org/wiki/ISO_4217#List_of_ISO_4217_currency_codes"
            )
            continue

        break

    return currency


def program_loop(
    fastforex_api_key: str,
    date: str,
    cached_conversions: CachedConversions,
    output: OutputJSON,
) -> None:
    print("Type 'end' at any time to gracefully exit the program.")

    amount: float = input_currency_value(prompt="Enter amount: ", output=output)
    from_currency: str = input_currency_type(
        prompt="Enter input currency: ", output=output
    )
    to_currency: str = input_currency_type(
        prompt="Enter target currency: ", output=output
    )

    if cached_conversions.stored_values.__contains__((from_currency, to_currency)):
        converted_amount: float = amount * cached_conversions.stored_values.__getitem__(
            (from_currency, to_currency)
        )
        output.append(
            date=date,
            amount=amount,
            base_currency=from_currency,
            target_currency=to_currency,
            converted_amount=converted_amount,
        )
        return None

    fastforex_request_url: str = f"https://api.fastforex.io/historical?date={date}&from={from_currency}&to={to_currency}&api_key={fastforex_api_key}"
    headers = {"accept": "application/json"}
    response: Response = get(fastforex_request_url, headers=headers)
    if response.status_code != 200:
        print("API response failed.")
        print(response)
        return None

    response_json: dict[str | dict[str, float], str | int] = response.json()
    converted_amount: float = amount * response_json["results"][to_currency]
    # Rounding down to the floor because it's finance.
    converted_amount = math.floor(converted_amount * 100) / 100
    converted_amount = float(str(f"{converted_amount:.2f}"))
    print(f"Converted amount: {converted_amount}")

    cached_conversions.stored_values[(from_currency, to_currency)] = converted_amount

    print(response_json)
    output.append(
        date=date,
        amount=amount,
        base_currency=from_currency,
        target_currency=to_currency,
        converted_amount=converted_amount,
    )
    print(output.output_json[0])


def main() -> None:
    parser = ArgumentParser(
        prog="CurrencyConversion.py",
        description="Converts user input value from one currency into another into a JSON file.",
    )
    parser.add_argument(
        "--date",
        "-d",
        type=str,
        default="",
        required=True,
        help="The date format is YYYY-MM-DD. You can also use 'now' as a shorthand for the current system day.",
    )

    args = parser.parse_args()

    date: str = parse_time(args.date)

    config: dict[str, str]

    with open(path.join(SCRIPT_PATH, "config.json"), "r") as config_file:
        config = json.load(config_file)

    fastforex_api_key: str = config["fast_forex_api_key"]
    # print(f"{fastforex_api_key}")

    cached_conversions: CachedConversions = CachedConversions()

    output: OutputJSON = OutputJSON()

    while True:
        program_loop(fastforex_api_key, date, cached_conversions, output)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(
            "\n",
            "Type out 'end' instead of forcing an exit because the program ",
            "won't write it's output otherwise!",
            sep="",
        )
        quit(1)
