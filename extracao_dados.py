import requests
import xml.etree.ElementTree as ET
import csv
import os


# Função para verificar o formato da resposta
def verificar_formato(resposta):
    content_type = resposta.headers['Content-Type']
    
    if 'application/json' in content_type:
        dados = resposta.json()
        
        if 'data' in dados and isinstance(dados['data'], list) and len(dados['data']) > 0:
            if 'survey_data' in dados['data'][0]:
                return "formato_antigo", dados
            else:
                return "formato_novo", dados
        else:
            raise ValueError("Finalizado extração")
    elif 'application/xml' in content_type or 'text/xml' in content_type:
        return "formato_xml", resposta.text
    else:
        raise ValueError("Formato desconhecido da resposta.")

# Função para carregar IDs já processados no CSV
def carregar_ids_processados(caminho_csv):
    ids_processados = set()
    if os.path.exists(caminho_csv):
        with open(caminho_csv, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Pular o cabeçalho
            for row in reader:
                ids_processados.add(row[0])  # Considerando que o 'ID da Pesquisa' está na primeira coluna
    return ids_processados

# Função para processar o formato antigo (JSON)
def processar_formato_antigo(dados, writer, ids_processados):
    for formulario in dados['data']:
        id_pesquisa = formulario['id']
        if id_pesquisa in ids_processados:
            #print(f"ID da Pesquisa {id_pesquisa} já processado, ignorando.")
            continue
        
        contact_id = formulario.get('contact_id', '[Contact ID não disponível]')
        status = formulario.get('status', '[Status não disponível]')
        
        for key, survey in formulario.get('survey_data', {}).items():
            pergunta = survey['question']
            if 'answer' in survey:
                if isinstance(survey['answer'], list):
                    for option in survey['answer']:
                        resposta = f"{option['option']} (Rank: {option['rank']})"
                        writer.writerow([id_pesquisa, contact_id, status, pergunta, resposta])
                else:
                    resposta = survey['answer']
                    writer.writerow([id_pesquisa, contact_id, status, pergunta, resposta])
            else:
                writer.writerow([id_pesquisa, contact_id, status, pergunta, "[Sem resposta fornecida]"])
        ids_processados.add(id_pesquisa)  # Adiciona o ID ao conjunto de processados

# Função para processar o formato novo (JSON)
def processar_formato_novo(dados, writer, ids_processados):
    for formulario in dados['data']:
        id_pesquisa = formulario['id']
        if id_pesquisa in ids_processados:
            #print(f"ID da Pesquisa {id_pesquisa} já processado, ignorando.")
            continue
        
        contact_id = formulario.get('contact_id', '[Contact ID não disponível]')
        status = formulario.get('status', '[Status não disponível]')
        
        for key, value in formulario.items():
            if key not in ["id", "contact_id", "status", "date_submitted", "session_id", "language", "date_started", "ip_address", "referer", "user_agent", "country"]:
                pergunta = key
                if isinstance(value, list):
                    if value:
                        for option in value:
                            resposta = f"{option['option']} (Rank: {option['rank']})"
                            writer.writerow([id_pesquisa, contact_id, status, pergunta, resposta])
                    else:
                        writer.writerow([id_pesquisa, contact_id, status, pergunta, "[Sem resposta fornecida]"])
                elif value:
                    writer.writerow([id_pesquisa, contact_id, status, pergunta, value])
                else:
                    writer.writerow([id_pesquisa, contact_id, status, pergunta, "[Sem resposta fornecida]"])
        ids_processados.add(id_pesquisa)

# Função para processar o formato XML
def processar_formato_xml(xml_data, writer, ids_processados):
    root = ET.fromstring(xml_data)
    
    for item in root.findall(".//item"):
        id_pesquisa = item.find('id').text if item.find('id') is not None else "[ID não disponível]"
        if id_pesquisa in ids_processados:
            #print(f"ID da Pesquisa {id_pesquisa} já processado, ignorando.")
            continue
        
        contact_id = item.find('contact_id').text if item.find('contact_id') is not None else "[Contact ID não disponível]"
        status = item.find('status').text if item.find('status') is not None else "[Status não disponível]"
        
        for survey_item in item.findall(".//survey_data/item"):
            pergunta = survey_item.find('question').text if survey_item.find('question') is not None else "[Pergunta não disponível]"
            resposta_element = survey_item.find('answer')
            resposta = resposta_element.text if resposta_element is not None and resposta_element.text is not None else "[Sem resposta fornecida]"
            writer.writerow([id_pesquisa, contact_id, status, pergunta, resposta])
        ids_processados.add(id_pesquisa)

# Função principal para obter dados da API
def obter_respostas_formulario():
    survey_id = 1  # Iniciando com o ID 1
    caminho_csv = '/home/gustavo-faria/Documentos/Numera_01/respostas_survey.csv'
    
    # Carrega IDs já processados
    ids_processados = carregar_ids_processados(caminho_csv)

    # Abrindo o arquivo CSV para adição
    with open(caminho_csv, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Escrevendo o cabeçalho apenas se o arquivo estiver vazio
        if not ids_processados:
            writer.writerow(['ID da Pesquisa', 'Contact ID', 'Status', 'Pergunta', 'Resposta'])
        
        while True:
            url = f"https://numera-case.web.app/v1/survey/{survey_id}/answers"
            print(f"Consultando: {url}")
            
            try:
                resposta = requests.get(url)
                
                # Tratamento para resposta 404
                if resposta.status_code == 404:
                    print(f"Nenhum dado encontrado para survey_id {survey_id}. Encerrando.")
                    break
                
                resposta.raise_for_status()  # Levanta um erro se o status não for 200
                
                formato, dados = verificar_formato(resposta)
                
                if formato == "formato_antigo":
                    processar_formato_antigo(dados, writer, ids_processados)
                elif formato == "formato_novo":
                    processar_formato_novo(dados, writer, ids_processados)
                elif formato == "formato_xml":
                    processar_formato_xml(dados, writer, ids_processados)
            
            except requests.exceptions.HTTPError as errh:
                print(f"Erro HTTP: {errh}")
                break
            except requests.exceptions.ConnectionError as errc:
                print(f"Erro de conexão: {errc}")
                break
            except requests.exceptions.Timeout as errt:
                print(f"Erro de timeout: {errt}")
                break
            except requests.exceptions.RequestException as err:
                print(f"Erro na requisição: {err}")
                break
            except ValueError as e:
                print(e)
                break

            survey_id += 1  # Incrementando o ID para a próxima pesquisa

# Iniciando o processo
print(f"Iniciando análise de formulários!")
obter_respostas_formulario()
