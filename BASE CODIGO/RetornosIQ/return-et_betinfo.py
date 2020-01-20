# Resultado do GetBetInfo | [ Dicionario Python ]

result = {'isSuccessful': True,
		  'message': [], 
		  'result': {
	  		'exp_value': 1.079759, 
	  		'expired': 1578263880, 
	  		'active': 'front.EURUSD-OTC', 
	  		'active_id': 76, 
	  		'bid': 1.079758, 
	  		'ask': 1.07976, 
	  		'data': {
  				'6013910920': {
  					'deposit': 5, 
  					'value': 1.079718, 
  					'profit': 0, 
  					'direction': 'put', 
  					'created': 1578263820, 
  					'refund': 0, 
  					'profit_income': 187, 
  					'option_type': 'turbo', 
  					'win': 'loose', 
  					'balance_id': 271778734, 
  					'buyback_state': None, 
  					'buyback_time': None, 
  					'client_platform_id': 82}
				}
			}, 
		  'statusCode': 200
		 }

id_entrada = "6013910920"

# Pega Resultado [ win / loose ]
print( result["result"]["data"][id_entrada]['win'] )