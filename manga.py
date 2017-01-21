import os
import time
import pickle
import requests
from Notification import Notification

manga = "Wu Dong Qian Kun"

if not os.path.exists('manga.txt'):
	open('manga.txt', 'wb')

def charger_parametres(file):
	"""Extrait les paramètres d'un fichier texte dedié"""
	parametres = []
	with open(file + ".txt", "rb") as fichier:
		pickler = pickle.Unpickler(fichier)
		parametres.append(pickler.load())
		return parametres

def maj_parametres(file, manga, url):
	"""Re-écrit les paramètres d'un fichier texte dedié"""
	with open(file + ".txt", "rb") as fichier:
		mon_pickler = pickle.Pickler(fichier)
		if parametres[manga] is not None:
			print("Manga déja existant.")
		parametres = charger_parametres(file)
		parametres[manga] = manga
		parametres[manga + "_URL"] = url
		parametres[manga + "_CHAP"] = test_manga(url, 0)
		mon_pickler.dump(tamp)

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


print(manga + " : " + test_manga(manga, "http://mangafox.me/manga/wu_dong_qian_kun/", 47))
print(manga + " : " + test_manga(manga, "http://mangafox.me/manga/doupo_cangqiong/", 47))
print(manga + " : " + test_manga(manga, "http://mangafox.me/manga/doulou_dalu/", 47))
print(manga + " : " + test_manga(manga, "http://mangafox.me/manga/wu_dong_qian_kun/", 47))
print(manga + " : " + test_manga(manga, "http://mangafox.me/manga/wu_dong_qian_kun/", 47))
print(manga + " : " + test_manga(manga, "http://mangafox.me/manga/wu_dong_qian_kun/", 47))

#.withdraw()
#Hides the window. Restore it with .deiconify() or .iconify().