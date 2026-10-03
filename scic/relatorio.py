from scic.config import LIMITE_ERRO_ACEITAVEL, LIMITE_ERRO_PREOCUPANTE


def analise_final(df, resultados):
    print("\n===== ANÁLISE FINAL DO SCIC =====")
    criticos = df[df["erro_relativo"] > LIMITE_ERRO_PREOCUPANTE]["modulo"].unique()
    atencao = df.groupby("modulo")["erro_relativo"].mean()
    atencao = atencao[atencao > LIMITE_ERRO_ACEITAVEL].index.tolist()
    print(f"Registros em alerta: {(df['status'] == 'alerta').sum()} de {len(df)}")
    print(f"Módulos com erro relativo preocupante em algum ciclo: {', '.join(criticos) if len(criticos) else 'nenhum'}")
    print(f"Módulos com erro médio acima de {LIMITE_ERRO_ACEITAVEL * 100:.0f}%: {', '.join(atencao) if atencao else 'nenhum'}")
    pior = df.groupby("modulo")["latencia_observada_ms"].mean().idxmax()
    print(f"Módulo com maior latência média: {pior}")
    if resultados:
        melhor = min(resultados, key=lambda m: resultados[m]["bic"])
        print(f"Modelo recomendado: {melhor} (R² = {resultados[melhor]['r2']:.3f}, MAE = {resultados[melhor]['mae']:.2f} ms)")
    else:
        print("Modelo ainda não foi treinado (opção 4).")
    print("\nRecomendações:")
    print("- Fazer manutenção preditiva nos módulos com erro relativo alto antes que virem falha.")
    print("- Usar a Antena Redundante quando a Comunicacao Central passar do limite de latência.")
    print("- Desligar transmissões não essenciais em horários de carga alta para economizar energia.")
    print("- As decisões automáticas devem sempre ser validadas pela equipe humana da colônia.")
