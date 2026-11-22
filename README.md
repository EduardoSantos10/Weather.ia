# 🌦️ Weather.ia

Sistema automatizado e modular desenvolvido em **Python** para monitoramento meteorológico em tempo real, envio de alertas inteligentes via **Telegram** (com espelhamento de notificações no smartwatch **Haylou S6**) e execução agendada na nuvem via **GitHub Actions**.

---

## 📋 Índice

- [Visão Geral e Arquitetura](#-visão-geral-e-arquitetura)
- [Estrutura de Arquivos e Funções](#-estrutura-de-arquivos-e-funções)
- [Conceitos e Termos Técnicos Aplicados](#-conceitos-e-termos-técnicos-aplicados)
- [Comandos e Interatividade no Telegram](#-comandos-e-interatividade-no-telegram)
- [Configuração Local e na Nuvem (Segurança)](#-configuração-local-e-na-nuvem-segurança)
- [Automação com GitHub Actions e Ajustes Realizados](#-automação-com-github-actions-e-ajustes-realizados)
- [Roadmap (Próximas Evoluções)](#-roadmap-próximas-evoluções)

---

## 🏗️ Visão Geral e Arquitetura

O **Weather.ia** segue o princípio de **separação de responsabilidades**, dividindo a coleta de dados, as regras de negócio, a persistência de estado e a comunicação externa em módulos independentes:

```text
Weather.ia/
├── .github/
│   └── workflows/
│       └── weather_ia.yml   # Pipeline de automação agendada (CI/CD)
├── main.py                  # Orquestrador principal do fluxo
├── clima_api.py             # Integração com a API Open-Meteo
├── regras_clima.py          # Motor determinístico de análise e classificação
├── telegram_bot.py          # Comunicação bidirecional com a API do Telegram
├── estado_bot.py            # Leitura e gravação de estado local (JSON)
├── requirements.txt         # Dependências do projeto (requests, python-dotenv)
├── .gitignore               # Bloqueio de arquivos sensíveis (.env e estado_bot.json)
└── README.md                # Documentação do projeto
```

---

## 🧩 Estrutura de Arquivos e Funções

### 1. `main.py` — Orquestração
Coordena o ciclo de execução completo da aplicação:
* Carrega as variáveis de ambiente (`load_dotenv()`).
* Recupera o estado atual (`carregar_estado()`).
* Verifica novas mensagens e comandos enviados pelo usuário autorizado no Telegram (`processar_comandos_telegram()`).
* Caso os alertas estejam ativos (ou uma nova localização GPS tenha sido enviada), consulta o clima atual (`obter_clima_atual()`), avalia a severidade (`avaliar_clima()`) e dispara o alerta (`enviar_mensagem_telegram()`).
* Persiste as atualizações no estado (`salvar_estado()`).

### 2. `clima_api.py` — Coleta de Dados Meteorológicos
Consome a API pública **Open-Meteo** sem necessidade de chave de API:
* **`obter_clima_atual(latitude, longitude)`**: realiza requisição HTTP `GET` passando coordenadas geográficas e parâmetros de clima atual (`temperature_2m`, `wind_speed_10m`, `precipitation`, `weather_code`), retornando um dicionário padronizado com os indicadores meteorológicos.

### 3. `regras_clima.py` — Regras de Negócio e Severidade
Motor determinístico que transforma números brutos em alertas objetivos e curtos (otimizados para leitura rápida no celular e na tela do smartwatch):
* **`avaliar_clima(dados_clima)`**: aplica faixas de decisão para temperatura extrema, rajadas de vento e volume de precipitação, retornando o nível de atenção e a mensagem formatada.

### 4. `telegram_bot.py` — Interface Bidirecional
Comunica-se diretamente com a **Telegram Bot API** via requisições HTTPS:
* **`enviar_mensagem_telegram(mensagem)`**: envia notificações de texto para o `TELEGRAM_CHAT_ID` configurado utilizando o endpoint `/sendMessage`.
* **`processar_comandos_telegram(estado)`**: consulta atualizações recentes no endpoint `/getUpdates`, filtra estritamente mensagens vindas do `TELEGRAM_CHAT_ID` autorizado (bloqueando terceiros) e interpreta comandos textuais (`/ativar`, `/desativar`) ou compartilhamento de localização (`location`).

### 5. `estado_bot.py` — Persistência de Estado
Gerencia as configurações dinâmicas da aplicação em formato JSON:
* **`carregar_estado()`**: lê o arquivo local `estado_bot.json` ou inicializa um dicionário padrão caso o arquivo ainda não exista.
* **`salvar_estado(estado)`**: grava o estado atualizado (`alertas_ativos`, `latitude`, `longitude`, `ultimo_update_id`) em `estado_bot.json` com codificação `UTF-8`.

---

## 📚 Conceitos e Termos Técnicos Aplicados

| Termo / Recurso | Aplicação no Projeto |
| :--- | :--- |
| **Variáveis de Ambiente (`.env`)** | Armazenamento seguro de credenciais fora do código-fonte usando `os.getenv()` e `python-dotenv`. |
| **GitHub Secrets** | Cofre criptografado no repositório para injetar `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` durante a execução na nuvem. |
| **`.gitignore` e `git rm --cached`** | Garantia de que arquivos sensíveis (`.env`) e dados pessoais de GPS (`estado_bot.json`) permaneçam apenas no ambiente local, sem versionamento no GitHub. |
| **CI/CD & Cron Schedule** | Automação via `.github/workflows/weather_ia.yml` agendada com `cron: "*/30 * * * *"` (a cada 30 minutos em UTC) e disparo manual via `workflow_dispatch`. |
| **API REST & JSON** | Integração via biblioteca `requests` com tratamento de status HTTP, timeouts e serialização/desserialização JSON. |

---

## 🤖 Comandos e Interatividade no Telegram

O controle operacional do bot é feito diretamente pelo chat autorizado no Telegram:

| Ação no Telegram | O que o Sistema Faz |
| :--- | :--- |
| **`/ativar`** | Altera `alertas_ativos` para `True` e confirma no chat. As verificações agendadas passam a enviar notificações para o Telegram e para o relógio. |
| **`/desativar`** | Altera `alertas_ativos` para `False` e confirma no chat. Pausa o envio de alertas automáticos até que `/ativar` seja enviado novamente. |
| **Enviar Localização (Pin GPS)** | Atualiza `latitude` e `longitude` com as coordenadas compartilhadas e dispara imediatamente uma leitura do clima para o novo local. |

---

## 🔐 Configuração Local e na Nuvem (Segurança)

### 1. Instalação Local
```bash
# Clonar o repositório
git clone https://github.com/EduardoSantos10/Weather.ia.git
cd Weather.ia

# Instalar dependências
pip install -r requirements.txt
```

### 2. Arquivo `.env` (Ambiente Local)
Crie um arquivo `.env` na raiz do projeto (nunca suba este arquivo para o Git):
```env
TELEGRAM_BOT_TOKEN=seu_token_gerado_pelo_botfather
TELEGRAM_CHAT_ID=seu_chat_id_numerico
```

### 3. GitHub Secrets (Ambiente Nuvem)
No repositório do GitHub, acesse **Settings → Secrets and variables → Actions** e cadastre:
* `TELEGRAM_BOT_TOKEN`
* `TELEGRAM_CHAT_ID`

---

## ⚙️ Automação com GitHub Actions e Ajustes Realizados

O workflow `.github/workflows/weather_ia.yml` executa o pipeline completo em um ambiente Linux (`ubuntu-latest`):

```yaml
name: Weather.ia Automação

on:
  schedule:
    - cron: "*/30 * * * *"
  workflow_dispatch:

jobs:
  verificar-clima:
    runs-on: ubuntu-latest
    steps:
      - name: Baixar código do repositório
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Instalar dependências
        run: pip install -r requirements.txt

      - name: Executar Weather.ia
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: python main.py
```

### Principais Ajustes Técnicos Documentados
1. **Compatibilidade de Runtime no Runner:** O ambiente de desenvolvimento local utilizava Python 3.8, mas os runners atuais do GitHub Actions (`Ubuntu 26.04`) não disponibilizam binários para versões EOL (End-of-Life). O workflow foi ajustado para `python-version: "3.11"`, garantindo execução estável em ~14 segundos.
2. **Remoção de Estado Local do Controle de Versão:** O arquivo `estado_bot.json` foi adicionado ao `.gitignore` e removido do índice do Git via `git rm --cached estado_bot.json`, preservando o arquivo localmente e protegendo coordenadas geográficas no repositório.
3. **Execução Efêmera na Nuvem:** Como cada execução do GitHub Actions inicia um container limpo, o bot consulta a fila do Telegram (`getUpdates`) antes de avaliar o clima, sincronizando comandos enviados pelo usuário antes do disparo.

---

## 🚀 Roadmap (Próximas Evoluções)

- [ ] **Comando `/clima` sob demanda:** permitir consulta imediata da previsão do ponto salvo mesmo quando os alertas automáticos estiverem pausados (`/desativar`).
- [ ] **Integração com API de IA Generativa:** adicionar camada de enriquecimento textual para resumos meteorológicos mais naturais, mantendo `regras_clima.py` como fonte determinística dos dados numéricos e fallback automático em caso de indisponibilidade da API.
- [ ] **Persistência de Estado na Nuvem:** armazenar o estado operacional entre execuções agendadas do GitHub Actions.