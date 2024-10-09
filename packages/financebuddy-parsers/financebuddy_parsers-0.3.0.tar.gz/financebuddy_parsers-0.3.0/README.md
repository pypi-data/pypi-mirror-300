# financebuddy-parsers

List of financial data parsers supported by [FinanceBuddy](https://github.com/cedricduriau/financebuddy).

### What is FinanceBuddy?

Please read the [README](https://github.com/cedricduriau/financebuddy/blob/main/README.md).

### What are parsers?

A parser is a tool transforming financial data from a specific bank into a centralized format. Every parser is linked to a format and an extension.

- the `format` is driven by the bank the data is coming from
- the `extension` is driven by the file format the data is stored in

### Available sources

| Bank                          | Format  | Extension  |
--------------------------------|---------|------------|
| BNP Parisbas Fortis (Belgium) | bnp-be  | csv        |
| ING (Belgium)                 | ing-be  | csv        |

## FAQ

### Why do some parsers mention a country?

Some banks have a specific format per country. The format or even the extension could be different. To differenciate them, the country code is embedded in the format for clarity.

An example is between ING for Belgium or the Netherlands. Both export a .CSV file but the contents differ.

## Development

### Install
```sh
python -m venv .env
source .env/bin/activate
make install-dev
```
