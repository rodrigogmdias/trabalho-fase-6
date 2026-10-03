import os

import pandas as pd

from scic.config import ARQUIVO_DADOS


def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        print(f"Arquivo {ARQUIVO_DADOS} não encontrado.")
        return None
    df = pd.read_csv(ARQUIVO_DADOS)
    df = df.dropna()
    # Colunas calculadas: potência (P = V x I), Lei de Ohm (R = V / I) e erros da latência
    df["potencia_w"] = (df["tensao_v"] * df["corrente_a"]).round(2)
    df["resistencia_ohm"] = (df["tensao_v"] / df["corrente_a"]).round(2)
    df["erro_absoluto_ms"] = (df["latencia_observada_ms"] - df["latencia_prevista_ms"]).abs().round(2)
    df["erro_relativo"] = (df["erro_absoluto_ms"] / df["latencia_prevista_ms"]).round(4)
    # Converte o código do sensor de hexadecimal para decimal e binário
    df["codigo_decimal"] = df["codigo_sensor"].apply(lambda c: int(c, 16))
    df["codigo_binario"] = df["codigo_decimal"].apply(lambda d: bin(d)[2:])
    return df


def mostrar_resumo(df):
    print("\n===== DADOS DA COLÔNIA AURORA SIGER =====")
    print(f"Total de registros: {len(df)}")
    print(f"Módulos monitorados: {df['modulo'].nunique()}")
    print(f"Ciclos registrados: {df['ciclo'].min()} até {df['ciclo'].max()}")
    print("\nQuantidade por status:")
    print(df["status"].value_counts().to_string())
    print("\nPrimeiros registros:")
    print(df[["ciclo", "modulo", "tipo", "codigo_sensor", "latencia_prevista_ms", "latencia_observada_ms", "status"]].head(10).to_string(index=False))


def consultar_registros(df):
    print("\n===== CONSULTAR REGISTROS =====")
    print("1 - Por módulo")
    print("2 - Por status")
    print("3 - Por ciclo")
    opcao = input("Escolha: ").strip()
    if opcao == "1":
        nome = input("Digite o nome (ou parte) do módulo: ").strip().lower()
        resultado = df[df["modulo"].str.lower().str.contains(nome)]
    elif opcao == "2":
        status = input("Digite o status (ativo, manutencao, alerta): ").strip().lower()
        resultado = df[df["status"] == status]
    elif opcao == "3":
        try:
            ciclo = int(input("Digite o ciclo: "))
        except ValueError:
            print("Ciclo inválido.")
            return
        resultado = df[df["ciclo"] == ciclo]
    else:
        print("Opção inválida.")
        return
    if resultado.empty:
        print("Nenhum registro encontrado.")
    else:
        print(resultado[["ciclo", "modulo", "status", "latencia_observada_ms", "prioridade", "mensagem"]].to_string(index=False))
