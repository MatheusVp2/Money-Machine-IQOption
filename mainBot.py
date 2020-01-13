#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
	Importações
'''
from botTraderApi import *
import time
from iqoptionapi.stable_api import IQ_Option
import os, sys

'''
	Codigo Principal
'''

os.system("cls")

# Logando na IQ_Option
print(f"{ getHoraNow() } - |-----| LOGANDO IQ_OPTION |-----| ")
email = CFG().getEmail()
senha = CFG().getSenha()
I_want_money = IQ_Option( email , senha )


# Verifica qual tipo de conta 
getTipoConta = CFG().getTipoConta()
if getTipoConta.upper()  == "DEMO":
	tipoConta = "PRACTICE"
else:
	tipoConta = "REAL"


# Aciona a conta a ser operada
print(f"{ getHoraNow() } - |-----| CONTA { getTipoConta.upper() } |-----| ")
I_want_money.change_balance( tipoConta ) # MODE: "PRACTICE" / "REAL"

print()

# Mostrando Informações basicas de Configuração
print( f"{ getHoraNow() } - |-----| Informações |-----| " )
print()
print('## Valor das Entradas: ', CFG().getDinheiro().upper() )
print('## Entradas com Gale : ', CFG().getGale().upper() )
if CFG().getGale().upper() == "ON":
	print('## Quantidade de Gales: ', CFG().getQtdGale() )
	print('## Multiplicador do Gale: ', CFG().getGaleMult() )
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

	valorEntrada      = int( CFG().getDinheiro() )
	entradas          = getEntradas()
	galeAtivo         = True if CFG().getGale().upper() == "ON" else False
	
	qtdGale           = int( CFG().getQtdGale() )
	galeMultiplicador = float( CFG().getGaleMult() )

	nextEntrada = 0
	qtdEntradas = len(entradas)
	
	timeVerificado = getHoraNow()

	
	
	for go in entradas:
		bGale = 1 # reseta o gale pra um sempre na proxima entreda
		vGale = valorEntrada # base da entrada para poder fazer os calculos dos gales
		
		pulaEntrada = False # Verificado para pular entrada

		duration = int(go[0])
		ativo    = go[1]
		btime    = go[2]
		action   = go[3].lower()

		while True:

			hora = getHoraNow()
			sys.stdout.write("\r" + f"{ getHoraNow() } - |-----| Aguardando Tempo |-----| ")
			if verificaHoraPassada( hora, btime ) < 0:
				print('\n')
				print(f"{ getHoraNow() } - |-----| Entrada ja Passou |-----| ")
				print(f"{ getHoraNow() } - |-----| Tempo: {duration} - Moeda: {ativo} - Tempo: {btime} - Ação: {action.upper()} |-----| ")
				print()
				pulaEntrada = True
				break

			if hora == timeVerificaAtivo( btime ):
				print('\n')
				break
			time.sleep(1)

		if pulaEntrada == False:
			print()
			print(f"{ getHoraNow() } - |-----| Verificando Ativo ( { ativo } ) |-----| ")
			print()
			ALL_Asset=I_want_money.get_all_open_time() # API para pegar todas as informações dos ativos
			moedaAtiva = ALL_Asset["turbo"][go[1]]["open"] # API Verificando o Ativo
		else:
			moedaAtiva = False

		if moedaAtiva:

			print()
			print(f"{ getHoraNow() } - |-----| Aguardando Entrada |-----| ")
			print(f"{ getHoraNow() } - |-----| Tempo: {duration} - Moeda: {ativo} - Tempo: {btime} - Ação: {action.upper()} |-----| ")
			print(f"{ getHoraNow() } - |-----| Valor de Entrada : {valorEntrada} |-----| ")
			print()

			while True:
				hora = getHoraNow()
				sys.stdout.write("\r" + f"{ getHoraNow() } - |-----| Aguardando Tempo |-----| ")
				if hora == btime:
					print('\n')
					break
				time.sleep(1)

			isTrue, id_entrada = I_want_money.buy(valorEntrada, ativo, action, duration) # Fazendo entrada
			if isTrue:
				print()
				print(f"{ getHoraNow() } - |-----| Verificando Entrada : {id_entrada} - Valor Entrada: {valorEntrada} |-----| ")
				print(f"{ getHoraNow() } - |-----| Tempo: {duration} - Moeda: {ativo} - Tempo: {btime} - Ação: {action.upper()} |-----| ")
				print()
				while I_want_money.get_betinfo(id_entrada)[0] == False : # Verificando a Entrada
					pass
				isTrue, result = I_want_money.get_betinfo( id_entrada ) # Verificando a Entrada
				id_entrada     = str(id_entrada)
				resultEntrada  = result["result"]["data"][id_entrada]['win'] # Pega o resultado da entrada
				print()
				print(f"{ getHoraNow() } - |-----| Resultado Entrada : {resultEntrada.upper()} |-----| ")
				print()
				winORloose     = False if resultEntrada == 'win' else True

			else:
				winORloose = False


			while (galeAtivo and winORloose and bGale <= qtdGale):
				print()
				print("Entrando com Gale : ", go)
				print("Valor : ", vGale * galeMultiplicador)
				print()

				valorGale = vGale * galeMultiplicador

				isTrue, id_entrada = I_want_money.buy(valorGale , ativo, action, duration) # Fazendo entrada
				if isTrue:
					print()
					print(f"{ getHoraNow() } - |-----| Verificando Entrada : {id_entrada} - Valor Entrada: {valorGale} |-----| ")
					print(f"{ getHoraNow() } - |-----| Tempo: {duration} - Moeda: {ativo} - Tempo: {btime} - Ação: {action.upper()} |-----| ")
					print()
					while I_want_money.get_betinfo(id_entrada)[0] == False : # Verificando a Entrada
						pass
					isTrue, result = I_want_money.get_betinfo( id_entrada ) # Verificando a Entrada
					id_entrada     = str(id_entrada)
					resultEntrada  = result["result"]["data"][id_entrada]['win'] # Pega o resultado da entrada
					print()
					print(f"{ getHoraNow() } - |-----| Resultado Entrada : {resultEntrada.upper()} |-----| ")
					print()
					winORloose     = False if resultEntrada == 'win' else True
				else:
					winORloose = False

				if winORloose == True:
					vGale = vGale * galeMultiplicador
					bGale +=1
		else:
			print()
			print(f"{ getHoraNow() } - |-----| Ativo não esta Aberto {ativo} |-----| ")
			print()

		nextEntrada += 1
		if nextEntrada >= qtdEntradas:
			print('\n')
			print(f"{ getHoraNow() } - |-----| Acabou as entradas |-----|")
			print(f"{ getHoraNow() } - |-----| Saindo do Programa |-----|")
			os.system("timeout /t 5")
			os.system("exit")
			break

		



else:
	print('\n')
	print("Obrigado estou saindo !")
	os.system("timeout /t 5")
