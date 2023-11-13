import requests
from bs4 import BeautifulSoup
from getProduct import getInfos
from getProduct import checkRedirection


import os
import csv

# création du csv
filename = 'produits.csv'

# En-têtes des colonnes
headers = ['Nom','Arborescence', 'Prix', 'Description', 'Couleurs disponibles', 'Volume', 'Dimensions', 'Caractéristiques techniques']

# Créer le fichier CSV avec les en-têtes
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)


index = 0
processed_products = []
url = 'https://www.liebherr.be/fr/refrigeration/modeles/'  # Remplacez par l'URL réelle de la page
parent_folder = 'réfrégirateurs '
# Envoyer une requête HTTP pour obtenir le contenu de la page
response = requests.get(url)

# Analyser le contenu HTML de la page
soup = BeautifulSoup(response.content, 'html.parser')

# Trouver toutes les div avec la classe 'product'
product_divs = soup.find_all('div', class_='product')

# Stocker les divs dans un tableau
products = [str(div) for div in product_divs]

for product in products:
# product = products[1]
#début de la boucle


    soup = BeautifulSoup(product, 'html.parser')

    # Trouver la balise <a> avec la classe 'url'
    url_tag = soup.find('a', class_='product_url')

    # Extraire l'attribut href, qui contient le lien
    if url_tag and url_tag.has_attr('href'):
        product_url = url_tag['href']
        if checkRedirection(product_url):
            getInfos(product_url)
        index += 1


#fin de la boucle
        

print("Nombre de produits traités :", index)

