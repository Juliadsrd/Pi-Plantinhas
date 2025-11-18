from flask import Flask, request, jsonify, render_template
from datetime import datetime

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Variável global para armazenar os últimos dados do sensor
sensor_data = {
    "umidade_solo": "N/A",
    "timestamp": "Nenhum dado recebido ainda"
}

# --- Endpoint para receber dados da ESP32 (POST) ---
@app.route('/dados', methods=['POST'])
def receber_dados():
    global sensor_data
    
    # 1. Verifica se o corpo da requisição é JSON
    if not request.is_json:
        return jsonify({"status": "erro", "mensagem": "O formato deve ser JSON"}), 400

    # 2. Obtém os dados JSON
    dados_recebidos = request.get_json()

    # 3. Processa e armazena os dados
    if 'umidade' in dados_recebidos:
        umidade = dados_recebidos['umidade']
        sensor_data['umidade_solo'] = f"{umidade}%"
        sensor_data['timestamp'] = datetime.now().strftime("%H:%M:%S em %d/%m/%Y")
        
        print(f"Dados Recebidos: Umidade = {umidade}%")
        return jsonify({"status": "ok", "mensagem": "Dados recebidos com sucesso!"}), 200
    else:
        return jsonify({"status": "erro", "mensagem": "Campo 'umidade' faltando no corpo da requisição"}), 400

# --- Endpoint para fornecer os dados mais recentes (GET) ---
@app.route('/latest', methods=['GET'])
def latest():
    return jsonify(sensor_data)

# --- Página inicial para visualização (GET) ---
@app.route('/')
def dashboard():
    return render_template('dashboard.html', data=sensor_data)

# --- Execução do servidor ---
if __name__ == '__main__':
    # Executa o servidor. host='0.0.0.0' para ser acessível na rede
    app.run(host='0.0.0.0', port=5000, debug=True)
