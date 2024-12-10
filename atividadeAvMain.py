from atividadeAvFunction import (
    apresenta_relatorio,
    cria_arquivo_parcial,
    cria_resumo,
    busca_top_votados_por_cidade,
    deleta_arquivos_gerados
)

def menu():
    while True:
        print("\nEscolha uma opção:")
        print("1 - Apresenta Relatório")
        print("2 - Cria Arquivo Parcial")
        print("3 - Cria Resumo")
        print("4 - Busca Top Votados por Cidade")
        print("5 - Deleta Arquivos Gerados")
        print("6 - Sair")

        opcao = input("Digite sua escolha: ")

        if opcao == "1":
            apresenta_relatorio()
        elif opcao == "2":
            cria_arquivo_parcial()
        elif opcao == "3":
            cria_resumo()
        elif opcao == "4":
            cidade = input("Digite o nome da cidade para pesquisa: ").strip()
            busca_top_votados_por_cidade("boletimSC.csv", cidade)
        elif opcao == "5":
            deleta_arquivos_gerados()
        elif opcao == "6":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()