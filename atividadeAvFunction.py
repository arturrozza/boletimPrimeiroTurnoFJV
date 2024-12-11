import csv
import os


def apresenta_relatorio():
    #verifica se o arquivo existe
    if not os.path.exists("boletimSC.csv"):
        print("ERRO, arquivo não encontrado, digite o nome correto!")
        return
    
    #abre arquivo pra leitura
    with open("boletimSC.csv", "r") as arquivo:
        leitor = csv.reader(arquivo, delimiter=";")
        linhas = list(leitor)

    #se o arquivo não estiver vazio vai exibir as informações pedidas
    if len(linhas) > 0:
        cabecalho = linhas [0]
        numero_linhas = len(linhas)
        print(f"Número total de linhas (inclui cabeçalho): {numero_linhas}")
        print(f"Número de colunas: {len(cabecalho)}")
        print(f"Nome das colunas: {', '.join(cabecalho)}")
    else:
        print("Arquivo vazio.")

def cria_arquivo_parcial():
    arquivo_origem = "boletimSC.csv"
    #verifica a existencia do arquivo origem
    if not os.path.exists(arquivo_origem):
        print("ERRO: Arquivo origem não encontrado")
        return
    
    #pede os dados para filtrar 
    arquivo_destino = input("Digite um nome para o arquivo csv destino (exemplo.csv): ")
    filtro_partido = input("Digite o partido para filtrar: ").strip()
    top_n_str = input("Digite o numero de cidades que deseja listar: ")


    #verifica se o numero de cidades é valido
    if not top_n_str.isdigit():
        print("ERRO: Digite um número válido para o top.")
        return
    top_n = int(top_n_str) 

    with open(arquivo_origem, "r") as arquivo_origem:
        leitor =  csv.reader(arquivo_origem, delimiter=";")
        cabecalho = next(leitor)


        #verifica se os cabecalhos existem
        if "NM_MUNICIPIO" not in cabecalho or "SG_PARTIDO" not in cabecalho or "QT_VOTOS" not in cabecalho:
            print("ERRO: Arquivo de origem não possuí os cabeçalhos esperados.")
            return
        
        #identifica os indices relevantes
        indice_cidade = cabecalho.index("NM_MUNICIPIO")
        indice_partido = cabecalho.index("SG_PARTIDO")
        indice_votos = cabecalho.index("QT_VOTOS")

        #filtra os dados pelo partido
        dados_filtrados = [
            (linha[indice_cidade], int(linha[indice_votos]))
            for linha in leitor if linha[indice_partido].strip().lower() == filtro_partido.lower()
        ]

        #ordena os dados
        dados_filtrados.sort(key=lambda x: x[1], reverse=True)
        dados_filtrados = dados_filtrados[:top_n]

        #escreve os dados no arquivo destino
        with open(arquivo_destino, "w", newline="") as arquivo_destino:
            escritor = csv.writer(arquivo_destino)
            escritor.writerow(["Cidade", "Votos"])
            escritor.writerows(dados_filtrados)

        print(f"Arquivo '{arquivo_destino}' criado com sucesso com os dados filtrados!")


def cria_resumo():
    arquivo_origem = "boletimSC.csv"
    if not os.path.exists(arquivo_origem):
        print("ERRO: Arquivo origem não encontrado")
        return

    with open(arquivo_origem, "r") as arquivo:
        leitor = csv.reader(arquivo, delimiter=";")
        cabecalho = next(leitor)

        if "SG_PARTIDO" not in cabecalho or "QT_VOTOS" not in cabecalho:
            print("ERRO: Arquivo de origem não possui os cabeçalhos esperados.")
            return


        indice_partido = cabecalho.index("SG_PARTIDO")
        indice_votos = cabecalho.index("QT_VOTOS")

        totalizadores = {}
        for linha in leitor:
            partido = linha[indice_partido].strip()
            votos = int(linha[indice_votos])
            totalizadores[partido] = totalizadores.get(partido, 0) + votos

        with open("resumo.csv", "w", newline="") as arquivo_resumo:
            escritor = csv.writer(arquivo_resumo)
            escritor.writerow(["Partido", "Total de Votos"])
            escritor.writerows(totalizadores.items())

        print("Arquivo 'resumo.csv' criado com sucesso!")


def busca_top_votados_por_cidade(arquivo, cidade):
    prefeitos = []
    vereadores = []

    with open(arquivo, "r", newline="") as f:
        leitor = csv.reader(f, delimiter=";")
        cabecalho = next(leitor)

        index_municipio = cabecalho.index("NM_MUNICIPIO")
        index_cargo = cabecalho.index("DS_CARGO_PERGUNTA")
        index_nome = cabecalho.index("NM_VOTAVEL")
        index_votos = cabecalho.index("QT_VOTOS")

        for linha in leitor:
            if linha[index_municipio].strip().lower() == cidade.lower():
                if linha[index_cargo].strip() == "Prefeito":
                    prefeitos.append((linha[index_nome], int(linha[index_votos])))
                elif linha[index_cargo].strip() == "Vereador":
                    vereadores.append((linha[index_nome], int(linha[index_votos])))

    prefeitos.sort(key=lambda x: x[1], reverse=True)
    vereadores.sort(key=lambda x: x[1], reverse=True)

    print(f"Top 3 prefeitos de {cidade}:")
    for i, (nome, votos) in enumerate(prefeitos[:3]):
        print(f"{i+1}. {nome} - {votos} votos")

    print("\nTop 15 vereadores de {cidade}:")
    for i, (nome, votos) in enumerate(vereadores[:15]):
        print(f"{i+1}. {nome} - {votos} votos")

    salvar = input("Deseja salvar os resultados em um arquivo CSV? (s/n): ").strip().lower()
    if salvar == "s":
        nome_arquivo = input("Digite o nome do arquivo de saída (exemplo_resultados.csv): ").strip()
        with open(nome_arquivo, "w", newline="") as f_saida:
            escritor = csv.writer(f_saida, delimiter=";")
            escritor.writerow(["Categoria", "Nome", "Votos"])

            for i, (nome, votos) in enumerate(prefeitos[:3]):
                escritor.writerow(["Prefeito", nome, votos])

            for i, (nome, votos) in enumerate(vereadores[:15]):
                escritor.writerow(["Vereador", nome, votos])

        print(f"Resultados salvos em '{nome_arquivo}'.")


def deleta_arquivos_gerados():
    arquivos = [arq for arq in os.listdir() if arq.endswith(".csv") and arq != "boletimSC.csv"]

    if not arquivos:
        print("Nenhum arquivo .csv encontrado.")
        return

    print("Arquivos disponíveis para exclusão:")
    for index, arquivo in enumerate(arquivos, start=1):
        print(f"{index}. {arquivo}")

    selecionar = input("Digite os números dos arquivos que deseja deletar, separados por vírgula (ou 'todos' para excluir tudo): ").strip()

    if selecionar.lower() == "todos":
        arquivos_selecionados = arquivos
    else:
        indices = selecionar.split(",")
        if all(num.isdigit() and 1 <= int(num) <= len(arquivos) for num in indices):
            arquivos_selecionados = [arquivos[int(num) - 1] for num in indices]
        else:
            print("Entrada inválida.")
            return
    
    for arquivo in arquivos_selecionados:
        if os.path.exists(arquivo):
            os.remove(arquivo)
            print(f"Arquivo '{arquivo}' deletado.")
        else:
            print(f"Arquivo '{arquivo}' não encontrado")

