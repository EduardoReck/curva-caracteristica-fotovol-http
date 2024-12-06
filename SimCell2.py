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
print("chegou em celula1")
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
            return False
    if response["status"]:
        print(f"Dados enviados para o TagoIO: {response['result']}")
    else:
        print(f"Erro ao enviar dados para o TagoIO: {response['message']}")

def celula_1(I_SC, Vdc, Vmp, TC):
    # Constantes e variáveis físicas
    q = 1.60217662 * 10**(-19)  # Carga elementar
    k = 1.38064852 * 10**(-23)  # Constante de Boltzmann
    n = 1.4                     # Fator de idealidade
    I_r = 800                   # Irradiância fixa
    T_0 = 298.15                # Temperatura de referência
    V_OC = 0.721                # Tensão de circuito aberto
    V_g = 1.79 * 10**(-19)      # Band gap
    temperatures = np.arange(298.15, 338.15 + 1, 10)  # Temperaturas de 298.15 K a 338.15 K
    V = np.linspace(0, Vmp / Vdc, 35)  # Intervalo de tensões

    # Preparação para armazenar resultados
    Iplot2 = np.zeros((len(temperatures), len(V)))
    Pplot2 = np.zeros((len(temperatures), len(V)))

    # Cálculo para cada temperatura
    for i, T in enumerate(temperatures):
        I_s0 = 1.2799 * 10**(-8)  # Corrente de saturação
        I_ph = ((I_SC / I_r) * I_r) * (1 + TC * (T - T_0))
        I_s = I_s0 * (T / T_0)**(3 / n) * np.exp((-(q * V_g) / (n * k)) * ((1 / T) - (1 / T_0)))
        I = I_ph - I_s * np.exp((q * V) / (n * k * T) - 1)
        P = I * V

        # Filtrando valores negativos
        I[I < 0] = np.nan
        P[P < 0] = np.nan

        Iplot2[i, :] = I
        Pplot2[i, :] = P

    # Gráfico corrente x tensão
    image_path_iv = "grafico_IV_temp.png"
    plt.figure()
    for i, T in enumerate(temperatures):
        plt.plot(V, Iplot2[i, :], label=f'T = {T:.2f} K')
    plt.xlabel('Tensão (V)')
    plt.ylabel('Corrente (I)')
    plt.title('Variação da Corrente com a Temperatura')
    plt.legend()
    plt.grid(True)
    plt.savefig(image_path_iv)
    plt.close()

    # Upload para Imgur
    url_iv = upload_to_imgur(image_path_iv)
    print(f"URL do gráfico I-V-temp: {url_iv}")

    # Enviar para o TagoIO
    send_data_to_tago("I_V_Temp", url_iv)

    # Gráfico potência x tensão
    image_path_pv = "grafico_PV_temp.png"
    plt.figure()
    for i, T in enumerate(temperatures):
        plt.plot(V, Pplot2[i, :], label=f'T = {T:.2f} K')
    plt.xlabel('Tensão (V)')
    plt.ylabel('Potência (P)')
    plt.title('Variação da Potência com a Temperatura')
    plt.legend()
    plt.grid(True)
    plt.savefig(image_path_pv)
    plt.close()

    # Upload para Imgur
    url_pv = upload_to_imgur(image_path_pv)
    print(f"URL do gráfico P-V-temp: {url_pv}")

    # Enviar para o TagoIO
    send_data_to_tago("P_V_Temp", url_pv)