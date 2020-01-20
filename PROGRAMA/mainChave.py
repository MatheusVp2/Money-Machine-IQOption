#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
	Importações
'''
from botTraderApi import *
from botApiLicenca import *
import time
from iqoptionapi.stable_api import IQ_Option
import os, sys
from os.path import exists


def main():

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

		if getValidadeLicenca() != True:
			print("|-----| Validade da Licenca Expirada |-----|")
			print("|-----| Renove caso queira continuar utilizar o BOT |-----|")
			print('\n')
			os.system("timeout /t 5")
			os.system('exit')

		print('\n')
		print(f"{ getHoraNow() } - |-----| Iniciando BOT |-----| ")
		print('')

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

			print('')
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
				ALL_Asset  = I_want_money.get_all_open_time() # API para pegar todas as informações dos ativos
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
				if pulaEntrada == False:
					print()
					print(f"{ getHoraNow() } - |-----| Ativo não esta Aberto {ativo} |-----| ")
					print()

			nextEntrada += 1
			if nextEntrada >= qtdEntradas:
				print('\n')
				print(f"{ getHoraNow() } - |-----| Acabou as entradas |-----|")
				print(f"{ getHoraNow() } - |-----| Verifique as Entradas |-----|")
				print(f"{ getHoraNow() } - |-----| Saindo do Programa |-----|")
				os.system("pause")
				break

			



	else:
		print('\n')
		print("Obrigado estou saindo !")
		os.system("timeout /t 5")



if __name__ == '__main__':

	os.system('cls')

	print()
	print("|-----| Bem Vindo ao Machine Money |-----|")
	time.sleep(1)
	print()
	print("|-----| Estou verificando sua licenca aguarde |-----|")
	print()
	time.sleep(1)

	fileLicenca = "./licenca.key"
	fileTrader  = "./trader.txt"
	fileConfig  = "./config.ini"

	if exists(fileLicenca):
		print("|-----| Verificando Arquivo de Licenca |-----|")
		print()
		time.sleep(1)
		nome     = LicencaConf().getNome()
		email    = LicencaConf().getEmail()
		dataexp  = LicencaConf().getDataExp()
		versiion = LicencaConf().getVersion()
		print('|-----| Informações da Licenca |-----|')
		print()
		print(f'|-----| Nome : {nome} |-----|')
		print(f'|-----| Email : {email} |-----|')
		print(f'|-----| Data Validade : {dataexp} |-----|')
		print(f'|-----| Nome : {nome} |-----|')
		print()
		time.sleep(1)

		if exists(fileTrader):
			print("|-----| Verificando Arquivo de Entradas |-----|")
			print()
			time.sleep(1)
			print("|-----| Arquivo de Entradas OK |-----|")
			print()
			print("|-----| Certifique se as entradas esteja no padrão |-----|")
			print("|-----| Padrão  : TEMPO;ATIVO;HORARIO;AÇAO |-----|")
			print("|-----| Exemplo : 1;AUDUSD;02:17:00;PUT |-----|")
			print()
			time.sleep(1)

			if exists(fileConfig):
				print("|-----| Verificando Arquivo de Configuração |-----|")
				print()
				time.sleep(1)
				print("|-----| Arquivo de Configuração OK |-----|")
				print()
				print("|-----| Certifique se as informações contidas neles estao corretas |-----|")
				print("|-----| Para nao haver problema nas entradas |-----|")
				print()
				time.sleep(1)

				print("|-----| Verificando Validade da Licenca ( EMAIL ) |-----|")
				print()
				time.sleep(1)
				emailconfig = CFG().getEmail()

				if email == emailconfig:
					print("|-----| Verificando Validade da Licenca ( DATA ) |-----|")
					print()
					time.sleep(1)

					if getDataPassada( getDateTimeNow(), dataexp ) > 0:
						print("|-----| Validade da Licenca OK |-----|")
						print()
						print("|-----| Abrindo o BOT |-----|")
						print()
						time.sleep(1)
						os.system("timeout /t 5")

						main()
						
					else:
						print("|-----| Validade da Licenca Expirada |-----|")
						print("|-----| Renove caso queira continuar utilizar o BOT |-----|")
						print('\n')
						os.system("timeout /t 5")
						os.system('exit')

				else:
					print("|-----| Verifique se o email e o mesmo da licenca no config |-----|")
					print("|-----| Sendo o mesmo a operar no IQ OPTION |-----|")
					print('\n')
					os.system("timeout /t 5")
					os.system('exit')


			else:
				print("|-----| Verifique se o arquivo => config.ini |-----|")
				print("|-----| Se esta no local correto ou se existe |-----|")
				print('\n')
				os.system("timeout /t 5")
				os.system('exit')

		else:
			print("|-----| Verifique se o arquivo => trader.txt |-----|")
			print("|-----| Se esta no local correto ou se existe |-----|")
			print('\n')
			os.system("timeout /t 5")
			os.system('exit')

	else:
		print("|-----| Verifique se o arquivo => licenca.key |-----|")
		print("|-----| Se esta no local correto ou se existe |-----|")
		print('\n')
		os.system("timeout /t 5")
		os.system('exit')



    # main()