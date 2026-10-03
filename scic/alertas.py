from scic.config import LIMITE_ERRO_ACEITAVEL
from scic.heap import FilaAlertas


# Quanto maior a pontuação, mais urgente é o alerta
def calcular_pontuacao(linha):
    pontos = linha["prioridade"] * 10
    pontos += linha["erro_relativo"] * 100
    pontos += linha["perda_pacotes_pct"] * 2
    if linha["status"] == "alerta":
        pontos += 20
    if linha["tipo"] in ("comunicacao", "suporte medico"):
        pontos += 10
    return round(pontos, 2)


def priorizar_alertas(df):
    print("\n===== PRIORIZAÇÃO DE ALERTAS COM HEAP =====")
    fila = FilaAlertas()
    # Entram no heap os registros que não estão ativos ou que têm erro acima do aceitável
    alertas = df[(df["status"] != "ativo") | (df["erro_relativo"] > LIMITE_ERRO_ACEITAVEL)]
    for _, linha in alertas.iterrows():
        alerta = {
            "ciclo": linha["ciclo"],
            "modulo": linha["modulo"],
            "codigo": linha["codigo_sensor"],
            "status": linha["status"],
            "mensagem": linha["mensagem"],
            "erro_relativo": linha["erro_relativo"],
        }
        fila.inserir(calcular_pontuacao(linha), alerta)
    print(f"{fila.tamanho()} alertas inseridos no heap.")
    print("Critério: prioridade x10 + erro relativo (%) + perda de pacotes x2 + 20 se status alerta + 10 se módulo essencial")
    try:
        qtd = int(input("Quantos alertas mais urgentes deseja ver? ") or 5)
    except ValueError:
        qtd = 5
    for i in range(min(qtd, fila.tamanho())):
        pontos, a = fila.remover_mais_urgente()
        print(f"{i + 1}º [{pontos:6.2f}] ciclo {a['ciclo']} | {a['modulo']} ({a['codigo']}) | {a['status']} | "
              f"{a['mensagem']} | erro rel {a['erro_relativo'] * 100:.2f}%")
    print("Com heap o alerta mais urgente sai em O(log n), sem precisar ordenar a lista toda a cada novo alerta.")
