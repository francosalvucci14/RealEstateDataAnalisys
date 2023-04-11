# Importare moduli
import requests
import pandas as pd
from bs4 import BeautifulSoup
import sys
import getopt
import math
# Indirizzo sito web
def FindNumber(string):
    empty_string = ""
    for m in string:
        if m.isdigit():
            empty_string = empty_string+m
    return int(empty_string)

def SearchNumberOfElements(type,zone):
    url = f"https://www.immobiliare.it/vendita-{type}/roma/{zone}/?criterio=rilevanza&noAste=1"
    response = requests.get(url)
        # Analizzare documento HTML del codice sorgente con BeautifulSoup
    html = BeautifulSoup(response.text, 'html.parser')
    number_of_el = html.find('div', class_="in-searchList__title")
    value = number_of_el.text
    split = value.split()
    number = split[0]
    return int(number)

def search(argv):
    # Import argument from terminal
    arg_zone = ""
    arg_type = ""
    arg_help = "Help: -z <zone> -t <type>".format(argv[0])
    
    try:
        opts, args = getopt.getopt(argv[1:], "hz:t:", ["help", "zone=", 
        "type="])
    except:
        print(arg_help)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-z", "--zone"):
            arg_zone = arg
        elif opt in ("-t", "--type"):
            arg_type = arg

    if arg_type == "all":
        arg_type = "case"
    locali_tot = []
    price_tot = []
    cycle = SearchNumberOfElements(arg_type,arg_zone)
    print(cycle)
    pagine = math.ceil(cycle/25)
    if pagine  == 1:
        url = f"https://www.immobiliare.it/vendita-{arg_type}/roma/{arg_zone}/?criterio=rilevanza&noAste=1"
        print(url)
        # Eseguire richiesta GET
        response = requests.get(url)
        # Analizzare documento HTML del codice sorgente con BeautifulSoup
        html = BeautifulSoup(response.text, 'html.parser')
        # Estrarre tutte le citazioni e gli autori dal documento HTML
        locali_html = html.find_all('a', class_="in-card__title")
        price_html = html.find_all(
            'li', class_="nd-list__item in-feat__item in-feat__item--main in-realEstateListCard__features--main")
        # Raccogliere le citazioni in un elenco
        locali = list()
        for locale in locali_html:
            locali.append(locale.text)
        # Raccogliere gli autori in un elenco
        prices = list()
        for price in price_html:
            prices.append(price.text)

        locali_tot += locali
        price_tot += prices
    else:
        for i in range(1, pagine+1):
            url = f"https://www.immobiliare.it/vendita-{arg_type}/roma/{arg_zone}/?criterio=rilevanza&pag={i}&noAste=1"
            print(url)
            # Eseguire richiesta GET
            response = requests.get(url)
            # Analizzare documento HTML del codice sorgente con BeautifulSoup
            html = BeautifulSoup(response.text, 'html.parser')
            # Estrarre tutte le citazioni e gli autori dal documento HTML
            locali_html = html.find_all('a', class_="in-card__title")
            price_html = html.find_all(
                'li', class_="nd-list__item in-feat__item in-feat__item--main in-realEstateListCard__features--main")
            # Raccogliere le citazioni in un elenco
            locali = list()
            for locale in locali_html:
                locali.append(locale.text)
            # Raccogliere gli autori in un elenco
            prices = list()
            for price in price_html:
                prices.append(price.text)

            locali_tot += locali
            price_tot += prices

    return locali_tot, price_tot


locali, prezzi = search(sys.argv)
somma_prezzi, count_locali, media_prezzo = 0, 0, 0
# for i in range(len(prezzi)):
#     prezzi[i] = prezzi[i].replace("€","")
#     print(prezzi[i])
#     somma_prezzi+=float(prezzi[i])
#     count_locali+=1
# print(somma_prezzi)
# media_prezzo = somma_prezzi/count_locali
df = pd.DataFrame({'Locali': locali, 'Prezzi': prezzi,
                  'Media prezzo:': media_prezzo})
df.to_csv('Immobiliare.csv', index=False, encoding='utf-8')
