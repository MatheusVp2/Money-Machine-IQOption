from datetime import datetime, timedelta
from time import strftime

# now = datetime.now()
# print( now )
# print( now - timedelta( seconds=5 ) )
# print( now.strftime( '%H:%M:%S' ) )

##### TESTE PARA VOLTA DE HORA #####
hora  = "13:30:00"
# cHora = datetime.strptime( hora, "%H:%M" )
# vHora = cHora - timedelta(seconds=5)
# print( cHora.strftime( '%H:%M:%S' ) )
# print( vHora.strftime( '%H:%M:%S' ) )
#####################################

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
	vHora     = cHora - timedelta(seconds=30)
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
	elif delay > 0 and delay <= 15:
		cHora       = datetime.strptime( timeEntrada , formato )
		vHora       = cHora - timedelta(seconds=delay)
		timeEntrada = vHora.strftime( '%H:%M:%S' )
		return timeEntrada
	else:
		cHora       = datetime.strptime( timeEntrada , formato )
		vHora       = cHora - timedelta(seconds=15)
		timeEntrada = vHora.strftime( '%H:%M:%S' )
		return timeEntrada




