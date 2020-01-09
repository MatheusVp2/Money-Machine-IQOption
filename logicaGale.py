entradas = [ [ 5, "AUDUSD", "12:00", "CALL" ] ,
			 [ 5, "AUDUSD", "12:05", "CALL" ] ,
			 [ 5, "AUDUSD", "13:00", "CALL" ] ,
			 [ 5, "AUDUSD", "13:00", "CALL" ] 
		   ]

valorEntrada = 3

galeAtivo = True
qtdGale   = 2
galeMultiplicador = 2.1

iniEntradas = 0
qtdEntradas = len(entradas)

for i in entradas:
	bGale     = 1

	print("Entrada: ", i)
	print("Valor : ", valorEntrada)
	print()

	valor = int(input("Acertou entrada : "))
	print()

	vGale = valorEntrada
	while (galeAtivo and valor == 0 and bGale <= qtdGale):
		print("Entrando com Gale : ", i)
		print("Valor : ", vGale * galeMultiplicador)

		print()
		valor = int(input("Acertou entrada : "))
		print()

		if valor == 0:
			vGale = vGale * galeMultiplicador
			bGale +=1

