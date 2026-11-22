import requests # Biblioteca externa para fazer requisições HTTP para API de clima 

def traduzir_condicao_wmo(codigo_clima):         # Recebe o código meteorológico padrão WMO da Open-Meteo
    if codigo_clima in (71, 73, 75, 77, 85, 86): # Codigos associados a queda de neve ou grãos de neve
        return "neve"                            # Padroniza como neve para o bloco 01

    elif codigo_clima in (96, 99): # Códigos associados com granizo
        return "granizo"           # Padroniza como "granizo" para o bloco 01
    
    elif codigo_clima in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82, 95): # Chuvas e pancadas
        return "chuva"                                                             # Padroniza como "chuva" para o bloco 01
    
    elif codigo_clima in (1, 2, 3, 45, 48): # Parcialmente nublado, encoberto ou neblina
        return "nublado"                    # Padroniza como "nublado" para o bloco 01
    else:                                   # Céu limpo (codigo 0) ou outros códigos não listados
        return "limpo"                      # Padrniza como "limpo" para o bloco 01
    
    
def buscar_clima_por_coordenadas(latitude, longitude):                           # Recebe coordenadas geográficas (float)
    url = "https://api.open-meteo.com/v1/forecast"                               # Endpoint público gratuito da Open-Meteo
    parametros = {                                                               # Dicionário com os parâmetros enviados na consulta HTTP
        "latitude": latitude,                                                    # Latitude do local a ser monitorado
        "longitude": longitude,                                                  # Longitude do local a ser monitorado
        "current": ["temperature_2m", "rain", "wind_speed_10m", "weather_code"], # Variáveis atuais desejadas
        "timezone": "auto",                                                      # Ajusta automaticamente o fuso horário conforme as coordenadas
        
    }
    
    try:                                                            # Bloco de proteção caso ocorra uma falha na rede, timeout ou resposta inválida
        resposta = requests.get(url, params=parametros, timeout=10) # Faz requisição GET com limite de 10 segundos
        resposta.raise_for_status()                                 # Lança exceção se o servidor retornar erro HTTP(ex: 400 ou 500)
        dados = resposta.json()                                     # Converte o corpo da resposta JSON em dicionário Python
    except requests.RequestException as erro:                       # Captura qualquer erro de requisição HTTP/rede
        print(f"Erro ao consultar API de clima: {erro}")            # Exibe mensagem de erro diagnóstica
        return None                                                 # Retorna None para o chamador saber que a consulta falhou
    
    atual = dados.get("current", {}) # Extrai com segurança o bloco "current" do JSON retornado
    
    temperatura_c = float(atual.get("temperature_2m", 0.0)) # Temperatura atual em °C
    vento_kmh = float(atual.get("wind_speed_10m", 0.0)) # Velocidade do vento a 10m em km/h
    chuva_mm = float(atual.get("rain", 0.0)) # Precipitação de chuva atual em mm
    codigo_wmo = int(atual.get("weather_code", 0)) # Código numérico de condição climática
    condicao_clima = traduzir_condicao_wmo(codigo_wmo) # Converte o código para o formato
    
    return{                                         # Retorna um dicionario organizado com os dados prontos para o Bloco 01
        "temperatura_c": temperatura_c,             # Temperatura em graus Celsius
        "vento_kmh": vento_kmh,                     # Velocidade do vento km/h
        "chuva_mm": chuva_mm,                       # Volume de chuva em mm
        "condicao_clima": condicao_clima,           # Condição padronizada ("limpo", "nublado", "chuva", etc.)
        "local_fuso": dados.get("timezone", "UTC"), # Fuso horário identificado pela API
    }
    
    
if __name__ == "__main__": # Executa este teste apenas quando rodar clima_api.py diretamente
    # Exemplo de coordenadas de São Bernardo do Campo, SP (Caso preferir: troque por qualquer outra)
    lat_teste = -23.6677   # Latitude de teste
    lon_teste = -46.5618   # Longitude de teste
    
    resultado = buscar_clima_por_coordenadas(lat_teste, lon_teste) # Chama a função de consulta
    print(resultado) # Exibe o dicionário retornado no terminal