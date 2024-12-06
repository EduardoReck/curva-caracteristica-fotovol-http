import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pyimgur
from tagoio_sdk import Device
import json

# Configuração do Imgur
CLIENT_ID = "seu id imgur"  # Substitua pelo seu Client ID do Imgur

# Configuração do TagoIO
TAGO_DEVICE_TOKEN = "Seu token tago aqui"  # Substitua pelo token do dispositivo TagoIO
myDevice = Device({"token": TAGO_DEVICE_TOKEN})
print("chegou em celula")
def upload_to_imgur(image_path):
    """Faz upload da imagem para o Imgur e retorna a URL pública."""
    try:
        im = pyimgur.Imgur(CLIENT_ID)
        uploaded_image = im.upload_image(image_path, title="Gráfico de Simulação")
        return uploaded_image.link
    except Exception as e:
        print(f"Erro ao fazer upload da imagem para o Imgur: {e}")
        return None

def send_data_to_tago(variable, value):
    """Envia os dados para o TagoIO usando a função sendData."""
    payload = {
        "variable": variable,
        "value": value
    }
    response = myDevice.sendData([payload])
    if isinstance(response, str):
        try:
            response = json.loads(response)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            return False  # Retorne algo para indicar falha
    if response["status"]:
        print(f"Dados enviados para o TagoIO: {response['result']}")
    else:
        print(f"Erro ao enviar dados para o TagoIO: {response['message']}")

def celula(I_SC, Vdc, Vmp, TC):
    # Variáveis físicas e condições de entrada
    q = 1.60217662 * 10**(-19)  # Carga elementar (C)
    k = 1.38064852 * 10**(-23)  # Constante de Boltzmann (J/K)
    n = 1.4                     # Fator de idealidade

    T = 298.15                   # Temperatura da célula (KELVIN)
    I_r = np.arange(200, 1001, 200)  # Irradiância (de 200 a 1000)

    V = np.linspace(0, Vmp / Vdc, 35)  # Tensão de entrada

    T_0 = 298.15                 # Temperatura de referência (25°C)
    I_r0 = 1000                  # Irradiância de referência
    V_OC = 0.721                 # Tensão de circuito aberto (V)

    V_g = 1.79 * 10**(-19)       # Band gap (Joules)
    
    V_m, I_rm = np.meshgrid(V, I_r)
    I_s0 = 1.2799 * 10**(-8)     # Corrente de saturação na temperatura de referência
    I_ph = ((I_SC / I_r0) * I_rm) * (1 + TC * (T - T_0))
    I_s = I_s0 * (T / T_0)**(3 / n) * np.exp((-(q * V_g) / (n * k)) * ((1 / T) - (1 / T_0)))
    I = I_ph - I_s * np.exp((q * V_m) / (n * k * T) - 1)
    P = I * V

    # Filtrando os valores negativos
    Iplot = np.where(I < 0, np.nan, I)
    Pplot = np.where(P < 0, np.nan, P)
    
    # Gerar gráfico de corrente x tensão
    image_path_iv = "grafico_IV.png"
    plt.figure()
    for i in range(len(I_r)):
        plt.plot(V, Iplot[i, :], label=f'Irradiância = {I_r[i]} W/m²')
    plt.xlabel('Tensão (V)')
    plt.ylabel('Corrente (I)')
    plt.legend()
    plt.grid(True)
    plt.savefig(image_path_iv)
    plt.close()

    # Upload para Imgur
    url_iv = upload_to_imgur(image_path_iv)
    print(f"URL do gráfico I-V: {url_iv}")

    # Enviar para o TagoIO
    send_data_to_tago("I_V", url_iv)

    # Gerar gráfico de potência x tensão
    image_path_pv = "grafico_PV.png"
    plt.figure()
    for i in range(len(I_r)):
        plt.plot(V, Pplot[i, :], label=f'Irradiância = {I_r[i]} W/m²')
    plt.xlabel('Tensão (V)')
    plt.ylabel('Potência (P)')
    plt.legend()
    plt.grid(True)
    plt.savefig(image_path_pv)
    plt.close()

    # Upload para Imgur
    url_pv = upload_to_imgur(image_path_pv)
    print(f"URL do gráfico P-V: {url_pv}")

    # Enviar para o TagoIO
    send_data_to_tago("P_V", url_pv)
