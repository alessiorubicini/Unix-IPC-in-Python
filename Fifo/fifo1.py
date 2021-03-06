# Comunicazione tra processi con fifo in Python
# Alessio Rubicini - Classe 4INC - I.T.T. Montani di Fermo
# Python 3.6.9


# Processo che crea la fifo


# ---------------------------------------------------------------
# Moduli

import os

# ---------------------------------------------------------------
# Programma principale

# Path della fifo
path = "./myfifo"

# Creazione fifo
os.mkfifo(path, 666)

while True:

	# Input messaggio
	msg = input("Scrivi messaggio: ")

	# Apertura fifo in scrittura
	fifo = open(path, 'w')

	# Scrittura del messaggio
	fifo.write(msg)

	# Chiusura della fifo
	fifo.close()


	# Apertura fifo in lettura
	fifo = open(path, 'r')

	# Lettura dalla fifo
	for line in fifo:
		print("User2: ", line)

	# Chiusura della fifo
	fifo.close()
