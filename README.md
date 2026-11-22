# Weather.ia
Projeto prático em Python com base no aprendizado de conceitos e pesquisas

# Como criar e ativar a venv
- python3 -m venv .venv

- source .venv/bin/activate

# Para desativar a venv
- deactivate

# Criação de arquivos
- regras_clima.py -> onde vai entrar o Bloco 1 (lógica de calor, frio, chuva, vento, granizo, neve, severidade e mensagem curta para celular + smartwatch Haylou S6).

- requirements.txt -> começa vazio (ou só com um comentário) e vamos preenchendo conforme entrarem bibliotecas externas nos próximos blocos.

- .gitignore -> você já tem o do GitHub, mas vale conferir se .venv/, __pycache__/ e .env estão lá dentro para nunca subirem sem querer.

# Utilizando funções, sintaxes e métodos
- append -> adiciona um único elemento ao final de uma lista existente.

- def -> serve para definir (criar) uma função. Uma função é um bloco de código reutilizável que executa uma tarefa específica e pode ser chamado várias vezes ao longo do programa.

# BLOCO 02:
- pip install requests instala a biblioteca apenas no seu ambiente virtual.

- pip freeze > requirements.txt registra a dependência para que, quando o GitHub Actions rodar na nuvem, ele saiba o que instalar.

- Bilbioteca requests: simplificar o envio de requisições HTTP para servidores web, permitindo que você se comunique com sites, consuma dados de APIs e faça a gestão de respostas de forma simples e intuitiva.

- raise_for_status() -> é um método de bibliotecas HTTP (como requests em Python) que verifica o código de status da resposta e lança uma exceção (HTTPError) se a requisição falhou. Quando a resposta é bem-sucedida, ele não faz nada e retorna None.

# BLOCO 03:

- os.getenv() -> serve para ler o valor de uma variável de ambiente do sistema operacional dentro de um código Python.
Ela faz parte do módulo nativo os e é muito usada para manter dados sensíveis ou configurações (como senhas, chaves de API e URLs de banco de dados) fora do código-fonte.