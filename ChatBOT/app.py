import re
import difflib
from flask import Flask, request, jsonify

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Dicionário com perguntas e respostas
faq = {
    "que dia acontecem os jogos inter ilhas deste ano": "Dia 07 de Dezembro",
    "como posso melhorar minhas notas": "Estude regularmente e participe das aulas.",
    "quando será o próximo feriado": "O próximo feriado é no dia 15 de novembro.",
    "que dia termina o ano letivo de 2024": "O ano letivo irá terminar dia 13 de Dezembro",
    "quem é o diretor da escola": "O diretor da escola é o professor Fernando Luiz Ramos Brock",
    "qual o horário de funcionamento da escola": "A escola funciona das 07:30 ao 12:00, e das 18:50 a 23:15",
}

def normalizar_pergunta(pergunta):
    return re.sub(r'[^\w\s]', '', pergunta).lower()

def encontrar_resposta(pergunta_normalizada):
    perguntas_disponiveis = list(faq.keys())
    pergunta_mais_proxima = difflib.get_close_matches(pergunta_normalizada, perguntas_disponiveis, n=1)
    
    if pergunta_mais_proxima:
        return faq[pergunta_mais_proxima[0]]
    else:
        return "Desculpe, não entendi a pergunta. Tente perguntar de outra forma."

@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Recebe a pergunta do usuário via JSON
    data = request.get_json()
    pergunta = data.get("pergunta", "")
    
    pergunta_normalizada = normalizar_pergunta(pergunta)
    resposta = encontrar_resposta(pergunta_normalizada)
    
    # Retorna a resposta em formato JSON
    return jsonify({'resposta': resposta})

if __name__ == "__main__":
    app.run(debug=True)