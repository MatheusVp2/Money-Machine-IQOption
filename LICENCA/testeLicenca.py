from cryptography.fernet import Fernet

def gravarChave():

	key = Fernet.generate_key()
	chaveFile = "chavedois.key"
	with open(chaveFile, 'wb') as f:
	    f.write(key)


def gerarLicenca():

	chaveKey    = b'JTcGUnRGzP12ALWeQuif-YAu4yWo0DNbHtgTwHHanCQ='
	input_file  = 'arqBase.txt'
	output_file = 'licenca.key'

	with open(input_file, 'rb') as f:
	    data = f.read()

	fernet    = Fernet(chaveKey)
	encrypted = fernet.encrypt(data)

	with open(output_file, 'wb') as f:
	    f.write(encrypted)


def lerLicenca():

	input_file = 'licenca.key'
	chaveKey    = b'JTcGUnRGzP12ALWeQuif-YAu4yWo0DNbHtgTwHHanCQ='

	with open(input_file, 'rb') as f:
	    data = f.read()

	fernet = Fernet(chaveKey)
	encrypted = fernet.decrypt(data)

	return encrypted.decode('utf-8')

gerarLicenca()