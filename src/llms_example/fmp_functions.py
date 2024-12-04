# Description

"""
This code include different functions to download data from Financial Modeling Prep.

Financial Modeling Prep gives us access to various historical financial data, such as 
financial statements, market data, metrics, ratios, etc.

"""

# References

'https://site.financialmodelingprep.com/developer/docs/#Financial-Statements-List'
'https://github.com/antoinevulcain/Financial-Modeling-Prep-API'

# Libraries 

import pandas as pd
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import certifi
import json
import datetime

import logging

#logging config
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Logger Config
logger = logging.getLogger('myAppLogger')

#%%


def earnings_calls(api_key: str, 
                   stocks: list[str], 
                   earnings_calls_start_year: int) -> dict:
    """
    Parameters
    ----------
    api_key : str
        FMP Api Key.
    stocks : list[str]
        List of tickers.
    earnings_calls_start_year : int
        Initial year.

    Returns
    -------
    dict
        A dictionary of dictionaries with pandas
        dataframes, where first key is 
        the ticker and the other more are
        keys as years.

    """
    current_year = datetime.date.today().year

    earnings_calls = {}

    for stock in stocks:
        year = earnings_calls_start_year
        stock_calls = {}

        try:
            while year <= current_year:
                url = (
                    f'https://financialmodelingprep.com/api/v4/batch_earning_call_transcript/'
                    f'{stock}?year={year}&apikey={api_key}'
                )
                try:
                    response = urlopen(url, cafile=certifi.where())
                    data = json.loads(response.read().decode("utf-8"))
                    if not data:
                        logger.warning(f"No data returned for {stock} in year {year}.")
                        year += 1
                        continue

                    df = pd.DataFrame(data)
                    if 'date' not in df.columns:
                        logger.warning(f"Missing 'date' column for {stock} in year {year}.")
                        year += 1
                        continue

                    stock_calls[year] = df.set_index('date')
                
                except HTTPError as http_err:
                    logger.error(f"HTTP error for {stock} in year {year}: {http_err}")
                except URLError as url_err:
                    logger.error(f"URL error for {stock} in year {year}: {url_err}")
                except ValueError as val_err:
                    logger.error(f"Error decoding JSON for {stock} in year {year}: {val_err}")
                except Exception as e:
                    logger.error(f"Unexpected error for {stock} in year {year}: {e}")

                year += 1
            
            earnings_calls[stock] = stock_calls

        except Exception as e:
            logger.error(f"Failed to fetch earnings calls for ticker {stock}: {e}")

    return earnings_calls
