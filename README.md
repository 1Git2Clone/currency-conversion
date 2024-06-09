# Appolica assessment

[![GH_Build Icon]][GH_Build Status]&emsp;[![License Icon]][LICENSE]

[GH_Build Icon]: https://img.shields.io/github/actions/workflow/status/1git2clone/currency-conversion/pylint.yml?branch=main
[GH_Build Status]: https://github.com/1git2clone/currency-conversion/actions?query=branch%3Amaster
[License Icon]: https://img.shields.io/badge/license-MIT-blue.svg
[LICENSE]: LICENSE

Related to [this page containing all the requirements](https://www.appolica.com/assessment).

A program that converts user input value from one currency into another into a
`JSON` file.

## Features

The currency converter takes a date, value and your desired input and output
currencies in an infinite loop. In order to exit the app you just need to type
`end`. After typing `end` you'll get a few additional prompts telling you to
save your file in `output/conversions.json` and if there's already a saved file
from there then you can choose to:

- Write to a new file (only in `output/`).

- Override the existing file.

- Discard your changes.

In the case where you want to use today's date, there's a neat shorthand for
the `--date` / `-d` command with an alias of `now`. With it you can use today's
date without having to type it out like this:

```sh
python3 CurrencyConversion.py --date=now
# or
python3 CurrencyConversion.py -d=now
# Trailing/leading quotes don't affect it either
python3 CurrencyConversion.py -d="now"
# It's also case-insensitive
python3 CurrencyConversion.py -d="nOw"
```

## Setting up

Head to [FastForex](https://console.fastforex.io/auth/signin) and make an
account for an API key.

Add the API key in a `config.json` file in the root of this repository. The
file format should be like this

```json
{
  "fast_forex_api_key": "your-key-here | check out https://console.fastforex.io/auth/signin"
}
```

It's necessary for the variable to be called `fast_forex_api_key`.

Additionally you need to install requests if you haven't already. You can do it
in 2 ways (i recommend using the [requirements.txt](requirements.txt) one).

```sh
pip install -r requirements.txt # NOTE: in the project root.
# Or
pip install requests
```

Then it's a manner of running the app.

```sh
python3 CurrencyConversion.py -d=YYYY-MM-DD
# or
python3 CurrencyConversion.py --date=YYYY-MM-DD
```

Replace the `YYYY-MM-DD` part with the year-month-day you wish to do your
currency conversion in.

> [!NOTE]
> Free accounts are limited to 14 days back in time and their service works for
> dates after 2015-01-01.
