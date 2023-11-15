import requests
from bs4 import BeautifulSoup
import csv
import re

parent_folder = 'images'
filename = 'produits.csv'

def getInfos(url):

    # Envoyer une requête HTTP pour obtenir le contenu de la page
    response = requests.get(url)

    # Analyser le contenu HTML de la page
    soup = BeautifulSoup(response.content, 'html.parser')

    #Titre du produit
    product_title = soup.find('h1')
    product_title_text = ' '.join(product_title.get_text().strip().split())

    #Arborescence
    arborescence = soup.find('div', class_='uk-first-column')
    arborescence_lis = arborescence.find_all('li') if arborescence else []
    arborescence_text = '|'.join(li.get_text().strip() for li in arborescence_lis)

    # Prix
    product_price = soup.find('span', class_='amount').get_text().strip().replace(',', '').replace('-', '')

    # Description
    description = soup.find('p', class_='uk-margin-small')
    description_text = ' '.join(description.get_text().strip().split())

    #couleurs
    elements_with_data_kleur = soup.find_all(attrs={"data-kleur": True})
    # Récupérer les valeurs de l'attribut 'data-kleur' de ces éléments
    data_kleur_values = [element['data-kleur'] for element in elements_with_data_kleur]
    # Vérifier si la liste 'data_kleur_values' contient des éléments
    if len(data_kleur_values) > 0:
    # Joindre les éléments de la liste avec une virgule
        result_text = ', '.join(data_kleur_values)
    else:
    # Si la liste est vide, définir le texte à 'None'
        result_text = 'None'

    # Volume
    # Trouver le premier élément 'ul' avec la classe 'specificaties'
    ul_element = soup.find('ul', class_='specificaties')
    # Vérifier si l'élément ul a été trouvé
    if ul_element:
        # Créer un tableau avec tous les éléments 'dl' dans cet 'ul'
        dl_elements = ul_element.find_all('dl')
        # Trouver le 'dl' qui contient le texte 'Volume total'
        for dl in dl_elements:
            if 'Volume total' in dl.get_text():
                if 'Volume total' in dl.get_text():
                    dd_element = dl.find('dd').get_text().strip()
                else:
                    dd_element = 'None'   
            else:
                    dd_element = 'None'  
            print(dd_element)

    # Dimensions
    elements_with_dimensions = soup.find_all(text=lambda text: 'Dimensions' in text)
    # Extraire et afficher les dimensions du premier élément correspondant
    if len(elements_with_dimensions) > 0:
        dimentions = elements_with_dimensions[0].split(':')[1].strip()
    else:
        dimentions = 'None'

    # Caractéristiques techniques

    # Ouvrir le fichier en mode append ('a') pour ajouter des données sans écraser les données existantes
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Ajouter le nom du produit dans la colonne "Nom"
        # Assurez-vous que le nombre de colonnes dans writer.writerow() correspond au nombre de colonnes dans le fichier CSV
        writer.writerow([product_title_text, arborescence_text, result_text, product_price, description_text, dd_element, dimentions, '']) 



def checkRedirection(url):
    response = requests.get(url, allow_redirects=True)

    # Vérifier si une redirection a eu lieu
    if response.history:
        print("Redirigé de:", response.history[0].url)
        print("Redirigé vers:", response.url)
        return False
    else:
        return True