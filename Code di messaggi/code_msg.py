# Scambio informazioni tra processi con coda di messaggi System V
# Alessio Rubicini - Classe 4INC - I.T.T. Montani di Fermo (A.S. 2019/20)
# Python 3.6.9

# -------------------------------------------------------------------------------------------
# Moduli
from sysv_ipc import *		# Sistemi di IPC System V
import os 					# Operazioni di sistema operativo

# -------------------------------------------------------------------------------------------
# Programma principale

# Prende in input la chiave da assegnare alla coda con input controllato
key = -1
while key < 0:

    key = int(input("Inserisci key: "))


print("Creo una coda con key ", key)


# Creazione coda con flag O_CREAT (apre una coda esistente, se non esiste la crea)
coda = MessageQueue(key, flags=IPC_CREAT, mode=660, max_message_size=2048)

if coda is None:
    print("Errore nella creazione/apertura della coda di messaggi")
    exit()

# Creazione nuovo processo con fork
pid = os.fork()

# Controlla fork
if pid == -1:
    print("Errore chiamata fork()")
    exit()

# Processo figlio
if pid == 0:

    # Riceve il messaggio
    messaggio = coda.receive(block=True, type=1)

    # Modifica il messaggio
    print("Il processo figlio ha letto dalla coda: ", messaggio)

    # Decodifica il messaggio ricevuto
    messaggio = messaggio[0].decode("utf-8")

    # Trasforma il messaggio
    messaggio = messaggio.upper()

    # Rimanda il messaggio sulla coda
    coda.send(messaggio, block=True, type=1)

# Processo padre
else:

    # Prende in input il messaggio dall'utente
    input_msg = input("Scrivi messaggio: ")

    # Invia il messaggio preso in input
    coda.send(input_msg, block=True, type=1)

    # Aspetta termine del processo figlio
    os.waitpid(pid, 0)

    # Riceve il messaggio modificato
    messaggio = coda.receive(block=True, type=1)

    # Decodifica il messaggio ricevuto
    messaggio = messaggio[0].decode("utf-8")

    # Lo stampa
    print("Il processo padre ha letto dalla coda: ", messaggio)

    # Rimuove la coda di messaggi
    coda.remove()
