# -- coding: utf-8 --

import os
import sys
import pickle

try:
	import requests
	from bin.Notification import Notification
except:
	# print("Composant are not installed yet. install it ? (y/n)")
	test = ""
	while test != 'o' and test != 'n' and test != 'O' and test != 'N':
		test = input("Composant are not installed yet. install it ? (y/n) : ")
	if test != ('o' or 'O'):
		sys.exit("Quit.")
	else:
		os.system("pip install requests")
		os.system("pip install pypiwin32")
		print("Done")
		import requests
		from bin.Notification import Notification


def charger_parametres():
	"""Extrait les paramètres d'un fichier texte dedié"""
	parametres = dict()
	with open("save.manga", "rb") as fichier:
		pickler = pickle.Unpickler(fichier)
		try:
			save = pickler.load()
		except EOFError:
			return dict()
		parametres.update(save)
		return parametres

def ajout_parametres(manga, url):

	parametres = charger_parametres()

	if manga in parametres:
		print(manga + " est déja enregistrer.")
		return

	maj_parametres(manga, url)

def maj_parametres(manga, url, chapitre=0):
	"""Re-écrit les paramètres d'un fichier texte dedié"""

	parametres = charger_parametres()

	parametre = dict()

	with open("save.manga", "wb") as fichier:
		mon_pickler = pickle.Pickler(fichier)
		parametre["name"] = manga
		parametre[manga + "_URL"] = url
		parametre[manga + "_CHAP"] = maj_chapitre(manga, url, chapitre)
		parametres[manga] = parametre
		mon_pickler.dump(parametres)

def maj_chapitre(manga, url, chapitre):
	"""Va tester chercher dans un page web le dernier scan a etre sortit et va checker si il a déja été lu par l'utilisateur."""
	try:
		req = requests.get(url)
	except Exception as e:
		print("Error : " + str(e))
		return

	if req.status_code != 200:
		print("Error : " + str(req.status_code))
		# sys.quit("Error : " + str(req.status_code))
		return

	chapitre_actu = ""

	#-------------------------------------------#

	if url.startswith("mangafox", 7):

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

	elif url.startswith("japscan", 11):
		lignes = req.text.split('/">')
		test = True
		chap = []
		a = 1
		while test:
			chap.append(lignes[5][len(lignes[5]) - a])
			if chap[a - 1].isnumeric() is False:
				del chap[a - 1]
				test = False
			a += 1

		for i in chap:
			chapitre_actu += i

		chapitre_actu = chapitre_actu[::-1]

	elif url.startswith("crunchyroll", 11):

		lignes = req.text.split("Épisode ")
		test = True
		chap = []
		a = 0
		while test:
			chap.append(lignes[1][a])
			if chap[a].isnumeric() is False:
				del chap[a]
				test = False
			a += 1

		for i in chap:
			chapitre_actu += i

	elif url.startswith("animedigitalnetwork", 7):
		pass

		lignes = req.text.split("")

	return chapitre_actu

def maj_manga(manga, url, chapitre):
	"""meme chose que maj_chapitre mais va afficher une notification si un nouveau chapitre est sortit"""
	if chapitre is None or chapitre == "":
		chapitre = 0

	if type(chapitre) != int():
		chapitre = int(chapitre)


	chapitre_actu = maj_chapitre(manga, url, chapitre)
		
	if chapitre < int(chapitre_actu):
		Notification("New Chapter !", manga + " has release the " + chapitre_actu + " tome !")
		maj_parametres(manga, url, chapitre=chapitre_actu)
		chapitre_actu += " (new)"

	return chapitre_actu

def test_manga():

	parametres = charger_parametres()

	for keys in parametres.keys():
		parametre = parametres[keys]
		manga = parametre["name"]
		print(parametre["name"] + " : " + maj_manga(parametre["name"], parametre[manga + "_URL"], parametre[manga + "_CHAP"]))
