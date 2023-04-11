# Importare moduli
import requests
import pandas as pd
from bs4 import BeautifulSoup
import sys
import getopt
# Indirizzo sito web

def search():
    locali_tot = []
    price_tot = []
    for i in range(1, 10):
        url = f"https://www.immobiliare.it/vendita-case/roma/centocelle/?criterio=rilevanza&pag={i}&noAste=1"
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
        # Per eseguire il test, combinare e visualizzare le voci di entrambi gli elenchi
        # for t in zip(locali,prices):
        #    print(t)
        # Salvare le citazioni e gli autori in un file CSV nella directory corrente
        # Aprire il file con Excel / LibreOffice, ecc.
        # with open('./citazioni.csv', 'w') as csv_file:
        #     csv_writer = csv.writer(csv_file, dialect='excel')
        #     csv_writer.writerows(zip(quotes, authors))
        locali_tot += locali
        price_tot += prices

    return locali_tot, price_tot


locali, prezzi = search()
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
