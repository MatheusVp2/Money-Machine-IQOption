#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser

config = configparser.ConfigParser()
config.read("config.ini")

config.set("CONTA","EMAIL", "teste")

var = dict(config.items('CONTA'))

def updateConfig( tagIndice, dictSave ):
	global config
	for i in dictSave:
		config.set(f"{ tagIndice.upper() }",f"{ i }", f"{ dictSave[i] }")

var['email'] = "matheus@gmail.com"
var['senha'] = "matheus121212"
var['tipo']  = "real"

tagIndice = 'conta'

updateConfig( tagIndice, var )


# save to a file
with open('config.ini', 'w') as configfile:
    config.write(configfile)