import json # Módulo padrão para ler e gravar dados estruturados em formato JSON
import os   # Módulo padrão para verificar se o arquivo de estado já existe

ARQUIVO_ESTADO = "estado_bot.json" # Nome do arquivo local que guarda estados e coordenadas

ESTADO_PADRAO = {           # Valores iniciais caso o arquivo não exista
    "alertas_ativos": True, # Alertas começam ativos por padrão
    "latitude": -23.6677,   # Latitude padrão de referência
    "longitude": -46.5618   # Longitude pdrão de referência
}

def carregar_estado():                     # Lê o estado atual salvo ou devolve o padrão com segurança
    if not os.path.exists(ARQUIVO_ESTADO): # Se o arquivo ainda não foi criado
        return ESTADO_PADRAO.copy()        # Retorna uma cópia do dicionário padrão
    
    try:                                                             # Protege contra arquivo corrompido ou JSON inválido
        with open(ARQUIVO_ESTADO, "r", encoding="utf-8") as arquivo: # Abre o JSON para leitura em UTF-8
            dados = json.load(arquivo)                               # Converte o conteúdo JSON em dicionário Python
        estado = ESTADO_PADRAO.copy()                                # Começa com os padrões para garantir todas as chaves
        estado.update(dados)                                         # Sobrescreve com os valores salvos no arquivo
        return estado                                                # Retorna o estado completo e atualizado
    except (OSError, json.JSONDecodeError):                          # Trata erro de leitura ou formato inválido
        return ESTADO_PADRAO.copy()                                  # Em caso de falha, volta ao estado padrão sem quebrar o bot
    
def salvar_estado(estado):                                       # Persiste o dicionário de estado no arquivo JSON
    with open(ARQUIVO_ESTADO, "w", encoding="utf-8") as arquivo: # Abre o arquivo para escrever em UTF-8
        json.dump(estado, arquivo, indent=2, ensure_ascii=False) # Salva JSON formatado e legível