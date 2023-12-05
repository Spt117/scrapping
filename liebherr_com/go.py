from Bibliothèque.produit import produit
import csv
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup


# création du csv
filename = 'produits.csv'

# En-têtes des colonnes
headers = ['Nom','Arborescence', 'Description', 'Données techniques']

with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

# Liste des urls
urls = ["https://home.liebherr.com/fr/fra/products/%C3%A9lectrom%C3%A9nager/pose-libre/combin%C3%A9s-r%C3%A9frig%C3%A9rateur-cong%C3%A9lateur/combin%C3%A9s-r%C3%A9frig%C3%A9rateur-cong%C3%A9lateur.html?event=fid108537&size=100",""]

async def getUrls(param):
    try:
        browser = await launch()
        page = await browser.newPage()
        await page.goto(param, waitUntil='networkidle0')
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')

        urlsProducts = []
        div_teaser_group = soup.find('div', class_='dpt-teaser-group')
        if div_teaser_group:
            for a_tag in div_teaser_group.find_all('a', class_='button primary trackEvent', href=True):
                urlsProducts.append("https://home.liebherr.com"+a_tag['href'])
        await browser.close()

        for urlProduct in urlsProducts:
            await produit(urlProduct)
            print("Done")

    except Exception as e:
        print(f"Erreur rencontrée : {e}")
        print("Relancement de la fonction getUrls.")
        await getUrls(param)




# asyncio.get_event_loop().run_until_complete(getUrls())

for url in urls:
    asyncio.get_event_loop().run_until_complete(getUrls(url))
    print("Done collection")


