from flask import Flask, jsonify
import csv

app = Flask(__name__)

# Função para ler os dados do arquivo CSV e retornar uma lista de dicionários
def ler_dados_csv(caminho_csv):
    dados = []
    try:
        with open(caminho_csv, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Converter None para string vazia ou um valor padrão
                linha_tratada = {key if key is not None else "": (value if value is not None else "") for key, value in row.items()}
                dados.append(linha_tratada)
    except FileNotFoundError:
        return {"erro": "Arquivo CSV não encontrado."}, 404
    return dados

# Rota para obter os dados do CSV
@app.route('/dados', methods=['GET'])
def obter_dados():
    caminho_csv = '/home/gustavo-faria/Documentos/numera-case-solution/respostas_survey.csv'
    dados = ler_dados_csv(caminho_csv)
    return jsonify(dados)

# Inicializando a API
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8085)
