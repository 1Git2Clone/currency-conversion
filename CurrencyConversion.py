def valid_currency(value: str) -> bool:
    try:
        float(value)
        split = value.split('.')
        if len(split[1]) > 2:
            return False;
    except:
        try:
            int(value)
        except:
            return False;

    return True;

def main():
    while True:
        amount: str = input("Enter amount: ")
        if valid_currency(amount):
            break
        print("Please enter an integer or a decimal value with up to 2 floating points.")

    parsed_amount = float(amount)

if __name__ == "__main__":
    main()
