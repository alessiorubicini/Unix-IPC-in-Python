'''

Utilizzo semafori POSIX in Python

Sviluppato da Alessio Rubicini

Versione Python: 3.8.2

'''


# ------------ MODULI -----------------------

import posix_ipc as ipc
import os                   # Funzioni di sistema (es. fork)
import time                 # Modulo time per sleep()

# ------------ ESECUZIONE --------------------


'''
Creazione semaforo

Parametri:
    - Chiave: deve essere None, IPC_PRIVATE o un intero. Se è None il modulo sceglie una chiave random non utilizzata
    - Flag: 0 (default) apre un semaforo esistente, IPC_CREAT apre o crea il semaforo se non esiste, IPC_CREX crea un semaforo e restituisce errore se già esiste
    - Mode: permessi
    - Initial_value: valore a cui viene inizializzato il semaforo
'''
try:
    sem = ipc.Semaphore("/semaforo", ipc.O_CREAT, initial_value=1)
except ipc.Error as errore:
    print("ERRORE:", errore)
    exit()
    

print("Semaforo creato con nome '/semaforo'")


# Fork
pid = os.fork()


# Controllo errore fork
if pid < 0:
    print("Errore fork")
    exit()

# Processo figlio
if pid == 0:

    # Apre il semaforo creato precedentemente
    child_sem = ipc.Semaphore("/semaforo")

    with child_sem:
        print("Figlio: ho acquisito il semaforo con nome '/semaforo")
        
        # REGIONE CRITICA
        # Scrive qualcosa sul file
        with open("prova.txt", "w") as file:
            file.write("Ciao a tutti, sono il processo figlio")
        
        print("Figlio: file scritto, rilascio il semaforo")
        # Aspetta 3 secondi
        time.sleep(2)

        # Uscendo dal costrutto 'With' rilascia il semaforo

# Processo padre
elif pid > 0:
    
    # Rilascia il semaforo
    sem.release()
    print("Padre: rilascio il semaforo per il figlio")

    # Aspetta 1 secondo per dare al figlio la possibilità di acquisire il semaforo
    time.sleep(1)

    # Aspetta che il figlio rilasci il semaforo
    sem.acquire(10)

    # Legge cosa ha scritto il figlio nel file
    with open("prova.txt", "r") as file:
        print("Il padre ha letto: " + file.read())

    # Rilascia ed elimina il semaforo
    print("Padre: elimino il semaforo")

    try:
        sem.unlink()
    except ipc.Error as errore:
        print("ERRORE:", errore)
        exit()
    
    print("Padre: semaforo rilasciato ed eliminato con successo")
