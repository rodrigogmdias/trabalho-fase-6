import math
import os

import matplotlib.pyplot as plt

from scic.config import PASTA_GRAFICOS


def simular_euler(df):
    print("\n===== SIMULAÇÃO DA LATÊNCIA COM MÉTODO DE EULER =====")
    print("Modelo: dL/dt = -k * (L - L_alvo), a latência volta para o normal depois de uma falha.")
    modulo = input("Nome do módulo (Enter para Comunicacao Central): ").strip() or "Comunicacao Central"
    dados = df[df["modulo"].str.lower() == modulo.lower()]
    if dados.empty:
        print("Módulo não encontrado.")
        return
    l_alvo = dados["latencia_prevista_ms"].mean()
    l0 = dados["latencia_observada_ms"].max() * 1.5
    k = 0.4
    h = 0.5
    passos = 20
    t = [0.0]
    l = [l0]
    # Euler: L(t + h) = L(t) + h * f(L)
    for _ in range(passos):
        l_novo = l[-1] + h * (-k * (l[-1] - l_alvo))
        l.append(l_novo)
        t.append(t[-1] + h)
    exata = [l_alvo + (l0 - l_alvo) * math.exp(-k * ti) for ti in t]
    print(f"Latência inicial após falha: {l0:.2f} ms | latência alvo: {l_alvo:.2f} ms")
    for i in range(0, len(t), 4):
        erro = abs(exata[i] - l[i])
        print(f"t={t[i]:4.1f}  Euler={l[i]:7.2f} ms  exata={exata[i]:7.2f} ms  erro abs={erro:.3f}")
    os.makedirs(PASTA_GRAFICOS, exist_ok=True)
    plt.figure(figsize=(7, 5))
    plt.plot(t, l, "o-", label="Euler")
    plt.plot(t, exata, label="Solução exata")
    plt.axhline(l_alvo, color="gray", linestyle="--", label="Latência alvo")
    plt.xlabel("Tempo (ciclos)")
    plt.ylabel("Latência (ms)")
    plt.title(f"Recuperação da latência - {modulo}")
    plt.legend()
    plt.grid(True)
    caminho = os.path.join(PASTA_GRAFICOS, "euler_latencia.png")
    plt.savefig(caminho)
    plt.close()
    print(f"Gráfico salvo em {caminho}")
