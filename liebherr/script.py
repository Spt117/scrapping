from go import go
import csv


urls =['https://www.liebherr.be/fr/refrigeration/modeles','https://www.liebherr.be/fr/congelation/modeles','https://www.liebherr.be/fr/vin/modeles','https://www.liebherr-professional.be/fr/appareils-professionels/merchandising/refrigerateurs-encastrables-sous-plan/','https://www.liebherr-professional.be/fr/appareils-professionnels/merchandising/refrigerateurs-bouteilles/','https://www.liebherr-professional.be/fr/appareils-professionnels/merchandising/refrigerateurs-display/','https://www.liebherr-professional.be/fr/appareils-professionnels/merchandising/refrigerateurs-coffres/','https://www.liebherr-professional.be/fr/appareils-professionnels/merchandising/congelateurs-encastrables-sous-plan/','https://www.liebherr-professional.be/fr/appareils-professionnels/merchandising/congelateurs-display/','https://www.liebherr-professional.be/fr/appareils-professionnels/merchandising/congelateurs-coffres/','https://www.liebherr-professional.be/fr/appareils-professionnels/gastronomie/refrigerateurs-encastrables-sous-plan-gastronomie/','https://www.liebherr-professional.be/fr/appareils-professionnels/gastronomie/congelateurs-encastrables-sous-plan-gastronomie/','https://www.liebherr-professional.be/fr/appareils-professionnels/gastronomie/refrigerateurs-pour-la-gastronomie/','https://www.liebherr-professional.be/fr/appareils-professionnels/gastronomie/congelateurs-pour-la-gastronomie/','https://www.liebherr-professional.be/fr/appareils-professionnels/gastronomie/combines-pour-la-gastronomie/','https://www.liebherr-professional.be/fr/appareils-professionnels/laboratoire/refrigerateurs-de-laboratoire/','https://www.liebherr-professional.be/fr/appareils-professionnels/laboratoire/refrigerateurs-laboratoire-antideflagrants/','https://www.liebherr-professional.be/fr/appareils-professionnels/laboratoire/refrigerateurs-pour-produits-pharmaceutiques/','https://www.liebherr-professional.be/fr/appareils-professionnels/laboratoire/combines-de-laboratoire/','https://www.liebherr-professional.be/fr/appareils-professionnels/laboratoire/congelateurs-de-laboratoire/','https://www.liebherr-professional.be/fr/appareils-professionnels/creme-glacee/conservateurs-de-creme-glacee/','https://www.liebherr-professional.be/fr/appareils-professionnels/boulangerie/refrigerateurs-boulangerie/','https://www.liebherr-professional.be/fr/appareils-professionnels/boulangerie/congelateurs-boulangerie/']

 # création du csv
filename = 'produits.csv'

# En-têtes des colonnes
headers = ['Nom','Arborescence', 'Couleurs disponibles','Prix', 'Description',  'Volume', 'Dimensions']

# Créer le fichier CSV avec les en-têtes
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

for url in urls:
    go(url)