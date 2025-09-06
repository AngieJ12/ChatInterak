from flask import Flask, render_template, request, jsonify
import spacy
import re

# Cargar modelo de spaCy en español
nlp = spacy.load("es_core_news_sm")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"].strip()

    # Saludo inicial
    if not hasattr(app, 'saludo_iniciado') or not app.saludo_iniciado:
        if user_msg.lower() == "hola":
            app.saludo_iniciado = True
            return jsonify({
                "user": user_msg,
                "bot": "¡Hola! Soy tu asistente de gramática. Escríbeme una frase y te explicaré cómo funciona la tokenización, la lematización y el POS tagging.",
                "analisis": []
            })
        else:
            return jsonify({
                "user": user_msg,
                "bot": "Por favor inicia el chat diciendo 'HOLA'.",
                "analisis": []
            })

    # Despedida
    if user_msg.lower() == "chao":
        app.saludo_iniciado = False
        return jsonify({
            "user": user_msg,
            "bot": "¡Hasta luego! Gracias por practicar conmigo.",
            "analisis": []
        })

    # --- Procesamiento con spaCy ---
    doc = nlp(user_msg)

    # Tokenización (dividir el texto en palabras y signos)
    tokens_regex = re.findall(r'\w+|[^\w\s]', user_msg, re.UNICODE)

    # Lemas (forma base de cada palabra)
    lemas = [token.lemma_ for token in doc if not token.is_punct]

    # POS tagging (etiquetar la categoría gramatical de cada palabra)
    pos_tags = [f"{token.text} ({token.pos_})" for token in doc if not token.is_punct]

    # Explicación de cada proceso
    explicacion = f"""
    <b>📌 Explicación de los procesos:</b><br>
    🔹 <b>Tokenización:</b> es el proceso de dividir el texto en unidades mínimas llamadas <i>tokens</i> (palabras, signos).<br>
    ➡ Ejemplo con tu frase: {', '.join(tokens_regex)}<br><br>

    🔹 <b>Lematización:</b> consiste en reducir cada palabra a su forma base o diccionario (lema).<br>
    ➡ Ejemplo con tu frase: {', '.join(lemas)}<br><br>

    🔹 <b>POS tagging:</b> asigna a cada palabra su categoría gramatical (sustantivo, verbo, adjetivo, etc.).<br>
    ➡ Ejemplo con tu frase: {', '.join(pos_tags)}
    """

    return jsonify({
        "user": user_msg,
        "bot": explicacion,
        "analisis": {
            "tokens_regex": tokens_regex,
            "lemmas": lemas,
            "pos": pos_tags
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
