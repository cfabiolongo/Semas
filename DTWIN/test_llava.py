import base64
import requests

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def describe_image(image_path, model="llava:13b-v1.6-vicuna-q8_0", temperature=0.7):
    image_base64 = image_to_base64(image_path)

    # Messaggio da inviare al modello
    data = {
        "model": model,
        "prompt": "descrivi l’immagine",
        "images": [image_base64],
        "temperature": temperature,
        "stream": False
    }

    try:
        response = requests.post("http://localhost:11434/api/generate", json=data)

        if response.status_code == 200:
            result = response.json()
            return result.get("response", "Nessuna risposta dal modello.")
        else:
            return f"Errore: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return "Errore: impossibile connettersi a Ollama. Verifica che sia in esecuzione su http://localhost:11434."


# Esempio di utilizzo
if __name__ == "__main__":
    image_path = "images/immagine_webcam.jpg"  # <-- Cambia con il percorso della tua immagine
    temperatura = 0.1
    usa_stream = True  # imposta a True per usare streaming
    descrizione = describe_image(image_path, temperature=temperatura)
    print("Descrizione dell'immagine:")
    print(descrizione)