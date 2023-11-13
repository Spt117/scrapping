import requests
from bs4 import BeautifulSoup
import os
import csv

index = 1
processed_products = []
url = 'https://www.liebherr.be/fr/refrigeration/modeles/'  # Remplacez par l'URL réelle de la page
parent_folder = 'images'
# Envoyer une requête HTTP pour obtenir le contenu de la page
response = requests.get(url)

# Analyser le contenu HTML de la page
soup = BeautifulSoup(response.content, 'html.parser')

# Trouver toutes les div avec la classe 'product'
product_divs = soup.find_all('div', class_='product')

# Stocker les divs dans un tableau
products = [str(div) for div in product_divs]

with open('product_names.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Écrire l'en-tête du fichier CSV
    writer.writerow(['Noms'])

    for product in products:
    # Analyser ce div avec Beautiful Soup
        soup = BeautifulSoup(product, 'html.parser')

    # Trouver la balise avec la classe 'product_title'
        product_title_tag = soup.find(class_='product_titel')
        if product_title_tag:
            product_title = product_title_tag.get_text().strip()
            # Ajouter le titre du produit à la liste des produits traités
            processed_products.append(product_title)
        product_image_tag = soup.find('img', class_='product_image')

    # Extraire et afficher le texte du titre
        product_title = product_title_tag.get_text().strip()
        # print("Titre du produit :", product_title)

        folder_path = os.path.join(parent_folder, product_title)
        os.makedirs(folder_path, exist_ok=True)
        product_image_tag = soup.find('img', class_='product_image')

        if product_image_tag:
        # Obtenir l'URL de l'image
         image_url = product_image_tag['src']


        # Télécharger l'image
        response = requests.get(image_url)

        if response.status_code == 200:
            # Nom de fichier de l'image dans le sous-dossier
            image_filename = os.path.join(folder_path, 'product_image.jpg')

            # Enregistrer l'image dans le fichier
            with open(image_filename, 'wb') as file:
                file.write(response.content)
            print(f"Image téléchargée avec succès dans le dossier: {folder_path}")
            index += 1
        else:
            print("Impossible de télécharger l'image.")


    # Créer ou ouvrir un fichier CSV pour écrire les données


        soup = BeautifulSoup(product, 'html.parser')

        # Trouver la balise avec la classe 'product_title'
        product_title_tag = soup.find(class_='product_titel')

        if product_title_tag:
            product_title = product_title_tag.get_text().strip()
            print("Titre du produit :", product_title)

            # Écrire le nom du produit dans le fichier CSV
            writer.writerow([product_title])
        else:
            print("Titre du produit non trouvé.")


print(len(products))

print(index)