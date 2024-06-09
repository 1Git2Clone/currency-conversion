# Applica assessment

Related to [this page containing all the requirements](https://www.appolica.com/assessment).

A program that converts user input value from one currency into another into a
`JSON` file.

## Setting up

Head to [FastFortex](https://console.fastforex.io/auth/signin) and make an
account for an API key.

Add the API key in a `config.json` file in the root of this repository. The
file format should be like this

```json
{
  "fast_forex_api_key": "your-key-here | check out https://console.fastforex.io/auth/signin"
}
```

It's necessary for the variable to be called `fast_fortex_api_key`.

Additionally you need to install requests if you haven't already. You can do it
in 2 ways (i recommend using the [requirements.txt](requirements.txt) one).

```sh
pip install -r requirements.txt # NOTE: in the project root.
# Or
pip install requests
```

Then it's a manner of running the app.

```sh
python3 CurrencyConversion.py YYYY-MM-DD
```

Replace the `YYYY-MM-DD` part with the year-month-day you wish to do your
currency conversion in.

> [!NOTE]
> Free accounts are limited to 14 days back in time and the service works for
> dates after 2015-01-01.
