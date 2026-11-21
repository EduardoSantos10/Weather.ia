# Dados simulados de entrada para testar a lógica (nos próximos blocos virão da API de clima)

temperatura_c = 32.5 # Temperatura atual em graus Celsius (Float)
vento_kmh = 42.0 # Velocidade do vento em KM/H (float)
chuva_mm = 12.0 # Volume de chuva em milimetro (float)
condicao_clima = "chuva" # Condição geral: "limpo", "nublado", "chuva", "granizo". "neve"

# Estrtutura para registrar os fenômenos detectados e o nível de severidade
alertas = [] # Lista que vai armazenar cada condição relevante encontrada
severidade = "NORMAL" # Estado inicial; só sobe quando houver condição de atenção ou severa

