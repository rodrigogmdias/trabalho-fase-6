import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from scic.config import PASTA_GRAFICOS


# AIC e BIC pela fórmula com a soma dos erros ao quadrado (k = número de parâmetros)
def calcular_aic_bic(y_real, y_previsto, k):
    n = len(y_real)
    sse = np.sum((np.array(y_real) - np.array(y_previsto)) ** 2)
    aic = n * np.log(sse / n) + 2 * k
    bic = n * np.log(sse / n) + k * np.log(n)
    return aic, bic


def treinar_modelo(df):
    print("\n===== MODELO DE PREVISÃO DE LATÊNCIA (REGRESSÃO LINEAR) =====")
    modelos = {
        "Modelo 1 (carga da rede)": ["carga_rede_pct"],
        "Modelo 2 (carga, potência e perda)": ["carga_rede_pct", "potencia_w", "perda_pacotes_pct"],
    }
    y = df["latencia_observada_ms"]
    resultados = {}
    # Treina os dois modelos com 75% dos dados e avalia nos 25% de teste
    for nome, colunas in modelos.items():
        X = df[colunas]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        modelo = LinearRegression()
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        aic, bic = calcular_aic_bic(y_train, modelo.predict(X_train), len(colunas) + 1)
        resultados[nome] = {"modelo": modelo, "colunas": colunas, "mae": mae, "mse": mse, "rmse": rmse,
                            "r2": r2, "aic": aic, "bic": bic, "y_test": y_test, "y_pred": y_pred}
        print(f"\n{nome}")
        print(f"Treino: {len(X_train)} registros | Teste: {len(X_test)} registros")
        print(f"MAE  : {mae:.2f} ms")
        print(f"MSE  : {mse:.2f}")
        print(f"RMSE : {rmse:.2f} ms")
        print(f"R²   : {r2:.4f}")
        print(f"AIC  : {aic:.2f} | BIC: {bic:.2f}")

    # O menor BIC indica o melhor equilíbrio entre ajuste e complexidade
    melhor = min(resultados, key=lambda m: resultados[m]["bic"])
    r = resultados[melhor]
    print(f"\nMelhor modelo pelo BIC: {melhor}")
    print(f"Em média o modelo erra {r['mae']:.2f} ms na latência.")
    if r["rmse"] > r["mae"] * 1.3:
        print("O RMSE está bem maior que o MAE, então existem alguns registros com erro grande.")
    else:
        print("RMSE e MAE estão próximos, então os erros estão bem distribuídos, sem muitos valores extremos.")
    print(f"O R² mostra que o modelo explica cerca de {r['r2'] * 100:.1f}% da variação da latência,")
    print("mas um R² alto não quer dizer que o modelo é perfeito, por isso olhamos todas as métricas juntas.")

    os.makedirs(PASTA_GRAFICOS, exist_ok=True)
    plt.figure(figsize=(7, 5))
    plt.scatter(r["y_test"], r["y_pred"], color="tab:blue")
    minimo = min(r["y_test"].min(), r["y_pred"].min())
    maximo = max(r["y_test"].max(), r["y_pred"].max())
    plt.plot([minimo, maximo], [minimo, maximo], "r--", label="Previsão perfeita")
    plt.xlabel("Latência observada (ms)")
    plt.ylabel("Latência prevista (ms)")
    plt.title(f"Real x Previsto - {melhor}")
    plt.legend()
    plt.grid(True)
    caminho = os.path.join(PASTA_GRAFICOS, "real_vs_previsto.png")
    plt.savefig(caminho)
    plt.close()
    print(f"Gráfico salvo em {caminho}")

    while True:
        resp = input("\nDeseja simular uma previsão nova? (s/n): ").strip().lower()
        if resp != "s":
            break
        try:
            valores = [float(input(f"Informe {coluna}: ")) for coluna in r["colunas"]]
        except ValueError:
            print("Valor inválido.")
            continue
        entrada = pd.DataFrame([valores], columns=r["colunas"])
        previsao = r["modelo"].predict(entrada)[0]
        print(f"Latência prevista: {previsao:.2f} ms")
    return resultados
