import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, unquote

def getDocuments(url, folder_name):
    # Envoyer une requête HTTP pour obtenir le contenu de la page
    response = requests.get(url)

    # Analyser le contenu HTML de la page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Trouver l'élément <ul> avec les classes spécifiées
    target_ul = soup.find('ul', class_='uk-list uk-list-divider uk-margin-remove-bottom')

    if target_ul:
        # Parcourir tous les éléments <li> dans la liste
        for li in target_ul.find_all('li'):
            link = li.find('a')
            if link and 'href' in link.attrs:
                document_url = link['href']
                split_url = urlsplit(document_url)
                file_name = folder_name+'_'+li.get_text(strip=True).replace(' ', '_').replace('/', '_')

                # Détecter l'extension du fichier à partir de l'URL
                file_extension = os.path.splitext(unquote(split_url.path))[1].lower()
                
                # Si aucune extension n'est trouvée, supposer que c'est un PDF
                if not file_extension:
                    file_extension = '.pdf'

                file_path = os.path.join('documents', folder_name, file_name + file_extension)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                # Vérifier si l'URL est un PDF ou une image
                try:
                    # Télécharger le document
                    document_response = requests.get(document_url)

                    if document_response.status_code == 200:
                        with open(file_path, 'wb') as file:
                            file.write(document_response.content)

                        # print(f'Document téléchargé : {file_path}')
                except requests.RequestException as e:
                    print(f'Erreur lors du téléchargement du document : {e}')
            else:
                print('Pas de lien trouvé dans ce <li>.')
    else:
        print('Liste spécifiée non trouvée dans la page.')