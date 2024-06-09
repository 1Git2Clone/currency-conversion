from argparse import ArgumentParser

ISO_4217_CURRENCY_CODES: set = {
    'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN',
    'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BOV',
    'BRL', 'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHE', 'CHF',
    'CHW', 'CLF', 'CLP', 'CNY', 'COP', 'COU', 'CRC', 'CUC', 'CUP', 'CVE',
    'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD',
    'FKP', 'FOK', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ',
    'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'INR',
    'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR',
    'KID', 'KMF', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD',
    'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU',
    'MUR', 'MVR', 'MWK', 'MXN', 'MXV', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO',
    'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN',
    'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG',
    'SEK', 'SGD', 'SHP', 'SLE', 'SLL', 'SOS', 'SRD', 'SSP', 'STN', 'SVC',
    'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TVD',
    'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'USN', 'UYI', 'UYU', 'UYW', 'UZS',
    'VED', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XAG', 'XAU', 'XBA', 'XBB',
    'XBC', 'XBD', 'XCD', 'XDR', 'XOF', 'XPD', 'XPF', 'XPT', 'XSU', 'XTS',
    'XUA', 'XXX', 'YER', 'ZAR', 'ZMW', 'ZWL'
}

def input_currency_value(prompt: str) -> float:
    value_error = "Please enter an integer or a decimal value with up to 2 floating points."

    while True:
        amount: str = input(prompt)

        if not amount:
            print(value_error)
            continue

        try:
            split = amount.split('.')
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

def input_currency_type(prompt: str):
    while True:
        currency: str = input(prompt)

        if not currency:
            print("Please enter the 3 digit code of your target currency.")
            continue

        if currency.upper() not in ISO_4217_CURRENCY_CODES:
            print("Please enter an ISO 4217 compliant currency code.")
            print("https://en.wikipedia.org/wiki/ISO_4217#List_of_ISO_4217_currency_codes")
            continue

        break

    return currency


def main():
    parser = ArgumentParser(
                    prog='CurrencyConversion.py',
                    description='Converts user input value from one currency into another into a JSON file.')
    parser.add_argument(
        '--date', '-d', \
        type=str, \
        default="", \
        help='The SauceNAO API Rate Limit toggle (On by default)', \
    )

    args = parser.parse_args()

    yyyy_mm_dd: str = args.date.split('-')

    if not yyyy_mm_dd or \
       len(yyyy_mm_dd) != 3:
        print("Please make sure to specify a --date / -d flag.")
        return 1

    try:
        int(yyyy_mm_dd[0])
        int(yyyy_mm_dd[1])
        int(yyyy_mm_dd[2])
    except ValueError:
        print("Please make sure your YYYY-MM-DD format only uses integer values.")
        return 1

    amount: float = input_currency_value(prompt="Enter amount: ")
    from_currency: str = input_currency_type(prompt="Enter input currency: ")
    to_currency: str = input_currency_type(prompt="Enter target currency: ")


if __name__ == "__main__":
    main()
