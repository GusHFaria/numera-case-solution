Passo a Passo para Preparar o Ambiente e Rodar Nossa Automação

Aqui está um guia completo para configurar e executar o script Python que acessa os dados do CSV e fornece uma API para consulta dos dados.

Requisitos:
Python 3.7 ou superior
pip (gerenciador de pacotes do Python)
Bibliotecas Python: Flask, requests
1. Instalar o Python
Se o Python ainda não estiver instalado, você pode baixá-lo em https://www.python.org/downloads/. Certifique-se de instalar a versão 3.7 ou superior.

2. Configurar um Ambiente Virtual (Opcional, mas Recomendado)
Configurar um ambiente virtual permite isolar as dependências do seu projeto. Para criar e ativar um ambiente virtual:

bash
Copiar código
# No Linux/macOS
python3 -m venv venv
source venv/bin/activate

# No Windows
python -m venv venv
venv\Scripts\activate
3. Instalar as Dependências
Com o ambiente virtual ativado (ou diretamente no sistema, se não estiver usando um ambiente virtual), instale as bibliotecas necessárias:

bash
Copiar código
pip install flask requests
4. Estrutura dos Arquivos
Certifique-se de que os dois arquivos estão no mesmo diretório ou conforme o caminho que você especificou nos scripts.

rotina.py: O script que realiza a extração dos dados da API e salva no CSV.
app.py: O script Flask que cria uma API para acessar os dados armazenados no CSV.
5. Executar o Script de Extração de Dados
Rode o script que extrai os dados da API e os salva no CSV:

bash
Copiar código
python extracao_dados.py
Esse script irá coletar os dados de acordo com os survey_id e salvar tudo no arquivo CSV.

6. Executar o Servidor Flask
Depois que os dados forem extraídos e salvos no CSV, execute o servidor Flask para fornecer acesso à API:

bash
Copiar código
python app.py
Esse comando iniciará o servidor Flask na porta 8085. A API estará disponível em http://localhost:8085/dados.

7. Acessar a API
Para acessar os dados, abra o navegador ou use ferramentas como curl ou Postman para fazer uma requisição GET no endpoint:

http://localhost:8085/dados
A API retornará os dados do CSV em formato JSON.

8. Automatizar a Execução (Opcional)
Se quiser automatizar a execução dos scripts para rodarem de tempos em tempos, você pode utilizar ferramentas de agendamento de tarefas como o cron no Linux/macOS ou o Task Scheduler no Windows.

Resumo
Instale o Python 3.7 ou superior.
Crie e ative um ambiente virtual (opcional).
Instale as dependências usando pip install flask requests.
Execute o script de extração (python rotina.py).
Execute o servidor Flask (python GusAPIDados.py).
Acesse a API em http://localhost:8085/dados.
Seguindo esses passos, você terá o ambiente pronto para rodar o script de extração de dados e a API em Flask. Se tiver dúvidas ou precisar de mais ajuda, estou à disposição!
