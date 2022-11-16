import argparse as arg
import json
import re
import requests
from bs4 import BeautifulSoup
from scrapper import titreVideo, idVideo, authorVideo, lienDescriptionVideo, decriptionVideo, commentaires

r = requests.get("https://www.youtube.com/watch?v=K0x-P5xmBHs")
soup = BeautifulSoup(r.text, "html.parser")

url = "https://www.youtube.com/watch?v=K0x-P5xmBHs"

data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)
data_json = json.loads(data)

with open("codesource.json", mode="w") as f:
    json.dump(data_json, f)

fichier = open("codesource.json", "r")
fichier_json = json.load(fichier)

def test_titrevideo():
    assert titreVideo(soup) == 'Imagine Dragons - Symphony (Official Visualizer)'

# Le nombre de vue augmente, tout comme le nombre de j'aime donc on ne peux pas les tester
#def test_viewVideo():
#    assert viewVideo(soup) == '2267763'

def test_idvideo():
    assert idVideo(soup) == 'K0x-P5xmBHs'

def test_authorVideo():
    assert authorVideo(soup) == 'ImagineDragonsVEVO'

def test_lienDescriptionVideo():
    assert lienDescriptionVideo(fichier_json) == 'https://ImagineDragons.lnk.to/Mercury\nhttps://ImagineDragons.lnk.to/NV10\nhttp://ImagineDragonsmusic.com/Tour\nhttp://ImagineDragons.lnk.to/Discord\nhttps://ImagineDragons.lnk.to/Facebook\nhttps://ImagineDragons.lnk.to/Twitter\nhttps://ImagineDragons.lnk.to/Instagram\nhttps://ImagineDragons.lnk.to/TikTok\nhttps://ImagineDragons.lnk.to/EmailList\nhttp://vevo.ly/GdefsB\n'

def test_decriptionVideo():
    assert decriptionVideo(fichier_json) == "Imagine Dragons - Symphony (Official Visualizer)\n\nListen to “Symphony” from the new album “Mercury - Acts 1 & 2” out now : https://ImagineDragons.lnk.to/Mercury\nListen to “Night Visions (Expanded Edition)” out now: https://ImagineDragons.lnk.to/NV10\nCatch Imagine Dragons on tour: http://ImagineDragonsmusic.com/Tour\nJoin the Imagine Dragons Discord: http://ImagineDragons.lnk.to/Discord   \n\nFollow Imagine Dragons:\n\nFacebook: https://ImagineDragons.lnk.to/Facebook\nTwitter: https://ImagineDragons.lnk.to/Twitter\nInstagram: https://ImagineDragons.lnk.to/Instagram\nTikTok: https://ImagineDragons.lnk.to/TikTok\nSign up for email updates: https://ImagineDragons.lnk.to/EmailList\n\nShot and Directed by Matt Eastin\n\n“Symphony” Lyrics:\n\nEver since I was young (coming up, coming up)\nAlways marching to a drum (bra da dum, bra da dum)\nAlways focused on me (one one, one one)\nNow I wish that I could hold someone (someone)\nSo tell my mom I love her, call my baby sister\nShould’ve hugged and kissed her\nCause life is just a mystery\nAnd it’s gone before you know it\nSo If you love me, won’t you show it\n\nCause this life is one big symphony\nThis night is one for you and me\nI’m the strings and you’re the timpani\nYou’re my constant tambourine\nThis life is one big symphony\nSo glad I’ve got you next to me\nI’m the chords and you’re the melody\nThis life’s one big symphony\n\nShe was the piano I’m the xylophone\nYou can have the trumpet, I’m the saxophone\nLife is skipping rope (keep going, keep going)\nFinding solace in a note (dote dote, dote dote)\nHad to struggle when I was broke (so low, so low)\nWriting music just to cope (no hope, no hope)\n\nYea, life is just perspective\nLaughing when you’ve wrecked it  \nSmiling when you kept it together \nYou weathered the storm \nAt the end of the play, you sang all the way \nDoesn’t matter how off key\nIf you did it, your way\n\nThis life is one big symphony\nThis night is one for you and me\nI’m the strings and you’re the timpani\nYou’re my constant tambourine\nThis life is one big symphony\nSo glad I’ve got you next to me\nI’m the chords and you’re the melody\nThis life’s one big symphony\n\nWould you care if I played you the flute?\nSee it’s my favorite one because it’s so delicate and beautiful\nI pull out the trombone if its more suitable\nWanna make you smile, it’s been a little while since I’ve seen the white of your teeth\nBeen a hard year\nLucky the guitar’s here\n\nLife is just one big symphony\n\nCause this life is one big symphony\nThis night is one for you and me\nI’m the stings and you’re the timpani\nYou’re my constant tambourine\nThis life is one big symphony\nSo glad I’ve got you next to me\nI’m the chords and you’re the melody\nThis life’s one big symphony\n\n#ImagineDragons #Symphony #Mercury \n\nMusic video by Imagine Dragons performing Symphony (Visualizer). © 2022 KIDinaKORNER/Interscope Records\n\nhttp://vevo.ly/GdefsB"

def test_commentaires():
    assert commentaires(url) == ["IM NEVER GONNA GET TIRED OF IMAGINE DRAGONS",
                "No importa la canción que sea, si es de Imagine Dragons el buen ritmo y la letra perfecta no faltarán.",
                "Imagine Dragons nunca decepciona!",
                "I haven't respected a band this much since Linkin Park. They make meaningful lyrics, manage to draw your attention, and don't let a genre stop them. I've been listening to and like this album a lot. Very awesome!",
                "They dont make songs,they make masterpices<3"]