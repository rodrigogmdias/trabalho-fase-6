import math

import numpy as np

from scic.config import LIMITE_ERRO_ACEITAVEL, LIMITE_ERRO_PREOCUPANTE


def classificar_erro(erro_relativo):
    if erro_relativo <= LIMITE_ERRO_ACEITAVEL:
        return "aceitável"
    if erro_relativo <= LIMITE_ERRO_PREOCUPANTE:
        return "atenção"
    return "preocupante"


def calcular_indicadores(df):
    print("\n===== INDICADORES DE COMUNICAÇÃO =====")
    latencias = df["latencia_observada_ms"].to_numpy()
    print(f"Latência média observada: {np.mean(latencias):.2f} ms")
    print(f"Desvio padrão da latência: {np.std(latencias):.2f} ms")
    print(f"Maior latência: {np.max(latencias):.2f} ms")
    print(f"Perda média de pacotes: {df['perda_pacotes_pct'].mean():.2f} %")
    disponibilidade = (df["status"] != "alerta").sum() / len(df) * 100
    print(f"Disponibilidade dos enlaces (registros sem alerta): {disponibilidade:.1f} %")

    print("\n===== ERRO ABSOLUTO E RELATIVO POR MÓDULO (média dos ciclos) =====")
    por_modulo = df.groupby("modulo")[["latencia_prevista_ms", "latencia_observada_ms", "erro_absoluto_ms", "erro_relativo"]].mean()
    por_modulo = por_modulo.sort_values("erro_relativo", ascending=False)
    for modulo, linha in por_modulo.iterrows():
        print(f"{modulo:<25} prevista={linha['latencia_prevista_ms']:7.2f} ms  observada={linha['latencia_observada_ms']:7.2f} ms  "
              f"erro abs={linha['erro_absoluto_ms']:6.2f} ms  erro rel={linha['erro_relativo'] * 100:5.2f}%  -> {classificar_erro(linha['erro_relativo'])}")

    # Mostra que somas em ponto flutuante podem dar resultados um pouco diferentes
    print("\n===== PRECISÃO NUMÉRICA (PONTO FLUTUANTE) =====")
    x = 0.1 + 0.2
    print(f"0.1 + 0.2 = {format(x, '.17f')}")
    print(f"0.1 + 0.2 == 0.3? {x == 0.3}")
    print(f"math.isclose(0.1 + 0.2, 0.3)? {math.isclose(x, 0.3)}")
    soma_python = 0.0
    for valor in df["latencia_observada_ms"]:
        soma_python += valor
    soma_numpy = np.sum(df["latencia_observada_ms"].to_numpy())
    print(f"Soma das latências com laço: {soma_python:.12f}")
    print(f"Soma das latências com NumPy: {soma_numpy:.12f}")
    print(f"Diferença entre as somas: {abs(soma_python - soma_numpy):.2e}")
    print("Por isso o sistema compara erros usando tolerância e arredonda os valores exibidos.")
