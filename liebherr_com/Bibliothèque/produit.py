from bs4 import BeautifulSoup
import csv
from pyppeteer import launch
import os
import requests
import re


parent_folder = 'images'
filename = 'produits.csv'



async def produit(url):
    try:
        browser = await launch()
        page = await browser.newPage()
        await page.goto(url, waitUntil='networkidle0')
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')

        #Titre du produit
        title = soup.find('h1')
        product_title = ' '.join(title.get_text().strip().split())
        product_title_text = re.sub(r'[\\/*?:"<>|]', '_', product_title)
        print(product_title_text)

        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if product_title_text in row:
                    print(f"Produit '{product_title_text}' existe déjà dans le fichier CSV.")
                    return

        # #Arborescence
        campaign_divs = soup.find_all('div', class_='breadcrumb')
        arborescence = ' / '.join(campaign_divs[0].get_text().strip().split())

        #Description
        description = soup.find('section', class_='singleRow article_module text_img_module')
        description_sections = description.find_all('section', class_='text description')

        description_text = ""
        for section in description_sections:
            # Trouver le h3 et le paragraphe dans la section
            h3 = section.find('h3')
            paragraph = section.find('p')

            # Vérifier si h3 et le paragraphe existent
            if h3 and paragraph:
                h3_text = f'{h3.get_text(strip=True)}'
                paragraph_text = paragraph.get_text(strip=True)

                # Ajouter au texte formaté
                description_text += h3_text + "\r\n" + paragraph_text + "\r\n\r\n"


        # Caractéristiques
        data_table_div = soup.find('div', class_='data_table_module')
        features = ""
        # Vérifier si la div data_table_div a été trouvée
        rows = data_table_div.find_all('div', class_='data_table_module__row')
        for row in rows:
            spans = row.find_all('span')
            # Vérifier s'il y a bien deux spans dans la row
            span1_text = spans[0].get_text(strip=True)
            span2_text = spans[2].get_text(strip=True)
            # Ajouter au texte formaté
            features += f"{span1_text} : {span2_text}\r\n"

        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([product_title_text, arborescence, description_text, features]) 



        # Images
        divImages = soup.find('div', class_='zoom-gallery layerSlider')
        divIcons = soup.find('div', class_='featureIcons')
        # Chemin du dossier pour les images
        folder_path = "images"
        os.makedirs(folder_path, exist_ok=True)
        # Trouver tous les liens d'image dans l'élément <ul>
        images = divImages.find_all('img')
        icons = divIcons.find_all('img') 
        all_images = images + icons
        for index, img in enumerate(all_images, start=1):
            img_url = 'https://home.liebherr.com' + img.get('src')
            if img_url and any(ext in img_url for ext in ['.jpg', '.jpeg', '.png', '.svg']):
                # Télécharger chaque image
                try:
                    response = requests.get(img_url)
                    if response.status_code == 200:
                        file_extension = img_url.split('.')[-1]
                        file_name = f"{product_title_text}_{index}.{file_extension}"
                        file_path = os.path.join(folder_path, file_name)  # Ajouter le nom du fichier au chemin du dossier
                        with open(file_path, 'wb') as file:
                            file.write(response.content)
                except Exception as e:
                    print(f"Erreur lors du téléchargement de l'image : {e}")


        #PDF
        div_with_id = soup.find('div', id='table_module_downloads_1')
        # Récupérer tous les éléments <a>
        links = div_with_id.find_all('a')
        # Vérifier l'existence du dossier 'downloads', le créer si nécessaire
        download_folder = 'downloads'
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        # Télécharger pdfs
        for link in links:
            file_url = 'https://home.liebherr.com'+ link.get('href') 
            file_title = link.get('title') or 'default_filename'
            file_extension = os.path.splitext(file_url)[1]
            file_name = product_title_text+ " fichier " + file_title + file_extension
            file_path = os.path.join(download_folder, file_name)

            try:
                response = requests.get(file_url, stream=True)
                if response.status_code == 200:
                    with open(file_path, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
            except Exception as e:
                print(f"Erreur lors du téléchargement du fichier : {e}")


        await browser.close()


    except Exception as e:
        print(f"Erreur rencontrée : {e}")
        print("Relancement de la fonction.")
        await produit()