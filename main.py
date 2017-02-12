# -*- coding: utf-8 -*-
import os
import time
from bin.manga import *
from bin.Notification import Notification

HELP = "Bienvenue dans manga notifier !\nTapez help pour plus d'aide.\n(La séparation se fait avec des virgule ex: add,manga name,url)\n"

def start():
	"""start function"""
	test_manga()
	time.sleep(60*5)
	os.system("cls")

def console():
	commands = ['help', 'add', 'start']
	temp = input(">>>")
	command = temp.split(",")
	if command[0] in commands:
		if command[0] == commands[0]: #help
			print(HELP)
			return console()
		elif command[0] == commands[1]: #add
			if len(command) == 3 and (command[2].startswith("http://") or command[2].startswith("https://")):
				ajout_parametres(command[1], command[2])
				return console()
		elif command[0] == commands[2]: #start
			os.system("cls")
			while True:
				start()
	else:
		print(HELP)

if not os.path.exists('save.manga'):
	open('save.manga', 'wb')

if __name__ == "__main__":
	console()

#.withdraw()
#Hides the window. Restore it with .deiconify() or .iconify().



"""
ajout_parametres("Black Clover", "http://www.japscan.com/mangas/black-clover/")
ajout_parametres("Twin Star Exorcists", "http://www.crunchyroll.com/twin-star-exorcists")
ajout_parametres("Doupo Cangqiong", "http://mangafox.me/manga/doupo_cangqiong/")
ajout_parametres("Douluo Dalu", "http://mangafox.me/manga/doulou_dalu/")
ajout_parametres("Sehn Yin Wang Zuo", "http://mangafox.me/manga/shen_yin_wang_zuo/")
ajout_parametres("Tower Of God", "http://mangafox.me/manga/tower_of_god")
ajout_parametres("Wizardly Tower", "http://mangafox.me/manga/wizardly_tower/")
ajout_parametres("Black Healer", "http://mangafox.me/manga/isekai_de_kuro_no_iyashi_te_tte_yobarete_imasu")
ajout_parametres("Wu Dong Qian Kun", "http://mangafox.me/manga/wu_dong_qian_kun/")
ajout_parametres("Gosu", "http://mangafox.me/manga/gosu/")
"""