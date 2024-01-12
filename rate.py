import requests


def rate(currency):
    r = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json")
    for x in r.json():
        if x["cc"] == currency:
            return round(x["rate"], 2)
    return 1
