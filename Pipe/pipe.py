# Comunicazione tra processi con pipe in Python
# Alessio Rubicini - Classe 4INC - I.T.T. Montani di Fermo
# Python 3.6.9

# ---------------------------------------------------------------
# Moduli

import os

# ---------------------------------------------------------------
# Programma principale

# Crea la pipe restituendo i due descrittori di lettura e scrittura
r, w = os.pipe()

# Creazione nuovo processo tramite fork()
pid = os.fork()

if pid == -1:
    print("Errore fork")
    exit()

# Processo figlio
if pid == 0:

    # Chiude descrittore di lettura
    os.close(r)

    # Prende in input il messaggio dall'utente
    msg = input("Sono il processo figlio. Scrivi qualcosa: ")

    # Apre il descrittore di scrittura
    w = os.fdopen(w, 'w')

    # Scrive il messaggio sulla pipe
    w.write(msg)


# Processo padre
else:

    # Aspetta il termine del processo figlio
    os.waitpid(pid, 0)

    # Chiude descrittore di scrittura
    os.close(w)

    # Apre descrittore di lettura
    r = os.fdopen(r)

    # Legge il messaggio dalla pipe
    msg = r.read()

    # Stampa il messaggio
    print("Sono il padre, ho letto: ", msg)
