from clima_api import buscar_clima_por_coordenadas                              # Importa a função do bloco 02 (coleta na API)
from estado_bot import carregar_estado                                          # Lê o estado atual salvo (alertas_ativos, lat, lon)
from regras_clima import avaliar_clima                                          # Importa a funçao do bloco 01 (regras de severidade)
from telegram_bot import enviar_mensagem_telegram, processar_comandos_telegram  # Importa a função do bloco 03 (envio do Telegram)

def executar_verificacao_clima(latitude, longitude, forcar_envio=False): # Executa floxo completo para lat/lon
    estado = carregar_estado()                                           # Lê o estado mais recente
    
    if not estado.get("alertas_ativos", True) and not forcar_envio:             # Respeita /desativar nas checagens normais
        print("Alertas pausados via /desativar. Nenhuma notificação enviada.")  # Informa no console
        return None                                                             # Encerra sem notificar
    
    clima_atual = buscar_clima_por_coordenadas(latitude, longitude) # Buscar dados reais na API
    
    if clima_atual is None:                                      # Verifica se houve falha na consulta a API
        print("Não possível obter os dados no clima no momento") # Avisa sobre a falha
        return None                                              # Encerra execução com retorno vazio
    
    resultado = avaliar_clima(                        # Aplica regras de severidade e formata a mensagem
        temperatura_c=clima_atual["temperatura_c"],   # Passa a temperatura em °C
        vento_kmh=clima_atual["vento_kmh"],           # Passao vento em km/h
        chuva_mm=clima_atual["chuva_mm"],             # Passa a chuva em mm
        condicao_clima=clima_atual["condicao_clima"], # Passa condiçao padronizada
    )
    
    print(resultado["mensagem"])                                                 # Mostra resumo no terminal
    enviado = enviar_mensagem_telegram(resultado["mensagem"])                    # Envia para Telegram e relógio
    print("Notificação enviada!" if enviado else "Falha ao enviar notificação.") # Status no console
    return resultado                                                             # Devolve avaliação

def checar_nova_localizacao(lat, lon):                      # Callback aciona quando você envia localização GPS no Telegram
    executar_verificacao_clima(lat, lon, forcar_envio=True) # Verifica e envia o clima no novo ponto GPS



if __name__ == "__main__":                                                                  # Executa quando rodarmos main.py diretamente
    estado_atual = processar_comandos_telegram(on_nova_localizacao=checar_nova_localizacao) # Lê comandos e GPS
    executar_verificacao_clima(                                                             # Executa checagem para localização configurada
        latitude=estado_atual["latitude"],                                                  # Latitude salva nos estado
        longitude=estado_atual["longitude"]                                                 # Longitude salva nos estado
    )