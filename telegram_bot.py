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
    token = os.getenv("TELEGRAM_BOT_TOKEN")                         # Busca o token do Bot nas variáveis de ambiente (nunca fixo no código)
    chat_id_autorizado = os.getenv("TELEGRAM_CHAT_ID")              # Busca o chat_id permitido para receber os alertas
    
    if not token or not chat_id_autorizado:                                    # Verifica se algumas das credênciais está ausente ou vazia
        print("Erro: TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID não configurador") # Informa o problema do console
        return False                                                           # Interrompe o envio e retorna False indicando falha
    
    destino = str(chat_id_destino) if chat_id_destino else str(chat_id_autorizado) # Define o alvo convertendo para texto
    if destino != str(chat_id_autorizado):                                         # Compara o destino solicitado com o chat_id autorizado
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
    
if __name__ == "__main__":                                                                   # Garante que o código abaixo só rode ao executar telegram_bot.py diretamente
    enviado = enviar_mensagem_telegram("Teste Weather.ia: conexão com Telegram funcionando") # Dispara mensagem de teste
    print("Enviado com sucesso!" if enviado else "Falha no envio")                           # Imprime resultado final no terminal