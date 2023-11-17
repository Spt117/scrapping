import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
import base64
from io import BytesIO

def clean_name_for_path(name):
    return name.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')

def getImages(url, name):
    # Envoyer une requête HTTP pour obtenir le contenu de la page
    response = requests.get(url)

    # Analyser le contenu HTML de la page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Trouver toutes les images avec la classe 'el-image'
    ul = soup.find('ul', class_='uk-slideshow-items uk-width-1-1')
    des = soup.find('div', class_='uk-width-3-5@m')
    images = ul.find_all('img') + des.find_all('img', class_='el-image')

    # Nettoyer le nom pour le chemin du dossier
    clean_folder_name = clean_name_for_path(name)

    # Chemin du dossier où sauvegarder les images
    folder_path = 'images'

    # Assurer que le dossier existe
    folder_to_create = os.path.join(folder_path, clean_folder_name)
    if not os.path.exists(folder_to_create):
        os.makedirs(folder_to_create)

    # Parcourir chaque image et les télécharger
    for index, img in enumerate(images):
        if img.has_attr('src'):
            image_url = img['src']
            if image_url.endswith('.svg'):
                image_url = image_url.replace('.svg', '.png')
                image_url = image_url.replace('lhis.be', 'lhis.nl')

            # Gérer les images encodées en base64
            if image_url.startswith('data:image'):
                try:
                    image_data = image_url.split(',')[1]
                    image_bytes = base64.b64decode(image_data)
                    image = Image.open(BytesIO(image_bytes))
                    image_path = os.path.join(folder_to_create, f'{clean_folder_name}_{index + 1}.jpg')
                    image.save(image_path)
                except Exception as e:
                    print(f"Erreur lors du traitement de l'image base64 : {e}")

            # Gérer les images normales via HTTP
            elif image_url.startswith('http'):
                try:
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image_path = os.path.join(folder_to_create, f'{clean_folder_name}_{index + 1}.jpg')
                        with open(image_path, 'wb') as file:
                            file.write(image_response.content)
                except requests.RequestException as e:
                    print(f"Erreur lors du téléchargement de l'image : {e}")
