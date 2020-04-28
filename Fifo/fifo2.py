# Comunicazione tra processi con fifo in Python
# Alessio Rubicini - Classe 4INC - I.T.T. Montani di Fermo
# Python 3.6.9


# Processo che apre la fifo


# ---------------------------------------------------------------
# Moduli

import os

# ---------------------------------------------------------------
# Programma principale

# Path della fifo
path = "./myfifo"

while True:

	# Apertura fifo in lettura
	fifo = open(path, 'r')

	# Lettura dalla fifo
	for line in fifo:
		print("User1: ", line)

	# Chiusura della fifo
	fifo.close()


	# Input messaggio
	msg = input("Scrivi messaggio: ")

	# Apertura fifo in scrittura
	fifo = open(path, 'w')

	# Scrittura del messaggio
	fifo.write(msg)

	# Chiusura della fifo
	fifo.close()
