from scic.trie import Trie


# Indexa nome do módulo, código do sensor, tipo e palavras das mensagens
def montar_trie(df):
    trie = Trie()
    for _, linha in df.iterrows():
        registro = f"{linha['modulo']} | {linha['codigo_sensor']} | ciclo {linha['ciclo']} | {linha['status']}"
        trie.inserir(linha["modulo"], registro)
        trie.inserir(linha["codigo_sensor"], registro)
        trie.inserir(linha["tipo"], registro)
        for palavra in linha["mensagem"].split():
            if len(palavra) > 3:
                trie.inserir(palavra, registro)
    return trie


def buscar_prefixo(trie):
    print("\n===== BUSCA POR PREFIXO COM TRIE =====")
    print("Pode buscar por nome de módulo, tipo, código do sensor (ex: 0x1a) ou palavra do alerta.")
    prefixo = input("Digite o prefixo: ").strip()
    if not prefixo:
        print("Prefixo vazio.")
        return
    resultados = trie.autocompletar(prefixo)
    if not resultados:
        print("Nenhum registro encontrado.")
        return
    print(f"{len(resultados)} palavra(s) encontrada(s):")
    for palavra, registros in resultados[:15]:
        print(f"- {palavra} ({len(registros)} registro(s))")
        for reg in registros[:3]:
            print(f"     {reg}")
