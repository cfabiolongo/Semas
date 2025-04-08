import cv2

# Apri la webcam (0 di solito è la webcam predefinita)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Errore: Impossibile accedere alla webcam")
    exit()

# Leggi un singolo frame
ret, frame = cap.read()

if ret:
    # Salva l'immagine
    cv2.imwrite("images/immagine_webcam.jpg", frame)
    print("Immagine salvata come 'immagine_webcam.jpg'")
else:
    print("Errore: Impossibile catturare l'immagine")

# Rilascia la webcam
cap.release()
cv2.destroyAllWindows()
