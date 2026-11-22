import os                      # Importa o módulo padrão do Python para ler variáveis de ambiente do sistema operacional
import requests                # Importa a biblioteca requests para fazer requisições HTTP á API do Telegram
from dotenv import load_dotenv # Importa a função load_dotenv para carregar váriaveis de arquivo .env
from estado_bot import carregar_estado, salvar_estado # Gerencia estado de alertas e coordenadas

load_dotenv() # Ler o arquivo .env (se existir na pasta) e injeta as váriaveis no ambiente atual

def _obter_credenciais():                                                      # Função auxiliar interna para validar token e chat_id autorizado
    token = os.getenv("TELEGRAM_BOT_TOKEN")                                    # Token do bot gerado no @BotFather
    chat_id_aurotizado = os.getenv("TELEGRAM_CHAT_ID")                         # Chat ID permitido para usar o sistema
    if not token or not chat_id_aurotizado:                                    # Garante que ambas as variáveis existem
        print("Erro: TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID não configurados") # Aviso no terminal
        return None, None                                                      # Retorna vazio se faltar credencial
    return token, str(chat_id_aurotizado)                                      # Retorna token e chat_id como string


def enviar_mensagem_telegram(texto_mensagem, chat_id_destino=None): # Define função que envia mensagens no Telegram
    token, chat_id_autorizado = _obter_credenciais() # Busca e valida credênciais
    if not token or not chat_id_autorizado: # Se não houver credênciais válidas
        return False # Cancela o envio
    
    destino = str(chat_id_destino) if chat_id_destino else chat_id_autorizado      # Define o chat ed destino
    if destino != chat_id_autorizado:                                              # Bloqueia o envio para qualquer chat diferente do autorizado
        print("Bloqueado: tentativa de envio para chat_id não autorizado")         # Bloqueia envio para chats desconhecidos
        return False                                                               # Retorna False sem disparar a requisição HTTP
    
    url = f"https://api.telegram.org/bot{token}/sendMessage" # Monta o EndPoint Oficial do Telegram com o o Token do Bot
    payload = { # Cria o corpo JSON que será enviado na requisição POST
        "chat_id": destino, # ID do chat que vai receber a notificação
        "text": texto_mensagem, # Conteúdo textual da mensagem (curto para celular e Haylou S6)
    }
    
    try: # Inicia bloco para lidar com possíveis falhas de rede ou API
        resposta = requests.post(url, json=payload, timeout=10)   # Envia requisição POST com limite de 10 segundos
        resposta.raise_for_status()                               # Gera requisiçção automaticamente se o Telegram responder com erro HTTP (4xx/5xx)
        return True                                               # Retorna True confirmando que o envio foi aceito pela API
    except requests.RequestException as erro:                     # Captura erros de conexão, timeout ou status HTTP inválido
        print(f"Erro ao enviar mensagem para o Telegram: {erro}") # Exibe o erro para diagnóstico
        return False                                              # Retorna False indicando que o envio não ocorreu
    

def processar_comandos_telegram(on_nova_localizacao=None): # Lê novas interações a atualiza o estado
    token, chat_id_autorizado = _obter_credenciais()       # Obtém credênciais válidas
    if not token or not chat_id_autorizado:                # Se faltarem credênciais
        return carregar_estado()                           # Retorna estado atual sem carregar nada
    
    estado = carregar_estado()                        # Carrega estado salvo (alertas ativos, latitude, longitude)
    ultimo_update_id = estado.get("ultimo_update_id") # Pega último update processado se existir
    
    url = f"https://api.telegram.org/bot{token}/getUpdates" # EndPoint para buscar eventos/mensagens novos
    parametros = {"timeout": 5}                             # Aguarda até 5s por uma resposta limpa da API
    
    if ultimo_update_id is not None:                # Se já processamos updates antes
        parametros["offset"] = ultimo_update_id + 1 # Pede apenas atualizações ainda não confirmadas
        
    try:                                                            # Protege a chamada HTTP de leitura
        resposta = requests.get(url, params=parametros, timeout=15) # Consulta getUPdate
        resposta.raise_for_status()                                 # Verifica erro HTTP
        dados = resposta.json()                                     # Converte resposta em dicionário Python
    except requests.RequestException as erro:                       # Trata erro de rede/API
        print(f"Erro ao ler comandos do Telegram: {erro}")          # Exibe diagnóstico
        return estado                                               # Retorna estado sem alterações
    
    atualizacoes = dados.get("result", []) # Lista de eventos reecebidos no Telegram
    maior_update_id = ultimo_update_id     # Controla o maior update_id visto nessa execução
    
    for item in atualizacoes:             # Percorre cada atualização recebida
        update_id = item.get("update_id") # Identificador único da atualização no Telegram
        if update_id is not None:         # Se houver update_id
            maior_update_id = update_id if maior_update_id is None else max(maior_update_id, update_id) # Atualiza máximo
            
        mensagem = item.get("message")or item.get("edited_message") # Extrai objeto de mensagem
        if not mensagem:                                            # Ignora atualizações que não sejam mensagem
            continue                                                # Vai para o próximo item
        
        chat_id = str(mensagem.get("chat", {}).get("id", "")) # Extrai chat_id de quem enviou
        if chat_id != chat_id_autorizado:                     # Segurança: ignora qualquer mensagem de outro chat_id
            continue                                          # Não processa comandos ou localizações de terçeiros
        
        # 1. Verifica se o usuário enviou uma localização GPS (pin de localização no Telegram)
        if "location" in mensagem:                         # Se a mensagem contém dados de GPS
            lat = float(mensagem["location"]["latitude"])  # Latitude enviada pelo GPS
            lon = float(mensagem["location"]["longitude"]) # Lnogitude enviada pelo GPS
            estado["latitude"] = lat                       # Salva nova latitude no estado
            estado["longitude"] = lon                      # Salva nova longitude no estado
            salvar_estado(estado)                          # Persiste no JSON imediatamente
            enviar_mensagem_telegram(                      # Confirma atualização no Telegram (e no relógio)
                f"GPS atualizado: lat {lat:.4f}, lon {lon:4.f}. Checando clima..."
            )
            if callable(on_nova_localizacao): # Se o main.py passou o callback para checar o clima na hora
                on_nova_localizacao(lat, lon) # Dispara verificação imediata nas novas coordenadas
            continue                          # Passa para a próxima atualização
        
        # 2. Verifica comandos de texto (/ativar e /desativar)
        texto = (mensagem.get("text") or "").strip().lower() # Normaliza texto em minusculo sem espaços extras
        if texto.startswith("/ativar"):                      # Comando para ativar alertas
            estado["alertas_ativos"] = True                  # Liga o envio automático de alertas
            salvar_estado(estado)                            # Salva no JSON
            enviar_mensagem_telegram("Weather.ia ATIVADO: alertas automaticos ligados.") # Confirma ao usuário
            
        elif texto.startswith("/desativar"): # Comando para desativar alertas
            estado["alertas_ativos"] = False # Pausa o envio automatico de alertas
            salvar_estado(estado)            # Salva no JSON
            enviar_mensagem_telegram("Weather.ia DESATIVADO: alertas automáticos pausados.") # Confirma ao usuário
            
    if maior_update_id is not None:                  # Se processarmos ao menos um update
        estado["ultimo_update_id"] = maior_update_id # Guarda para não reprocessar o mesmo comando depois
        salvar_estado(estado)                        # Salva o no offset no JSON
        
    return estado # Devolve o estado atualizado ao chamador