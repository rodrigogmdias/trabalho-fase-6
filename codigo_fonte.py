from scic.alertas import priorizar_alertas
from scic.busca import buscar_prefixo, montar_trie
from scic.dados import carregar_dados, consultar_registros, mostrar_resumo
from scic.eletrica import converter_bases
from scic.indicadores import calcular_indicadores
from scic.modelo import treinar_modelo
from scic.relatorio import analise_final
from scic.simulacao import simular_euler


# Menu principal do sistema no terminal
def menu():
    df = None
    trie = None
    resultados = None
    while True:
        print("\n========== SCIC - AURORA SIGER ==========")
        print("1 - Carregar dados da colônia")
        print("2 - Consultar registros")
        print("3 - Calcular indicadores e erros numéricos")
        print("4 - Treinar e avaliar modelo de previsão")
        print("5 - Simular latência com método de Euler")
        print("6 - Priorizar alertas (heap)")
        print("7 - Buscar por prefixo (trie)")
        print("8 - Bases numéricas e eletricidade")
        print("9 - Análise final")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            print("Encerrando o SCIC. Até mais!")
            break
        if opcao == "1":
            df = carregar_dados()
            if df is not None:
                trie = montar_trie(df)
                mostrar_resumo(df)
            continue
        if opcao in "23456789" and len(opcao) == 1 and df is None:
            print("Carregue os dados primeiro (opção 1).")
            continue
        if opcao == "2":
            consultar_registros(df)
        elif opcao == "3":
            calcular_indicadores(df)
        elif opcao == "4":
            resultados = treinar_modelo(df)
        elif opcao == "5":
            simular_euler(df)
        elif opcao == "6":
            priorizar_alertas(df)
        elif opcao == "7":
            buscar_prefixo(trie)
        elif opcao == "8":
            converter_bases(df)
        elif opcao == "9":
            analise_final(df, resultados)
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
