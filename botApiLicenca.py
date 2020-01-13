#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################
'''
	Importações Gerais
'''

from time import strftime, time, sleep
from datetime import datetime, timezone, timedelta

from cryptography.fernet import Fernet
import ast 

#####################################
'''
	Funções de verificação de hora de data
'''
#####################################

def  getDataPassada(dtHoje, dtVencimento):
	'''
		VERIFICA SE A DATA JA PASSOU
	'''
	return  (datetime.strptime(dtVencimento, "%d/%m/%Y %H:%M:%S") - datetime.strptime(dtHoje, "%d/%m/%Y %H:%M:%S")).total_seconds()

def getDateTimeNow():
	'''
		DEFINE COMO PADRAO O HORARIO UTC-3
		RETORNAR DATA E HORA 
	'''
	fuso = timezone(timedelta(hours=-3))
	hora = datetime.now()
	hora = hora.astimezone(fuso)
	hora = hora.strftime( "%d/%m/%Y %H:%M:%S" )
	return hora


#####################################
'''
	Funções de verificação licenca
'''
#####################################


class LicencaConf():
	
	def __init__(self):

		file     = "./licenca.key"
		chaveKey = b'' #No Arquivvo Local

		with open(file, 'rb') as f:
		    data = f.read()

		fernet = Fernet(chaveKey)
		encrypted = fernet.decrypt(data)

		info = encrypted.decode('utf-8')

		self.licenca = ast.literal_eval(info) 


	def getNome(self):
		return self.licenca['NOME']

	def getEmail(self):
		return self.licenca['EMAIL']

	def getDataExp(self):
		return self.licenca['DATAEXP']

	def getVersion(self):
		return self.licenca['VERSION']
