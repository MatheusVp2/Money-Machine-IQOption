#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
	Importações
'''
from botTraderApi import *
import time
from iqoptionapi.stable_api import IQ_Option
import os

'''
	Codigo Principal
'''

os.system("cls")

# Logando na IQ_Option
print(f"{ getHoraNow() } - |-----| LOGANDO IQ_OPTION |-----| ")
# I_want_money = IQ_Option( email , senha )


# Verifica qual tipo de conta 
getTipoConta = CFG().getTipoConta()
if getTipoConta.upper()  == "DEMO":
	tipoConta = "PRACTICE"
else:
	tipoConta = "REAL"


# Aciona a conta a ser operada
print(f"{ getHoraNow() } - |-----| CONTA { getTipoConta.upper() } |-----| ")
# I_want_money.change_balance( tipoConta ) # MODE: "PRACTICE" / "REAL"

print()

# Mostrando Informações basicas de Configuração
print( f"{ getHoraNow() } - |-----| Informações |-----| " )
print()
print('Valor das Entradas: ', CFG().getDinheiro().upper() )
print('Entradas com Gale : ', CFG().getGale().upper() )
print()
print(f"{ getHoraNow() } - |-----| Entradas Programadas |-----|")
print()
for i in getEntradas():
	btime = " " + i[0] if len(i[0]) == 1 else i[0]
	print( f"TEMPO : { btime } - ATIVO : { i[1] } - HORARIO : { i[2] } - DIREÇÂO : { i[3] }" )

print('\n')

startBot = str(input("Deseja inciar o BOT ? [S ou N] : ")).upper()

if startBot == "S" or startBot == "SIM":
	print('\n')
	print(f"{ getHoraNow() } - |-----| Iniciando BOT |-----| ")
	print('\n')

	valorEntrada = CFG().getDinheiro()
	entradas     = getEntradas()
	ativaGale    = True if CFG().getGale().upper() == "ON" else False

	

	nextEntrada = 0
	qtdEntradas = len(entradas)
	

	ativoAnterior = ""
	verificaAtivo = True

	while True:
		entrada = entradas[nextEntrada]

		
		


		nextEntrada += 1
		if nextEntrada >= qtdEntradas:
			print('\n')
			print(f"{ getHoraNow() } - |-----| Acabou as entradas |-----|")
			print(f"{ getHoraNow() } - |-----| Saindo do Programa |-----|")
			os.system("timeout /t 5")
			os.system("exit")
			break

		
		time.sleep(1)




else:
	print('\n')
	print("Obrigado estou saindo !")
	os.system("timeout /t 5")


