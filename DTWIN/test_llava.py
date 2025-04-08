import requests
import json
import base64
import os

# Endpoint locale di Ollama
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# CONTEXTO GLOBALE
CONTEXT = """Estrai regole (senza altro testo aggiuntivo) dalla frase in questa forma (ad esempio): Quando la temperatura dell'auto è maggiore di 200, la velocità diminuisce a 50 km/k ----> TEMPERATURE(200)  >> [-VEHICLE_SPEED(50), +VEHICLE_SPEED(50)]

Estrai soltanto beliefs dalla frase in questa forma (ad esempio): La temperatura è 35 gradi ----> TEMPERATURE(35)
"""

# Funzione per convertire un'immagine in base64
def image_to_base64(image_path):
    if not os.path.exists(image_path):
        print(f"[Errore] Immagine non trovata: {image_path}")
        return None
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Funzione per inviare prompt + immagine a Ollama in streaming
def ask_ollama_stream(prompt, image_path=None, model="llava:latest"):
    full_prompt = CONTEXT + "\n" + prompt
    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": True
    }

    # Se è specificata un'immagine, la carica e la include
    if image_path:
        base64_image = image_to_base64(image_path)
        if base64_image:
            payload["images"] = [base64_image]
        else:
            print("Impossibile includere immagine. Continuo solo con il testo.")

    try:
        with requests.post(OLLAMA_API_URL, json=payload, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    try:
                        token_json = json.loads(line.decode('utf-8'))
                        print(token_json.get("response", ""), end="", flush=True)
                    except json.JSONDecodeError as e:
                        print(f"\n[Errore parsing token JSON]: {e}")
            print()  # newline finale
    except requests.exceptions.RequestException as e:
        print(f"Errore nella richiesta: {e}")

# Loop interattivo
if __name__ == "__main__":
    print("Chat con il modello multimodale (digita 'esci' per terminare)")
    while True:
        user_input = input("\nTu: ")
        if user_input.lower() in ["esci", "exit", "quit"]:
            print("Uscita dalla chat.")
            break

        # Opzionalmente chiedi se c'è un'immagine da allegare
        image_name = input("immagine_webcam.jpg").strip()
        image_path = os.path.join("images", image_name) if image_name else None

        ask_ollama_stream(user_input, image_path=image_path)
