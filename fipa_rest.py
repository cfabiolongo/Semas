from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/parse_rdf', methods=['POST'])
def parse_rdf():
    # Ricevi il payload XML dalla richiesta POST
    rdf_data = request.data.decode('utf-8')

    # Parse del contenuto XML
    root = ET.fromstring(rdf_data)

    # Namespaces da gestire
    namespaces = {
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'fipa': 'http://www.fipa.org/schemas/fipa-rdf0#'
    }

    # Estrai le informazioni
    subj = root.find('.//rdf:subject', namespaces).text
    predicate = root.find('.//rdf:predicate', namespaces).attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'].split('#')[-1]
    obj = root.find('.//rdf:object', namespaces).text
    belief = root.find('.//fipa:belief', namespaces).text

    # Restituisci i dati in formato JSON

    semas_belief = f"{predicate}({subj}, {obj})"

    response = {
        'subject': subj,
        'predicate': predicate,
        'object': obj,
        'belief': belief,
        'Semas-belief': semas_belief
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)



# curl -X POST http://localhost:5000/parse_rdf \
# -H "Content-Type: application/xml" \
# -d '<?xml version="1.0"?>
# <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
# xmlns:fipa="http://www.fipa.org/schemas/fipa-rdf0#">
# <fipa:Proposition>
# <rdf:subject>TCP/IP Illustrated</rdf:subject>
# <rdf:predicate rdf:resource="http://description.org/schema#author"/>
# <rdf:object>W. Richard Stevens</rdf:object>
# <fipa:belief>true</fipa:belief>
# </fipa:Proposition>
# </rdf:RDF>'
