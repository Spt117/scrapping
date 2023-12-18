from Bibliothèque.produit import produit
import csv
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import os


# Chemin du fichier CSV
filename = 'produits.csv'
headers = ['Nom', 'Arborescence', 'Description', 'Données techniques']

# Vérifier si le fichier existe déjà
if not os.path.exists(filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

# Liste des urls
urls = ["https://home.liebherr.com/fr/fra/products/%C3%A9lectrom%C3%A9nager/pose-libre/cong%C3%A9lateurs-armoires/cong%C3%A9lateurs-armoires.html?event=&size=100","https://home.liebherr.com/fr/fra/products/%C3%A9lectrom%C3%A9nager/pose-libre/side-by-side/side-by-side.html","https://home.liebherr.com/fr/fra/products/%C3%A9lectrom%C3%A9nager/built-in-appliances/r%C3%A9frig%C3%A9rateurs-int%C3%A9grables-encastrables/r%C3%A9frig%C3%A9rateurs-int%C3%A9grables-encastrables.html?event=&size=100&__ncforminfo=GGFBb3afBo2ZO7igL-GiUNXjhipZ3tR8mQAWYl9i7icedcRpe38VyoVH_KSQueclPm9RzTVyfF0tmBclBsJu6eB5l-4PcPA28zVeN7qO9u0-VoKYrHe-nkk5tPDSPPaMOGyhUq7oncdsE2ztJQeteushlRnt_6qf","https://home.liebherr.com/fr/fra/products/%C3%A9lectrom%C3%A9nager/built-in-appliances/caves-%C3%A0-vin-encastrables/caves-%C3%A0-vin-encastrables/caves-%C3%A0-vin-encastrables.html?event=&size=100","https://home.liebherr.com/fr/fra/products/%C3%A9lectrom%C3%A9nager/built-in-appliances/caves-%C3%A0-vin-encastrables/caves-%C3%A0-vin-sous-plan/caves-%C3%A0-vin-sous-plan.html","https://home.liebherr.com/fr/fra/products/%C3%A9lectrom%C3%A9nager/built-in-appliances/cong%C3%A9lateurs-int%C3%A9grables/cong%C3%A9lateurs-int%C3%A9grables.html?event=&size=100&__ncforminfo=Vb0pi5QUgr5_0fvPobXBDseVZHIgnAfOWp4gSjVjhfBucjYn2SJdqbO-jeisO6eNFuncXZfhFQOSzo0iKIXTDdxhYD1_PcGd5KoIgIGzRNyzl2Kn8-b4JoRBIGAzzfDuMmRhoOs0HUqQSZArsXJAEjuAHpxMFjww-fMN91AZFsqTaXnvVu2T40Oi0H2Xp2S_2GePB0R3H8jyta5pEpzqRWoDHoVfYRvFY1cTPSwPdCk%3D","https://home.liebherr.com/fr/fra/products/%C3%A9lectrom%C3%A9nager/built-in-appliances/combin%C3%A9s-r%C3%A9frig%C3%A9rateur-cong%C3%A9lateur-int%C3%A9grables/combin%C3%A9s-r%C3%A9frig%C3%A9rateur-cong%C3%A9lateur-int%C3%A9grables.html?event=&size=100","https://home.liebherr.com/fr/fra/products/appareils-professionnels/h%C3%B4tellerie-et-restauration/r%C3%A9frig%C3%A9rateurs/r%C3%A9frig%C3%A9rateurs.html?event=&size=100&__ncforminfo=n30yHP3MaYPl5SxwtK4vhrw1Nc45edYV4xYEVEtZHEaxNGicy-AHgpEV52hB69bFWk-FKJHGp8bQcOimLViYb5rpwVNg8i9umTaYu9EWooxg0m4CqSMtLM66Q-8519yJybvlaISka9bgnGfR2f7ebiUfgEzLyN0bJJVpzyIAF7vGhTHf8-9CBGXywvFGRPGDNsTPjgc0alw%3D","https://home.liebherr.com/fr/fra/products/appareils-professionnels/h%C3%B4tellerie-et-restauration/cong%C3%A9lateurs/cong%C3%A9lateurs.html?event=&size=100","https://home.liebherr.com/fr/fra/products/appareils-professionnels/industrie-de-la-boisson/r%C3%A9frig%C3%A9rateurs/r%C3%A9frig%C3%A9rateurs.html?event=&size=100&__ncforminfo=YKTOYosc-q5rL8P6flS7Svg6eYpPF0MtO3CRrzdhzo5bVtTVoDEnzLsJuUkrMb5ztbZ5pMO_XNVgPi9_L-n8x3EhFyKeorpcg85K6zYBG6QsNvdMDt9SyVj61L36LuH8cPuFMsUJrUKwHThWIo9BSUWXJj-Cf_h7IHg_CUX0kmCXLDq965FE6c0HgLBsXjy_uNHXHJoIpYliC-H8yO0jUoK3job3qBd2TfGPzHRoHoAMIStzw5NTAMYiGXAD56AG5dgmLn70wD1rxqM7-5Oxc81cmEjAA_4oI6lZvLiUZaxePG_wro8AQB9tjSAA6zQ7fP8J2wk-R8P3tUq8ehnX6PlWBe2jkpzDvqGYvi5X5lBcWDlE1sdXlxDdspRDiSRmrWyyoOJ0ccFLcywbZRRjPjDp4PdPfJh6kz2ROWH62FcafRGweAphrbuAj32Dn7EZx27RLKZhd8s%3D","https://home.liebherr.com/fr/fra/products/appareils-professionnels/h%C3%B4tellerie-et-restauration/tables-r%C3%A9frig%C3%A9r%C3%A9es/tables-r%C3%A9frig%C3%A9r%C3%A9es.html?event=&size=100&__ncforminfo=TXqctJ97PI-QXlDLcWJVnSYRnJufDgeHlRuHHvQ6pNRNd2hkpj12OES7ZtvWOc83x685pbQqjW9oJaUBrhQwcGhRx0Y9ic7HXUHStDdPYtFnTXiZGEZYP5Tb0xU56i9Xh4k7Km-FZmNKO3eeXUXe1x2sJ8a5W-_QWO3Y0VieZC3jOipkcsU8Wg%3D%3D","https://home.liebherr.com/fr/fra/products/appareils-professionnels/h%C3%B4tellerie-et-restauration/armoires-%C3%A0-vin/armoires-%C3%A0-vins-encastrables/armoires-%C3%A0-vins-encastrables.html","https://home.liebherr.com/fr/fra/products/appareils-professionnels/boulangerie/r%C3%A9frig%C3%A9rateurs/r%C3%A9frig%C3%A9rateurs.html","https://home.liebherr.com/fr/fra/products/appareils-professionnels/boulangerie/cong%C3%A9lateurs/cong%C3%A9lateurs.html","https://home.liebherr.com/fr/fra/products/appareils-professionnels/recherche-et-laboratoire/r%C3%A9frig%C3%A9rateurs-de-laboratoire/r%C3%A9frig%C3%A9rateurs-de-laboratoire.html?event=&size=100","https://home.liebherr.com/fr/fra/products/appareils-professionnels/recherche-et-laboratoire/cong%C3%A9lateurs-de-laboratoire/cong%C3%A9lateurs-de-laboratoire.html?event=&size=100&__ncforminfo=5Qc7YrGt77ye7m6ZQPSDLsthsl_9wGP1iihInC7n-MQ0A5PBPYEx4VMjBwYcQjijzQPBDBVXAUB5ycGq6P3dzgI3RQ5ThWOO8QU2EucuxZPR56R0ppD-wEjN3AVoJ5krRhdGygyoKUPED8CXCgOFqPvOTxiDvyLqieRCceYYuzD7ccVpM41g6tpqxFVx8qqa-ejg6I_CyGYZVpX8JK-z75nega5npwV5tuj1gIrz2BsR33Vssl5t7BvtWSXH6owe6dejbdup7b_3r8rch1BSF6u1sySNBmL8hHO362Mhb1ZdgPY1pUb1UknhZX5K-3BC","https://home.liebherr.com/fr/fra/products/appareils-professionnels/recherche-et-laboratoire/produits-pharmaceutiques/produits-pharmaceutiques.html?event=&size=100&__ncforminfo=YEDgGoX1kQJC1QplhU4s1KMYXQM63iWoInZtgqUmoIN9B0QAhbj-JqBkWdkrQibCgDYeQICZZ_TiEda1fg41zMCxgicIWeOpzyWTBuMThpaHugV7HkhyNKQtxq_se8gn_t3FkA3xT1SHHOQ1uoUHpCrcclbZJZmTtIEiHUlcmhvHsERYfc6esLnC8nnRCfkXAF2-lwT3RmhF4obLZVffHkepcrKiRo-U1G9dRE6x9vvfQBI_V8_NzJoXWqY7F2dR9ImFN7aFVxE%3D","https://home.liebherr.com/fr/fra/products/appareils-professionnels/recherche-et-laboratoire/cong%C3%A9lateurs-%C3%A0-temp%C3%A9rature-ultra-basse/cong%C3%A9lateurs-%C3%A0-temp%C3%A9rature-ultra-basse.html","https://home.liebherr.com/fr/fra/products/appareils-professionnels/industrie-de-la-boisson/r%C3%A9frig%C3%A9rateurs/r%C3%A9frig%C3%A9rateurs.html?event=&size=100","https://home.liebherr.com/fr/fra/products/appareils-professionnels/h%C3%B4tellerie-et-restauration/armoires-%C3%A0-vin/armoires-%C3%A0-vins-encastrables/armoires-%C3%A0-vins-encastrables.html","https://home.liebherr.com/fr/fra/products/appareils-professionnels/industrie-des-produits-surgel%C3%A9s-et-cr%C3%A8mes-glac%C3%A9es/coffres-de-pr%C3%A9sentation-impuls/coffres-de-pr%C3%A9sentation-impuls.html?event=&size=100","https://home.liebherr.com/fr/fra/products/appareils-professionnels/industrie-des-produits-surgel%C3%A9s-et-cr%C3%A8mes-glac%C3%A9es/coffres-de-pr%C3%A9sentation/coffres-de-pr%C3%A9sentation.html?event=&size=100","https://home.liebherr.com/fr/fra/products/appareils-professionnels/industrie-des-produits-surgel%C3%A9s-et-cr%C3%A8mes-glac%C3%A9es/coffres-de-stockage/coffres-de-stockage.html?event=&size=100","https://home.liebherr.com/fr/fra/products/appareils-professionnels/industrie-des-produits-surgel%C3%A9s-et-cr%C3%A8mes-glac%C3%A9es/cong%C3%A9lateurs/cong%C3%A9lateurs.html"]
# ["https://home.liebherr.com/fr/fra/products/%C3%A9lectrom%C3%A9nager/pose-libre/combin%C3%A9s-r%C3%A9frig%C3%A9rateur-cong%C3%A9lateur/combin%C3%A9s-r%C3%A9frig%C3%A9rateur-cong%C3%A9lateur.html?event=&size=100","https://home.liebherr.com/fr/fra/products/%C3%A9lectrom%C3%A9nager/pose-libre/r%C3%A9frig%C3%A9rateurs-pose-libre-et-table-top/r%C3%A9frig%C3%A9rateurs-pose-libre-et-table-top.html?event=&size=100&__ncforminfo=nNVzH6xLsgsPcuLleeaGwrWyUXJogpBgggOzmaWAoMYmEtWYZIS9Qf3ztVZ0d4Z-QUe8AqmsGzMvenGENb9Q9KJC4h4wDxHQn53ep290AIWyfdguTqvtLJj3oMkRGad2RC4rlAR3tkKh4KixCmswyGQMeP5oj6cOMNUsh_ivaVbry5_FU8H8eEuUUwC3EKio18iCZQIcKwoUPdS8YfKyaG-f7Mc2WqGbKZVmyyUGPrNXgpZ5YAdvYcBatq0rVvT4BmRa6tgkTTCas_m8aNLQDgcUn3_4I3QdzMmBHrwserKY9GarP2s651c2GVEOFQjXHjz5T-GWzuKZJK-Tfrw07_IN8uIU2vDQCyl29fxoHrIQ26VLcNQfK4fjm3IIeb52Hxsh-xaiM1nNaoHoaHpueOrUCdb8nMF6fFa8fn8TIQYjUGlw03ay3QzxsJzE6QhGTKPMZMgas-KIQnxob9VLq9zRMjSw6Y7w8u6WxV28sbxk76FbRrN9wA%3D%3D","https://home.liebherr.com/fr/fra/products/%C3%A9lectrom%C3%A9nager/pose-libre/cong%C3%A9lateurs-armoires/cong%C3%A9lateurs-armoires.html?event=&size=100","https://home.liebherr.com/fr/fra/products/%C3%A9lectrom%C3%A9nager/pose-libre/side-by-side/side-by-side.html","https://home.liebherr.com/fr/fra/products/%C3%A9lectrom%C3%A9nager/pose-libre/appareils-compacts/humidor/humidor/humidor.html","https://home.liebherr.com/fr/fra/products/%C3%A9lectrom%C3%A9nager/pose-libre/appareils-compacts/cave-de-vieillissement-grandcru/cave-de-vieillissement-grandcru/cave-de-vieillissement-grandcru.html","https://home.liebherr.com/fr/fra/products/%C3%A9lectrom%C3%A9nager/built-in-appliances/caves-%C3%A0-vin-encastrables/caves-%C3%A0-vin-sous-plan/caves-%C3%A0-vin-sous-plan.html","https://home.liebherr.com/fr/fra/products/%C3%A9lectrom%C3%A9nager/built-in-appliances/caves-%C3%A0-vin-encastrables/caves-%C3%A0-vin-encastrables/caves-%C3%A0-vin-encastrables.html?event=&size=100","https://home.liebherr.com/fr/fra/products/%C3%A9lectrom%C3%A9nager/pose-libre/caves-%C3%A0-vin/armoires-de-mise-en-temp%C3%A9rature/vinidor/vinidor.html","https://home.liebherr.com/fr/fra/products/%C3%A9lectrom%C3%A9nager/pose-libre/caves-%C3%A0-vin/caves-de-vieillissement/grandcru/grandcru.html?event=&size=100"]

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


