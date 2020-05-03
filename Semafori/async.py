'''

Utilizzo semafori con modulo asyncio

Sviluppato da Alessio Rubicini

Versione Python: 3.8.2

'''


# ----------------- MODULI -----------------------

import asyncio as sync      # Modulo asyncio
import os                   # Funzioni di sistema (es. fork)
import time                 # Modulo time per sleep()

# ---------------- ESECUZIONE --------------------


# Creazione semaforo
try:
    sem = sync.Semaphore(10)
except ipc.Error as errore:
    print(errore)
    exit()
    
print("Semaforo creato con chiave 10")


# Acquisice il semaforo
sem.acquire()

# Fork
try:
    pid = os.fork()
except:
    print("Errore fork()")
    exit()

# Processo figlio
if pid == 0:

    # Con il semaforo acquisito
    sem.acquire()

    print("Figlio: ho acquisito il semaforo con chiave 10")
        
    # Scrive qualcosa sul file
    with open("prova.txt", "w") as file:
        file.write("Ciao a tutti, sono il processo figlio")
        
    # Aspetta 3 secondi
    time.sleep(3)

    # Uscendo dal costrutto 'With' rilascia il semaforo


# Processo padre
elif pid > 0:
    
    # Legge il contenuto iniziale del file
    with open("prova.txt", "r") as file:
        print("Contenuto iniziale del file: " + file.read())
    
    # Rilascia il semaforo
    sem.release()
    print("Padre: rilascio il semaforo per il figlio")

    # Aspetta 1 secondo per dare al figlio la possibilità di acquisire il semaforo
    time.sleep(1)

    # Aspetta che il figlio rilasci il semaforo
    sem.acquire()

    # Legge cosa ha scritto il figlio nel file
    with open("prova.txt", "r") as file:
        print("Il padre ha letto: " + file.read())


