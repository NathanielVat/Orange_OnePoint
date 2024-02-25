import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import sys

os.environ['PYTHONWARNINGS'] = 'ignore:Unverified HTTPS request' #teste

os.chdir(os.path.dirname(sys.argv[0]))

options = webdriver.ChromeOptions()
#options.add_argument("--headless")
options.add_argument('--log-level=3')

# Utiliser une seule instance de webdriver pour toutes les opérations
driver = webdriver.Chrome(options=options)

# Fonction pour extraire la date du dernier communiqué de presse depuis le site
def DateLastComm(entreprise):
    if entreprise == "Bouygues":
        url = "https://www.corporate.bouyguestelecom.fr/presse-et-actualites/"
    elif entreprise == "BouyguesEntreprises":
        url = "https://www.bouyguestelecom-entreprises.fr/a-propos/communique-presse"
    elif entreprise == "SFR":
        url = "https://alticefrance.com/communique-presse-all"
    elif entreprise == "Free":
        url = "https://www.freepro.com/communiques-presse/"
    elif entreprise == "Iliad":
        url = "https://www.iliad.fr/fr/media/communiques-de-presse/all/all"
    else:
        print("Entreprise non reconnue.")
        return None

    driver.get(url)
    driver.implicitly_wait(5)

    if entreprise == "Bouygues":
        dateSpan = driver.find_element(By.CLASS_NAME, 'card-com__header__date')
        dateBouygues = dateSpan.text.replace('COMMUNIQUÉ DU ', '').strip()
        lien = driver.find_element(By.CLASS_NAME, 'card-com__text')
        lienFinal = lien.get_attribute('href')
    elif entreprise == "BouyguesEntreprises":
        cookie_field = driver.find_element(By.ID, "popin_tc_privacy_button_2")
        cookie_field.click()
        dateBouyguesEntreprises = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/section[1]/div/div/p[2]/span/em").text
        lien = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/section[1]/div/div/p[1]/a")
        lienFinal = lien.get_attribute('href')
    elif entreprise == "SFR":
        dateSpan = driver.find_element(By.CLASS_NAME, 'pressrelease__type')
        dateSFR = dateSpan.text.replace('Actus en région - ', '').strip()
        lien = driver.find_element(By.CLASS_NAME, 'pressrelease-download')
        lienFinal = lien.get_attribute('href')
    elif entreprise == "Free":
        cookie_field = driver.find_element(By.ID, "didomi-notice-disagree-button")
        cookie_field.click()
        driver.implicitly_wait(5)
        dateFree = driver.find_element(By.CLASS_NAME, 'card-presse__date').text
        lien = driver.find_element(By.XPATH, '/html/body/main/section[2]/div/div/div[1]/div/div[2]/h2/a')
        lienFinal = lien.get_attribute('href')
    elif entreprise == "Iliad":
        cookie_field = driver.find_element(By.CLASS_NAME, "didomi-continue-without-agreeing")
        cookie_field.click()
        driver.implicitly_wait(5)
        zoneCommPresse = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[2]").text
        lignes = zoneCommPresse.split('\n')
        premiere_ligne = lignes[1]
        dateIliad = premiere_ligne.split('\n')[-1]
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        target_url_prefix = "https://s3.fr-par.scw.cloud/iliad-strapi/"
        target_link = None
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith(target_url_prefix):
                lienFinal = href
                break
    else:
        print("Entreprise non reconnue.")
        return None

    return locals()

def LireFichierTxt(entreprise):
    nom_fichier = os.path.join(os.path.dirname(sys.argv[0]), f"{entreprise}.txt")

    if not os.path.exists(nom_fichier):
        return entreprise, ""
    else:
        with open(nom_fichier, 'r') as fichier:
            dateFichier = fichier.read().strip()
            return dateFichier

def WriteFichierTxt(dateNumSite, entreprise):
    nom_fichier = os.path.join(os.path.dirname(sys.argv[0]), f"{entreprise}.txt")

    try:
        with open(nom_fichier, 'w') as fichier:
            fichier.write(dateNumSite)
    except Exception as e:
        print(f"Erreur lors de l'écriture dans le fichier : {e}")

def main(entreprise):
    result = DateLastComm(entreprise)

    if result is not None:
        dateSite = result.get('dateBouygues', '') or result.get('dateBouyguesEntreprises', '') or result.get('dateSFR', '') or result.get('dateFree', '') or result.get('dateIliad', '')
        lien = result.get('lienFinal', '')

        dateFichier = LireFichierTxt(entreprise)

        if dateFichier == dateSite:
            print("\n", entreprise, ": \n\nAucun nouveau communiqué de presse.")
            print("Dernier communiqué de presse -->", dateFichier)
            print("------------------------------------------------\n\n\n")
        else:
            print("\n", entreprise, ": \n\nNouveau communiqué de presse !\n")
            print("Precedent communiqué de presse -->", dateFichier)
            WriteFichierTxt(dateSite, entreprise)
            dateFichier = LireFichierTxt(entreprise)
            print("Nouveau communiqué de presse -->", dateFichier)
            print("------------------------------------------------>>>>>>>>>> ", lien, "\n\n\n")

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

main("Bouygues")
main("BouyguesEntreprises")
main("SFR")
main("Free")
main("Iliad")

driver.quit()
input("Appuyez sur enter pour quitter")
