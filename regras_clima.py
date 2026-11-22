def avaliar_clima(temperatura_c, vento_kmh, chuva_mm, condicao_clima):  # Recebe os dados do clima
    alertas = []                                                        # Lista que vai armazenar os fenômenos detectados
    severidade = "NORMAL"                                               # Estado inicial de severidade

    # 1. Fenômenos severos / desastres meteorológicos (granizo e neve)
    if condicao_clima == "granizo":   # Verifica ocorrência de granizo
        alertas.append("GRANIZO")     # Registra granizo
        severidade = "ALERTA SEVERO"  # Severidade máxima

    if condicao_clima == "neve":           # Verifica ocorrência de neve
        alertas.append("NEVE")             # Registra neve
        if severidade != "ALERTA SEVERO":  # Evita sobrescrever se já for ALERTA SEVERO
            severidade = "ALERTA SEVERO"   # Severidade máxima

    # 2. Faixas de temperatura (frio ou calor)
    if temperatura_c <= 5.0:                                 # Frio intenso (<= 5°C)
        alertas.append(f"FRIO INTENSO ({temperatura_c}°C)")  # Adiciona detalhe da temperatura
        if severidade != "ALERTA SEVERO":                    # Mantém ALERTA SEVERO caso já exista
            severidade = "ATENCAO"                           # Marca como ATENCAO
    elif temperatura_c <= 14.0:                      # Frio moderado (entre 5.1°C e 14°C)
        alertas.append(f"FRIO ({temperatura_c}°C)")  # Registra frio
        if severidade == "NORMAL":                   # Só altera se estiver NORMAL
            severidade = "ATENCAO"                   # Marca como ATENCAO
    elif temperatura_c >= 36.0:                               # Calor extremo (>= 36°C)
        alertas.append(f"CALOR EXTREMO ({temperatura_c}°C)")  # Registra calor extremo
        if severidade != "ALERTA SEVERO":                     # Mantém ALERTA SEVERO caso já exista
            severidade = "ATENCAO"                            # Marca como ATENCAO
    elif temperatura_c >= 30.0:                       # Calor (entre 30°C e 35.9°C)
        alertas.append(f"CALOR ({temperatura_c}°C)")  # Registra calor
        if severidade == "NORMAL":                    # Só altera se estiver NORMAL
            severidade = "ATENCAO"                    # Marca como ATENCAO

    # 3. Chuva e vento (avaliados em blocos separados para detectar combinações)
    if chuva_mm >= 25.0:                               # Chuva forte / risco de alagamento
        alertas.append(f"CHUVA FORTE ({chuva_mm}mm)")  # Registra chuva forte
        severidade = "ALERTA SEVERO"                   # Eleva para ALERTA SEVERO
    elif chuva_mm > 0.0 or condicao_clima == "chuva":  # Chuva leve/moderada ou condição chuvosa
        alertas.append(f"CHUVA ({chuva_mm}mm)")        # Registra chuva
        if severidade == "NORMAL":                     # Só altera se estiver NORMAL
            severidade = "ATENCAO"                     # Marca como ATENCAO

    if vento_kmh >= 60.0:                                 # Rajadas fortes / vendaval
        alertas.append(f"VENTO FORTE ({vento_kmh}km/h)")  # Registra vento forte
        severidade = "ALERTA SEVERO"                      # Eleva para ALERTA SEVERO
    elif vento_kmh >= 35.0:                               # Vento moderado a forte
        alertas.append(f"VENTO ({vento_kmh}km/h)")        # Registra vento moderado/forte
        if severidade == "NORMAL":                        # Só altera se estiver NORMAL
            severidade = "ATENCAO"                        # Marca como ATENCAO

    # 4. Montagem da mensagem prática para celular e smartwatch Haylou S6
    if len(alertas) > 0:                     # Se há algum alerta na lista
        resumo_eventos = ", ".join(alertas)  # Junta os alertas em um único texto
        mensagem = (                         # Formata string curta e direta
            f"[{severidade}] {resumo_eventos} | "
            f"T:{temperatura_c}°C V:{vento_kmh}km/h C:{chuva_mm}mm"
        )
    else:             # Se não há alertas relevantes
        mensagem = (  # Formata mensagem de clima estável
            f"[NORMAL] Clima estável | "
            f"T:{temperatura_c}°C V:{vento_kmh}km/h C:{chuva_mm}mm"
        )

    return {                       # Devolve um dicionário com o resultado da avaliação
        "severidade": severidade,  # Nível calculado
        "alertas": alertas,        # Lista de fenômenos encontrados
        "mensagem": mensagem,      # Texto final pronto para notificação
    }


if __name__ == "__main__":                            # Só executa este teste se rodar regras_clima.py diretamente
    teste = avaliar_clima(32.5, 42.0, 12.0, "chuva")  # Chama a função com valores de teste
    print(teste["mensagem"])                          # Exibe a mensagem formatada