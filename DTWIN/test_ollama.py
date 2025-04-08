import requests
import json

# Endpoint locale di Ollama
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# CONTEXTO GLOBALE — puoi personalizzarlo
CONTEXT = """Rispondi sempre True oppure False circa la veridicità della seguente affermazione:
"""

# Funzione per inviare richieste in streaming
def ask_ollama_stream(prompt, model="deepseek-r1:14b-qwen-distill-q8_0"):
    # Combina contesto + prompt utente
    full_prompt = CONTEXT + "\n" + prompt

    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": True  # Abilita lo streaming token per token
    }

    try:
        with requests.post(OLLAMA_API_URL, json=payload, stream=True) as response:
            response.raise_for_status()
            print("Risposta del modello:\n")
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

# Loop interattivo da linea di comando
if __name__ == "__main__":
    print("Chat con il modello (digita 'esci' per terminare)")
    while True:
        user_input = input("\nTu: ")
        if user_input.lower() in ["esci", "exit", "quit"]:
            print("Uscita dalla chat.")
            break
        ask_ollama_stream(user_input)
