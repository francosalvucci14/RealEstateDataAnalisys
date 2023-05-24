# Importare moduli
import requests
import pandas as pd
from bs4 import BeautifulSoup
import sys
import getopt
import math
import time
import csv

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
# Indirizzo sito web
def FindNumber(string):
    empty_string = ""
    for m in string:
        if m.isdigit():
            empty_string = empty_string+m
    return int(empty_string)

def SearchNumberOfElements(type,zone):
    url = f"https://www.immobiliare.it/vendita-{type}/roma/{zone}/?criterio=rilevanza&noAste=1&classeEnergetica=8"
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
    print(f"Numeri di elementi trovati : {cycle}")
    pagine = math.ceil(cycle/25)
    print("Inizio scansione e raccolta dati")
    #printProgressBar(0, cycle, prefix = 'Progress:', suffix = 'Complete', length = 50)
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
            time.sleep(0.1)
            printProgressBar(i, pagine, prefix = 'Progress:', suffix = 'Complete', length = 50)
            url = f"https://www.immobiliare.it/vendita-{arg_type}/roma/{arg_zone}/?criterio=rilevanza&pag={i}&noAste=1&classeEnergetica=8"
            #print(url)
            # Eseguire richiesta GET
            response = requests.get(url)
            # Analizzare documento HTML del codice sorgente con BeautifulSoup
            html = BeautifulSoup(response.text, 'html.parser')
            # Estrarre tutte le citazioni e gli autori dal documento HTML
            locali_html = html.find_all('a', class_="in-card__title")
            price_html = html.find_all(
                'li', class_="nd-list__item in-feat__item in-feat__item--main in-realEstateListCard__features--main")
            # da trasformare locali e prices in set, e farne l'unione
            locali = list()
            print(len(locali_html),len(price_html))
            for locale in locali_html:
                locali.append(locale.text)
            # Raccogliere gli autori in un elenco
            prices = list()
            for price in price_html:
                if price.text == 'Prezzo su richiesta':
                    price.text = "0"
                prices.append(price.text)      
                      
            locali_tot += locali
            price_tot += prices
    print(len(locali_tot),len(price_tot))
    return locali_tot, price_tot, arg_type


locali, prezzi,tipo_immobile = search(sys.argv)
media_prezzo = 0
# somma_prezzi, count_locali, media_prezzo = 0, 0, 0
# prezzi_media = [0]*len(prezzi)
# print(prezzi_media)
# for i in range(len(prezzi)):
#     prezzi_media[i] = prezzi[i].replace("€","")
#     print(prezzi_media[i])
#     if ' ' in prezzi_media[i]:
#         prezzi_media_split=prezzi_media[i].split(" ")
#         somma_prezzi+=float(prezzi_media_split[0])
#     else:
#         somma_prezzi+=float(prezzi_media[i])
#     count_locali+=1
# print(somma_prezzi)
# media_prezzo = somma_prezzi/count_locali
print(len(locali),len(prezzi))
print("Elaboro csv personalizzato")
dict = {'Locali': locali, 'Prezzi': prezzi}
df = pd.DataFrame(dict)
df.to_csv(f'Immobiliare_{tipo_immobile}.csv', index=False, encoding='utf-8')

print("Fine elaborazione.")
