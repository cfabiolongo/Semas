# pip install Flask

from flask import Flask, request, jsonify

app = Flask(__name__)

# Funzione per elaborare il testo
def elabora_testo(testo):
    return testo.upper()  # Esempio: converti il testo in maiuscolo

# Route per gestire le richieste POST
@app.route('/elabora-testo', methods=['POST'])
def elabora_testo_route():
    # Verifica che il corpo della richiesta contenga JSON
    if not request.json or 'testo' not in request.json:
        return jsonify({'errore': 'Formato JSON non valido'}), 400
    
    testo_da_elaborare = request.json['testo']
    
    # Elabora il testo utilizzando la funzione 'elabora_testo'
    testo_elaborato = elabora_testo(testo_da_elaborare)
    
    # Crea e ritorna una risposta JSON con il testo elaborato
    return jsonify({'testo_elaborato': testo_elaborato}), 200

if __name__ == '__main__':
    app.run(port=5000)  # Avvia il server Flask sulla porta 5000
    
    
# Con questo script, il servizio REST sarà in grado di gestire le richieste POST inviate
# a http://localhost:5000/elabora-testo. Ad esempio, puoi inviare una richiesta POST utilizzando
# curl o uno strumento come Postman:

# curl -X POST -H "Content-Type: application/json" -d '{"testo": "Hello, World!"}' http://localhost:5000/elabora-testo

# questo dovrebbe restituire una risposta simile a:

# {
#  "testo_elaborato": "HELLO, WORLD!"
# }

# In questo esempio, elabora_testo è una funzione molto semplice che converte il testo in
# maiuscolo. Potresti sostituire questa funzione con qualsiasi altra elaborazione desiderata.
