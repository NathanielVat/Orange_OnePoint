import os
import requests
from bs4 import BeautifulSoup

# Fonction pour extraire la date du dernier communiqué de presse depuis le site
def DateLastComm(entreprise):
    if entreprise == "Bouygues":  
        url = "https://www.corporate.bouyguestelecom.fr/presse-et-actualites/"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        dateSpan = soup.find('span', class_='card-com__header__date')  # Remplace avec la classe réelle     
        dateBouygues = dateSpan.text.replace('Communiqué du ', '').strip()
        lien = soup.find('a', class_='card-com__text')     
        lienFinal = lien.get('href')
        return dateBouygues, lienFinal
    
    if entreprise == "BouyguesEntreprises":  
        url = "https://www.bouyguestelecom-entreprises.fr/a-propos/communique-presse"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        em_element = soup.find('em')
        dateBouyguesEntreprises = em_element.text.strip()
        Txtlien = soup.find('div', class_='text presentation__col').find('p')
        lien = Txtlien.find('a')
        lienFinal = "https://www.bouyguestelecom-entreprises.fr/" + lien.get('href')
        return dateBouyguesEntreprises, lienFinal
    
    if entreprise == "SFR":                 
        url = "https://alticefrance.com/communique-presse-all"  
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        dateSpan = soup.find('h4', class_='pressrelease__type')  # Remplace avec la classe réelle
        dateSFR = dateSpan.text.replace('Actus en région - ', '').strip()
        lien = soup.find('a', class_='pressrelease-download')
        lienFinal = lien.get('href')
        return dateSFR, lienFinal
    
    if entreprise == "Free":                 
        url = "https://www.freepro.com/communiques-presse/"  
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        dateFree = soup.find('p', class_='card-presse__date').text  # Remplace avec la classe réelle
        lien = soup.find('a', class_='btn-link stretched-link')
        lienFinal = lien.get('href')
        return dateFree, lienFinal
    
    if entreprise == "Iliad":                 
        url = "https://www.iliad.fr/fr/media/communiques-de-presse/all/all"  
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        dateFree = soup.find('span', class_='jss50 ') 
        lien = soup.find('a', class_='jss16')
        print(dateFree, lien)
        #return dateFree, lien


def LireFichierTxt(entreprise):
    nom_fichier = os.path.join(os.path.dirname(__file__), f"{entreprise}.txt")
    # Vérifie si le fichier existe
    if not os.path.exists(nom_fichier):
        # Si le fichier n'existe pas, crée-le avec une date par défaut
        return entreprise, " "
    else:
        with open(nom_fichier, 'r') as fichier:
            dateFichier = fichier.read().strip()
            return dateFichier


def WriteFichierTxt(dateNumSite, entreprise):
    nom_fichier = os.path.join(os.path.dirname(__file__), f"{entreprise}.txt")
    try:
        with open(nom_fichier, 'w') as fichier:
            fichier.write(dateNumSite)
    except Exception as e:
        print(f"Erreur lors de l'écriture dans le fichier : {e}")


def main(entreprise):
    dateSite, lien = DateLastComm(entreprise)
    dateFichier = LireFichierTxt(entreprise)

    if dateFichier == dateSite:
        print("\n", entreprise, ": \n\nAucun nouveau communiqué de presse.")
        print("Dernier communiqué de presse -->", dateFichier)
        print("------------------------------------------------")
    else:
        print("\n", entreprise, ": \n\nNouveau communiqué de presse !\n")
        dateFichier = LireFichierTxt(entreprise)
        print("Precedent communiqué de presse -->", dateFichier)
        WriteFichierTxt(dateSite, entreprise)
        dateFichier = LireFichierTxt(entreprise)
        print("Nouveau communiqué de presse -->", dateFichier)
        
        


print(" _    _____  ________  ______  ____")
print("| |  / /   |/_  __/ / / / __ \/  _/")
print("| | / / /| | / / / / / / /_/ // /")
print("| |/ / ___ |/ / / /_/ / _, _// /")
print("|___/_/  |_/_/  \____/_/ |_/___/")
print("    _____   ______  __  _________________  __________")
print("   /  _/ | / / __ \/ / / / ___/_  __/ __ \/  _/ ____/")
print("   / //  |/ / / / / / / /\__ \ / / / /_/ // // __/")
print(" _/ // /|  / /_/ / /_/ /___/ // / / _, _// // /___")
print("/___/_/ |_/_____/\____//____//_/ /_/ |_/___/_____/")
print("")

'''
main("Bouygues")
main("BouyguesEntreprises")
main("SFR")
main("Free")
'''
DateLastComm("Iliad")

input("Appuyez sur enter pour quitter le programme ")
