# Tous les imports
import argparse as arg
import json
import re
import requests
from bs4 import BeautifulSoup
import sys
import getopt
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as E
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time

# ------------------------------------------------------------------------------------------------
# Cette fonction permet de retourner sous format json les valeurs de sortie
# On prend en paramètres tous les éléments que nous récupérons du scrapping youtube
def remplirOutput(titre, view, id, auteur, desc, lien, pouce, com):
    video = {
        id: {
            "titre": titre,
            "vue": view,
            "auteur": auteur,
            "description": desc,
            "lien description": lien,
            "Nombre de like": pouce,
            "commentaires" : com
        }
    }
    return video


# ------------------------------------------------------------------------------------------------
# Cette fonction retourne le fichier de sprtie nommée output.json
# On prend en paramètres tous les éléments que nous récupérons du scrapping youtube
def outputFichier(titre, view, id, auteur, desc, lien, pouce, com):
    output = argumentOuput(sys.argv[1:])
    filename = output
    # Lire ce qui se trouve dane le fichier output
    with open(filename, "r") as file:
        lst = json.load(file)

    # réecrire ce qui se trouve dans le fichier
    # En effet cela nous permet de ne pas supprimer les éléments rentrés précedemment
    with open(filename, "w") as f:
        json.dump(lst, f)

    # #ajouter les nouvelles lignes
    fichier_remplir = remplirOutput(titre, view, id, auteur, desc, lien, pouce, com)
    with open(filename, mode="w") as f:
        lst.append(fichier_remplir)
        json.dump(lst, f, ensure_ascii=False)


# ------------------------------------------------------------------------------------------------
# Cette fonction retroune le nombre de like sous la vidéo
def likeVideo(fichier_json):
    try:
        res = fichier_json["contents"]["twoColumnWatchNextResults"]["results"][
            "results"
        ]["contents"][0]["videoPrimaryInfoRenderer"]["videoActions"]["menuRenderer"][
            "topLevelButtons"
        ][
            0
        ][
            "segmentedLikeDislikeButtonRenderer"
        ][
            "likeButton"
        ][
            "toggleButtonRenderer"
        ][
            "defaultText"
        ][
            "accessibility"
        ][
            "accessibilityData"
        ][
            "label"
        ]
    except:
        res = "null"
    return res


# ------------------------------------------------------------------------------------------------
# Cette fonction retroune le titre de la vidéo
def titreVideo(soup):
    return soup.find("meta", itemprop="name")["content"]


# ------------------------------------------------------------------------------------------------
# Cette fonction retroune le nombre de vue de la vidéo
def viewVideo(soup):
    return soup.find("meta", itemprop="interactionCount")["content"]


# ------------------------------------------------------------------------------------------------
# Cette fonction retourne la description de la vidéo
def decriptionVideo(fichier_json):
    try:
        tab = fichier_json["contents"]["twoColumnWatchNextResults"]["results"][
            "results"
        ]["contents"][1]["videoSecondaryInfoRenderer"]["description"]["runs"]
        res_description = ""
        for i in range(len(tab)):
            res_description = res_description + tab[i]["text"]
    except:
        res_description = ""
    return res_description


# ------------------------------------------------------------------------------------------------
# Cette fonction retroune les liens de la description de la vidéo
def lienDescriptionVideo(fichier_json):
    try:
        tab_lien = fichier_json["contents"]["twoColumnWatchNextResults"]["results"][
            "results"
        ]["contents"][1]["videoSecondaryInfoRenderer"]["description"]["runs"]
        res_description_lien = ""
        for i in range(len(tab_lien)):
            if ("https://" in tab_lien[i]["text"]) or (
                "http://" in tab_lien[i]["text"]
            ):
                res_description_lien = res_description_lien + tab_lien[i]["text"] + "\n"
    except:
        res_description_lien = ""
    return res_description_lien


# ------------------------------------------------------------------------------------------------
# Cette fonction retroune l'id de la vidéo
def idVideo(soup):
    return soup.find("meta", itemprop="videoId")["content"]


# ------------------------------------------------------------------------------------------------
# Cette fonction retroune l'auteur de la vidéo
def authorVideo(soup):
    return soup.find("span", itemprop="author").next.next["content"]


# ------------------------------------------------------------------------------------------------
# Cette fonction est une autre fonction principale qui permet de scrapper les informations
# En paramètre ce trove l'id de la vidéo
def rechercherJson(id):
    r = requests.get("https://www.youtube.com/watch?v=" + id)
    soup = BeautifulSoup(r.text, "html.parser")

    data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)
    data_json = json.loads(data)

    with open("codesource.json", mode="w") as f:
        json.dump(data_json, f)

    fichier = open("codesource.json", "r")
    fichier_json = json.load(fichier)

    titre = titreVideo(soup)
    view = viewVideo(soup)
    id = idVideo(soup)
    auteur = authorVideo(soup)
    desc = decriptionVideo(fichier_json)
    lien = lienDescriptionVideo(fichier_json)
    pouce = likeVideo(fichier_json)
    com = commentaires("https://www.youtube.com/watch?v=" + id)

    outputFichier(titre, view, id, auteur, desc, lien, pouce, com)

# ------------------------------------------------------------------------------------------------
# Cette fonction récupère le paramètre d'input en argument d'entrée 
def argumentInput(argv):
    inputFile = ''
    try:
        options, args = getopt.getopt(argv,"hi:o:",["input=","output="])
    except getopt.GetoptError:
        print ('scrapper.py --input <inputfile> --output <outputfile>')
        sys.exit(2)
    for opt, arg in options:
        if opt == '-h':
            print ('scrapper.py --input <inputfile> --output <outputfile>')
            sys.exit()
        elif opt in ("-i", "--input"):
            input = arg
    return input

# ------------------------------------------------------------------------------------------------
# Cette fonction récupère le paramètre d'output en argument d'entrée 
def argumentOuput(argv):
    outputFile = ''
    try:
        options, args = getopt.getopt(argv,"hi:o:",["input=","output="])
    except getopt.GetoptError:
        print ('scrapper.py --input <inputfile> --output <outputfile>')
        sys.exit(2)
    for opt, arg in options:
        if opt == '-h':
            print ('scrapper.py --input <inputfile> --output <outputfile>')
            sys.exit()
        elif opt in ("-o", "--output"):
            output = arg
    return output

# ------------------------------------------------------------------------------------------------
# Cette fonction retourne les 5 premiers commentaires 
# Prend en entrée le'URL
def commentaires(url):
    try: 
        res = True
        s=Service(ChromeDriverManager().install())
        options = Options()
        driver = webdriver.Chrome(service=s, chrome_options=options)
    
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        commentaires = []
        element = driver.find_element(By.XPATH, "//*[@id=\"comments\"]")
        driver.execute_script("arguments[0].scrollIntoView();", element)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        commentsList = soup.find_all("ytd-comment-thread-renderer", {"class": "style-scope ytd-item-section-renderer"}, limit = 5) 
        if res:
            while commentsList == []:
                time.sleep(1)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                print(soup)
                commentsList = soup.find_all("ytd-comment-thread-renderer", {"class": "style-scope ytd-item-section-renderer"}, limit = 5)
                print(commentsList)
            for comment in commentsList:
                print(comment.find("yt-formatted-string", {"id": "content-text"}).text)
                commentaires.append(comment.find("yt-formatted-string", {"id": "content-text"}).text)
        driver.close()
    except:
        commentaires = ""
        driver.close()
    return commentaires

# ------------------------------------------------------------------------------------------------
# Cette fonction est la fonction principale
def main():
    input = argumentInput(sys.argv[1:])
    output = argumentOuput(sys.argv[1:])
    # Initialisation du fichier output.json
    employee = []
    with open(output, "w") as f:
        json.dump(employee, f)

    # Elle lit tous les id qui se trouve dans le fichier input.json
    with open(input) as mon_fichier:
        data = json.load(mon_fichier)
    for i in data["videos_id"]:
        # Et recherche pour un id les informations scrapper
        rechercherJson(i)
    mon_fichier.close

if __name__ == "__main__":  
    main()



