# Dados simulados de entrada para testar a lógica (nos próximos blocos virão da API de clima)

temperatura_c = 32.5     # Temperatura atual em graus Celsius (Float)
vento_kmh = 42.0         # Velocidade do vento em KM/H (float)
chuva_mm = 12.0          # Volume de chuva em milimetro (float)
condicao_clima = "chuva" # Condição geral: "limpo", "nublado", "chuva", "granizo". "neve"

# Estrtutura para registrar os fenômenos detectados e o nível de severidade
alertas = []          # Lista que vai armazenar cada condição relevante encontrada
severidade = "NORMAL" # Estado inicial; só sobe quando houver condição de atenção ou severa

# 1. Fenomenos severos / desastres meteorologicos (granizo e neve)
if condicao_clima == "granizo":     # Verifica se há ocorrencia de granizo
    alertas.append("GRANIZO")       # Adiciona Granizo a lista de alertas
    severidade = "ALERTA SEVERO"    # Granizo sempre configura severidade máxima
    
if condicao_clima == "neve":          # Verifica se há ocorrencia de neve
    alertas.append("NEVE")            # Adiciona NEVE á lista de alertas
    if severidade != "ALERTA SEVERO": # Só altera se ainda não for ALERTA SEVERO
        severidade = "ALERTA SEVERO"  # Neve também configura severidade máxima
        
        
# 2. Faixas de temperatura (frio ou calor)
if temperatura_c <= 5.0:                                # Frio intenso (<= 5°C)
    alertas.append(f"FRIO INTENSO ({temperatura_c}°C)") # Registra temperatura com f-string
    if severidade != "ALERTA SEVERO":                   # Preserva ALERTA SEVERO caso já tenha ocorrido
        severidade = "ATENÇÃO"                          # Eleva para ATENÇÃO
        
elif temperatura_c <= 14.0:                     # Frio moderado (entre 5.1°C e 14°C)
    alertas.append(f"FRIO ({temperatura_c}°C)") # Registra condição de frio
    if severidade == "NORMAL":                  # Só sobe se ainda estiver NORMAL
        severidade = "ATENÇÃO"                  # Marca como ATENÇÃO
        
elif temperatura_c >= 36.0:                              # Calor extremo (>= 36°C)
    alertas.append(f"CALOR EXTREMO ({temperatura_c}°C)") # Registra calor extremo
    if severidade != "ALERTA SEVERO":                    # Preserva ALERTA SEVERO se houver
        severidade = "ATENÇÃO"                           # Marca como ATENÇÃO
        
elif temperatura_c >= 30.0:                      # Calor entre 30°C e 35.9°C
    alertas.append(f"CALOR ({temperatura_c}°C)") # Registra condição de calor
    if severidade == "NORMAL":                   # Só sobe se ainda estiver NORMAL
        severidade = "ATENÇÃO"                   # Marca como ATENÇÃO

# 3. Chuva e vento (avaliados em blocos separados para detectar combinações)
if chuva_mm >= 25.0:                              # Chuva forte / risco de alagamentos
    alertas.append(f"CHUVA FORTE ({chuva_mm}mm)") # Registra chuva forte
    severidade = "ALERTA SEVERO"                  # Chuva forte eleva para ALERTA SEVERO
    
elif chuva_mm > 0.0 or condicao_clima == "chuva": # Chuva leve/moderada ou estado chuvoso
    alertas.append(f"CHUVA ({chuva_mm}mm)")       # Registra chuva atual
    if severidade == "NORMAL":                    # Só sobe se ainda estiver NORMAL
        severidade = "ATENÇÃO"                    # Marca como ATENÇÃO
        
if vento_kmh >= 60.0:                                # Rajadas fortes / vendaval
    alertas.append(f"VENTO FORTE ({vento_kmh}km/h)") # Registra vento forte
    severidade = "ALERTA SEVERO"                     # Vento forte eleva para ALERTA SEVERO
    
elif vento_kmh >= 35.0:                        # Vento moderado a forte 
    alertas.append(f"VENTO ({vento_kmh}km/h)") # Registra vento moderado/forte
    if severidade == "NORMAL":                 # Só sobe se ainda estiver NORMAL
        severidade = "ATENÇÃO"                 # Marca com ATENÇÃO
        

# 4. Montagem final de mensagem prática para celular  e smartwatch Haylon S6
if len(alertas) > 0:                    # Se existe pelo menos um item na lista de alertas
    resumo_eventos = ", ".join(alertas) # Une os alertas em uma única string separada por virgula
    mensagem = (                        # Monta uma mensagem curta e fácil de ler no relógio
        f"[{severidade}] {resumo_eventos} | "
        f"T: {temperatura_c}°C V:{vento_kmh}km/h C:{chuva_mm}mm"
    )
else:            # Se a lista de alertas estiver vazia 
    mensagem = ( # Monta um aviso curto de condição normal
        f"[NORMAL] Clima estável | "
        f"T:{temperatura_c}°C V:{vento_kmh}km/h C:{chuva_mm}mm"
    )
    
print(mensagem) # Mostra o resultado final no terminal