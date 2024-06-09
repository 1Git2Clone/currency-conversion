def main():
    as_float: float
    while True:
        amount: str = input("Enter amount: ")
        if not amount:
            continue
        try:
            split = amount.split('.')
            if len(split) == 2 and len(split[1]) > 2:
                continue
            as_float = float(amount)
            break;
        except ValueError:
            try:
                as_float = float(amount + ".0")
                break
            except ValueError:
                print("Please enter an integer or a decimal value with up to 2 floating points.")
                continue

if __name__ == "__main__":
    main()
