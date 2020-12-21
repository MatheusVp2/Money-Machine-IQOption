#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser

class INTER_CFG():
	
	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config.read("config.ini")

	def getAllTag(self, tag):
		return dict (self.config.items(f'{ tag }') )

	def updateConfig(self, tagIndice, dictSave ):
		for i in dictSave:
			self.config.set(f"{ tagIndice.upper() }",f"{ i }", f"{ dictSave[i] }")

	def saveConfig(self):
		with open('config.ini', 'w') as configfile:
			self.config.write(configfile)
