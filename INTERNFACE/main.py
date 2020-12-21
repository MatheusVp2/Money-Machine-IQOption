import eel
from apiConfig import *
import json


eel.init('web')

@eel.expose
def getAllInfo(tag):
	cfg = INTER_CFG()
	return cfg.getAllTag(tag)


@eel.expose
def saveInfo(tag ,info):
	cfg = INTER_CFG()
	cfg.updateConfig(tag, info)
	cfg.saveConfig()


eel.start('main.html', size=(800, 800), port=80)