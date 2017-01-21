import os
import time
import pickle
import requests
from Notification import Notification

def charger_parametres():
	"""Extrait les paramètres d'un fichier texte dedié"""
	parametres = dict()
	with open("save.manga", "rb") as fichier:
		pickler = pickle.Unpickler(fichier)
		try:
			save = pickler.load()
		except EOFError:
			return dict()
		parametres.append(save)
		return parametres

def maj_parametres(manga, url):
	"""Re-écrit les paramètres d'un fichier texte dedié"""
	parametres = charger_parametres()
	with open("save.manga", "rb") as fichier:
		mon_pickler = pickle.Pickler(fichier)
		if manga in parametres:
			print("Manga déja existant.")
			return
		parametre = dict()
		parametres = charger_parametres()
		parametre[manga] = manga
		parametre[manga + "_URL"] = url
		parametre[manga + "_CHAP"] = test_manga(manga, url, 0)
		parametres[manga] = parametre
		mon_pickler.dump(parametres)

def test_manga(manga, url, chapitre):
	chapitre_actu = ""
	if url.startswith("mangafox", 7):
		try:
			req = requests.get(url)
		except Exception as e:
			print("Error : " + e)
			return

		if req.status_code != 200:
			print("Error : " + req.status_code)
			return

		lignes = req.text.split("Chapter ")
		test = True
		chap = []
		a = 0
		while test:
			chap.append(lignes[1][(a + 4)])
			if chap[a].isnumeric() is False:
				del chap[a]
				test = False
			a += 1

		for i in chap:
			chapitre_actu += i

		if chapitre < int(chapitre_actu):
			chapitre_actu += " (new)"
			Notification("New Chapter !", manga + " has release the " + chapitre_actu + " tome !")

	return chapitre_actu


if not os.path.exists('save.manga'):
	open('save.manga', 'wb')
	print("mang")

parametres = charger_parametres()

for parametre in parametres:
	print(parametre[manga] + " : " + test_manga(parametre[manga], parametre[manga + "_URL"], parametre[manga + "_CHAP"]))


maj_parametres("Wu Dong Qian Kun", "http://mangafox.me/manga/wu_dong_qian_kun/")

#.withdraw()
#Hides the window. Restore it with .deiconify() or .iconify().