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
    amount: float = input_currency_value(prompt="Enter amount: ")
    from_currency: str = input_currency_type(prompt="Enter input currency: ")
    to_currency: str = input_currency_type(prompt="Enter target currency: ")


if __name__ == "__main__":
    main()
