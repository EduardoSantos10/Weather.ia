from clima_api import buscar_clima_por_coordenadas # Importa a função do bloco 02 (coleta na API)
from regras_clima import avaliar_clima             # Importa a funçao do bloco 01 (regras de severidade)
from telegram_bot import enviar_mensagem_telegram  # Importa a função do bloco 03 (envio do Telegram)

def executar_verificacao_clima(latitude, longitude): # Recebe coordenadas para checar o clima
    clima_atual = buscar_clima_por_coordenadas(latitude, longitude)       # Buscar dados reais na API
    
    if clima_atual is None:                                      # Verifica se houve falha na consulta a API
        print("Não possível obter os dados no clima no momento") # Avisa sobre a falha
        return None                                              # Encerra execução com retorno vazio
    
    return avaliar_clima(                             # Envia os dados reais para as regras do bloco 01
        temperatura_c=clima_atual["temperatura_c"],   # Passa a temperatura em °C
        vento_kmh=clima_atual["vento_kmh"],           # Passao vento em km/h
        chuva_mm=clima_atual["chuva_mm"],             # Passa a chuva em mm
        condicao_clima=clima_atual["condicao_clima"], # Passa condiçao padronizada
    )



if __name__ == "__main__": # Executa quando rodarmos main.py diretamente
    lat_teste = -23.6677   # Latitude de teste
    lon_teste = -46.5618   # Longitude de teste
    
    resultado = executar_verificacao_clima(lat_teste, lon_teste) # Roda a integração Bloco 02 -> Bloco 01
    
    if resultado is not None:                                                        # Confirma que a avaliação foi concluida com sucesso
        print(resultado["mensagem"])                                                 # Exibe o resumo no terminal para acompanhamento local
        enviado = enviar_mensagem_telegram(resultado["mensagem"])                    # Dispara o alerta para o Telegram
        print("Notificação enviada!" if enviado else "Falha ao enviar notificações") # Confirma status do envio