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


## default run
```
python main.py                            
[
  {
    "14.09.2023": {
      "EUR": {
        "sale": 41.1,
        "purchase": 40.1
      },
      "USD": {
        "sale": 38.0,
        "purchase": 37.4
      }
    }
  },
  {
    "13.09.2023": {
      "EUR": {
        "sale": 41.1,
        "purchase": 40.1
      },
      "USD": {
        "sale": 38.0,
        "purchase": 37.4
      }
    }
  }
]

```


## currencies
```
python main.py   --currencies EUR,USD,GBP                 
[
  {
    "14.09.2023": {
      "EUR": {
        "sale": 41.1,
        "purchase": 40.1
      },
      "GBP": {
        "sale": 47.46,
        "purchase": 45.4
      },
      "USD": {
        "sale": 38.0,
        "purchase": 37.4
      }
    }
  },
  {
    "13.09.2023": {
      "EUR": {
        "sale": 41.1,
        "purchase": 40.1
      },
      "GBP": {
        "sale": 47.46,
        "purchase": 45.4
      },
      "USD": {
        "sale": 38.0,
        "purchase": 37.4
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
        "sale": 41.1,
        "purchase": 40.1
      },
      "GBP": {
        "sale": 47.46,
        "purchase": 45.4
      },
      "USD": {
        "sale": 38.0,
        "purchase": 37.4
      }
    }
  },
  {
    "13.09.2023": {
      "EUR": {
        "sale": 41.1,
        "purchase": 40.1
      },
      "GBP": {
        "sale": 47.46,
        "purchase": 45.4
      },
      "USD": {
        "sale": 38.0,
        "purchase": 37.4
      }
    }
  },
  {
    "12.09.2023": {
      "EUR": {
        "sale": 41.0,
        "purchase": 40.0
      },
      "GBP": {
        "sale": 47.39,
        "purchase": 45.45
      },
      "USD": {
        "sale": 37.9,
        "purchase": 37.3
      }
    }
  },
  {
    "11.09.2023": {
      "EUR": {
        "sale": 41.0,
        "purchase": 40.0
      },
      "GBP": {
        "sale": 47.45,
        "purchase": 45.51
      },
      "USD": {
        "sale": 37.9,
        "purchase": 37.3
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
        "sale": 8.84,
        "purchase": 8.46
      }
    }
  },
  {
    "13.09.2023": {
      "PLN": {
        "sale": 8.84,
        "purchase": 8.46
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