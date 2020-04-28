# Scambio di dati con memoria condivisa System V in Python
# Autore: Alessio Rubicini - Classe 4INC - I.T.T. Montani di Fermo (A.S.
# 2019/20)

#-----------------------------------------------------------------------
# Moduli
from sysv_ipc import *
import os

#-----------------------------------------------------------------------
# Programma principale


# Prende in input la chiave del segmento di memoria con input controllato
key = 0
while key < KEY_MIN or key > KEY_MAX:

    key = int(input("Chiave segmento: "))


# Prova ad aprire/creare il segmento
segment = SharedMemory(key, flags=IPC_CREAT, size=100)

if segment is None:
    print("Errore nella creazione/apertura del segmento di memoria")
    exit()


print("Ho aperto/creato il segmento di memoria con chiave ", key)


# Aggancia il processo al segmento di memoria creato
segment.attach(address=None)

print("Segmento di memoria agganciato all'indirizzo ", segment.address)


# Creazione nuovo processo
pid = os.fork()


# Controllo fork
if pid == -1:
    print("Errore fork\n")
    exit()


# Processo figlio
if pid == 0:

    # Legge il messaggio dal segmento di memoria
    messaggio = segment.read(byte_count=0)

    # Decodifica il messaggio
    messaggio = str(messaggio.decode())

    # Trasforma il messaggio
    messaggio = messaggio.upper()

    # Scrive il messaggio trasformato sul segmento di memoria
    segment.write(messaggio, offset=0)


# Processo padre
if pid > 0:
    # Prende in input il messaggio da trasformare
    messaggio = str(input("Scrivi messaggio: "))

    # Scrive messaggio sul segmento di memoria
    segment.write(messaggio, offset=0)

    # Aspetta il figlio
    os.waitpid(pid, 0)

    # Legge dal messaggio
    messaggio = segment.read(byte_count=0)

    # Decodifica il messaggio
    messaggio = str(messaggio.decode())

    # Stampa contenuto
    print("Ho letto: ", messaggio)

# Sgancia il segmento dal processo attuale
segment.detach()

# Elimina il segmento di memoria
segment.remove()
