from datetime import datetime, timedelta
from time import strftime

# now = datetime.now()
# print( now )
# print( now - timedelta( seconds=5 ) )
# print( now.strftime( '%H:%M:%S' ) )




##### TESTE PARA VOLTA DE HORA #####
hora  = "13:30"
cHora = datetime.strptime( hora, "%H:%M" )
vHora = cHora - timedelta(seconds=5)
print( cHora.strftime( '%H:%M:%S' ) )
print( vHora.strftime( '%H:%M:%S' ) )
#####################################
