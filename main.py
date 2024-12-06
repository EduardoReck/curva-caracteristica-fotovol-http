from flask import Flask, request, jsonify
from tagoio_sdk import Device
from recebe_messege import receive_message
from pyngrok import ngrok
import logging

# Configuração do dispositivo TagoIO
TOKEN = "Seu token tago aqui"
myDevice = Device({"token": TOKEN})
ngrok.set_auth_token("SEU_AUTHTOKEN_AQUI")
# Inicializando o Flask
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Função auxiliar para exibir os valores das entradas
def print_entradas(entrada1, entrada2, entrada3, entrada4):
    print("\n=== Valores das Entradas ===")
    print(f"Entrada 1 (icc): {entrada1}")
    print(f"Entrada 2 (vmp): {entrada2}")
    print(f"Entrada 3 (vca): {entrada3}")
    print(f"Entrada 4 (temperature): {entrada4}")
    print("=============================\n")

@app.route('/process', methods=['POST'])
def process_data():
    """
    Endpoint para processar os dados recebidos via POST HTTP.
    """
    try:
        # Recebe os dados do POST
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400

        # Passa os dados para a função receive_message
        entrada1, entrada2, entrada3, entrada4 = receive_message(data)

        # Exibe os valores processados
        print_entradas(entrada1, entrada2, entrada3, entrada4)

        # Retorna sucesso
        return jsonify({
            "status": "success",
            "message": "Data processed successfully",
            "entrada1": entrada1,
            "entrada2": entrada2,
            "entrada3": entrada3,
            "entrada4": entrada4
        }), 200
    except Exception as e:
        # Em caso de erro, retorna mensagem de erro
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Cria o túnel ngrok para a porta 5000
    public_url = ngrok.connect(5000)
    print(f"Seu servidor está disponível publicamente em: {public_url}")
    
    # Inicia o Flask
    app.run(host='0.0.0.0', port=5000)
