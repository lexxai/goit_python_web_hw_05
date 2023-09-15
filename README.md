# goit_python_web_hw_05


```
usage: main.py [-h] [--days DAYS] [--currencies CURRENCIES] [--verbose]

Get exchangeRate from Bank: AUD,AZN,BYN,CAD,CHF,CNY,CZK,DKK,EUR,GBP,GEL,HUF,ILS,JPY,KZT,MDL,NOK,PLN,SEK,SGD,TMT,TRY,USD,UZS,XAU   

options:
  -h, --help            show this help message and exit
  --days DAYS           How many datys need to show reqults, max. 10 days, default: 2
  --currencies CURRENCIES
                        currencies for list. Allowed: items
                        "AUD,AZN,BYN,CAD,CHF,CNY,CZK,DKK,EUR,GBP,GEL,HUF,ILS,JPY,KZT,MDL,NOK,PLN,SEK,SGD,TMT,TRY,USD,UZS,XAU".    
                        Please use coma separeted list. default: EUR,USD
  --verbose             print deailed log
```


## currencies
```
python main.py   --currencies EUR,USD,GBP                 
[
  {
    "14.09.2023": {
      "EUR": {
        "sale": 39.2674,
        "purchase": 39.2674
      },
      "GBP": {
        "sale": 45.6175,
        "purchase": 45.6175
      },
      "USD": {
        "sale": 36.5686,
        "purchase": 36.5686
      }
    }
  },
  {
    "13.09.2023": {
      "EUR": {
        "sale": 39.1906,
        "purchase": 39.1906
      },
      "GBP": {
        "sale": 45.5974,
        "purchase": 45.5974
      },
      "USD": {
        "sale": 36.5686,
        "purchase": 36.5686
      }
    }
  }
]
```
## days 
```
python main.py   --currencies EUR,USD,GBP --days 4 
[
  {
    "14.09.2023": {
      "EUR": {
        "sale": 39.2674,
        "purchase": 39.2674
      },
      "GBP": {
        "sale": 45.6175,
        "purchase": 45.6175
      },
      "USD": {
        "sale": 36.5686,
        "purchase": 36.5686
      }
    }
  },
  {
    "13.09.2023": {
      "EUR": {
        "sale": 39.1906,
        "purchase": 39.1906
      },
      "GBP": {
        "sale": 45.5974,
        "purchase": 45.5974
      },
      "USD": {
        "sale": 36.5686,
        "purchase": 36.5686
      }
    }
  },
  {
    "12.09.2023": {
      "EUR": {
        "sale": 39.1979,
        "purchase": 39.1979
      },
      "GBP": {
        "sale": 45.7619,
        "purchase": 45.7619
      },
      "USD": {
        "sale": 36.5686,
        "purchase": 36.5686
      }
    }
  },
  {
    "11.09.2023": {
      "EUR": {
        "sale": 39.1247,
        "purchase": 39.1247
      },
      "GBP": {
        "sale": 45.6413,
        "purchase": 45.6413
      },
      "USD": {
        "sale": 36.5686,
        "purchase": 36.5686
      }
    }
  }
]
```
## verbose
```
python main.py   --currencies PLN --days 2 --verbose         
2023-09-15 04:04:26,151  Get request for 2 days
2023-09-15 04:04:26,151  Get request for: 14.09.2023
2023-09-15 04:04:26,151  Get request for: 13.09.2023
2023-09-15 04:04:26,151  Waing result for 2 requests
[
  {
    "14.09.2023": {
      "PLN": {
        "sale": 8.4988,
        "purchase": 8.4988
      }
    }
  },
  {
    "13.09.2023": {
      "PLN": {
        "sale": 8.405,
        "purchase": 8.405
      }
    }
  }
]


```

## Progress bas + verbose
```
python main.py   --currencies PLN --days 10 --verbose 
2023-09-15 04:16:35,705  Get request for 10 days
2023-09-15 04:16:35,705  Get request for: 14.09.2023
2023-09-15 04:16:35,705  Get request for: 13.09.2023
2023-09-15 04:16:35,705  Get request for: 12.09.2023
2023-09-15 04:16:35,705  Get request for: 11.09.2023
2023-09-15 04:16:35,705  Get request for: 10.09.2023
2023-09-15 04:16:35,705  Get request for: 09.09.2023
2023-09-15 04:16:35,705  Get request for: 08.09.2023
2023-09-15 04:16:35,705  Get request for: 07.09.2023
2023-09-15 04:16:35,705  Get request for: 06.09.2023
2023-09-15 04:16:35,705  Get request for: 05.09.2023
2023-09-15 04:16:35,705  Waing result for 10 requests
 30%|███████████████████████████▉                                                                 | 3/10 [00:10<00:26,  3.83s/it]
```