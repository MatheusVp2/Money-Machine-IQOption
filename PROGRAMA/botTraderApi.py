#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################
'''
	Importações Gerais
'''

from time import strftime, time, sleep
from datetime import datetime, timezone, timedelta
import configparser

#####################################


#####################################
'''
	Informações sobre leitura das entradas
'''
#####################################

# RETORNA AS ENTRADAS EM MATRIZ ( TIME | ATIVO | HORARIO | DIREÇAO )
def getEntradas():
	'''
	RETORNAR MATRIZ DE ENTRADAS COM PADRAO ( TIME | ATIVO | HORARIO | DIREÇAO )
	'''
	arq = open('trader.txt', 'r')
	entradas = arq.read().splitlines()
	arq.close()

	lista = []
	for i in entradas:
		lista.append(i.split(';'))

	return lista


#####################################
'''
	Funções para controle de horas
'''
#####################################

# TRAVANDO O HORARIO COM O FUSO HORARIO UTC-3
def getHoraNow():
	'''
	DEFINE COMO PADRAO O HORARIO UTC-3
	'''
	fuso = timezone(timedelta(hours=-3))
	hora = datetime.now()
	hora = hora.astimezone(fuso)
	hora = hora.strftime( '%H:%M:%S' )
	return hora

# VERIFICA SE O HORARIO JA PASSOU
def  verificaHoraPassada(horaAgora, horaEntrada):
	'''
		VERIFICA SE O HORARIO JA PASSOU = (horaAgora, horaEntrada)
	'''
	return  (datetime.strptime(horaEntrada, '%H:%M:%S') - datetime.strptime(horaAgora, '%H:%M:%S')).total_seconds()

# FUNÇÃO PARA VOLTAR A HORA E VERIFICAR O ATIVO 30 SEGUNDOS ANTES
def timeVerificaAtivo(timeEntrada):
	'''
	ENTRA COM A HORA DA ENTRADA
	E RETORNA 30 SEGUNDOS ANTES PARA VERIFICAÇÃO DO ATIVO
	'''

	# LOGICA PARA ERRO DE FORMATAÇÃO
	if len( timeEntrada.split(":") ) == 3:
		formato = "%H:%M:%S"
	else:
		formato = "%H:%M"
	# LOGICA PARA VOLTA DO HORARIO VERIFICADOR
	cHora     = datetime.strptime( timeEntrada , formato )
	vHora     = cHora - timedelta(seconds=12)
	timeAtivo = vHora.strftime( '%H:%M:%S' )
	return timeAtivo


# FUNÇÃO PARA PODER CRIAR O DELAY DA ENTRADA
def delayEntrada(delay, timeEntrada):
	'''
	ENTRA COM O DELAY E A HORA DA ENTRADA
	E RETORNA A NOVA HORA DA ENTRADA
	'''

	# LOGICA PARA ERRO DE FORMATAÇÃO
	if len( timeEntrada.split(":") ) == 3:
		formato = "%H:%M:%S"
	else:
		formato = "%H:%M"
	# LOGICA PARA O DELAY
	if delay <= 0:
		cHora       = datetime.strptime( timeEntrada , formato )
		timeEntrada = cHora.strftime( '%H:%M:%S' )
		return timeEntrada
	elif delay > 0 and delay <= 5:
		cHora       = datetime.strptime( timeEntrada , formato )
		vHora       = cHora - timedelta(seconds=delay)
		timeEntrada = vHora.strftime( '%H:%M:%S' )
		return timeEntrada
	else:
		cHora       = datetime.strptime( timeEntrada , formato )
		vHora       = cHora - timedelta(seconds=5)
		timeEntrada = vHora.strftime( '%H:%M:%S' )
		return timeEntrada

#####################################
'''
	Classe do Arquivo de Configuração
'''
#####################################

class CFG():
	
	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config.read("config.ini")

	def getEmail(self):
		return self.config["CONTA"]["EMAIL"]

	def getSenha(self):
		return self.config["CONTA"]["SENHA"]

	def getTipoConta(self):
		return self.config["CONTA"]["TIPO"]

	def getDinheiro(self):
		return self.config["ENTRADA"]["VALOR"]

	def getGale(self):
		return self.config["ENTRADA"]["GALE"]

	def getQtdGale(self):
		return self.config["ENTRADA"]["QTDGALE"]

	def getGaleMult(self):
		return self.config["ENTRADA"]["MULTGALE"]