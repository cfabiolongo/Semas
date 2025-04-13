import cv2
import os
from datetime import datetime

# Crea la cartella 'images' se non esiste
if not os.path.exists("images"):
    os.makedirs("images")

# Apri la webcam (0 di solito è la webcam predefinita)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Errore: Impossibile accedere alla webcam")
    exit()

# Leggi un singolo frame
ret, frame = cap.read()

if ret:
    # Ottieni data e ora correnti in formato breve
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Definisci il nome del file con timestamp
    filename = f"images/webcam_{timestamp}.jpg"

    # Salva l'immagine
    cv2.imwrite(filename, frame)
    print(f"Immagine salvata come '{filename}'")
else:
    print("Errore: Impossibile catturare l'immagine")

# Rilascia la webcam
cap.release()
cv2.destroyAllWindows()
