# Trie para busca por prefixo (cada nó guarda os registros da palavra que termina nele)
class NoTrie:
    def __init__(self):
        self.filhos = {}
        self.fim = False
        self.registros = []


class Trie:
    def __init__(self):
        self.raiz = NoTrie()

    def inserir(self, palavra, registro):
        no = self.raiz
        for letra in palavra.lower():
            if letra not in no.filhos:
                no.filhos[letra] = NoTrie()
            no = no.filhos[letra]
        no.fim = True
        if registro not in no.registros:
            no.registros.append(registro)

    def buscar(self, palavra):
        no = self.raiz
        for letra in palavra.lower():
            if letra not in no.filhos:
                return False
            no = no.filhos[letra]
        return no.fim

    # Anda até o nó do prefixo e depois coleta todas as palavras abaixo dele
    def autocompletar(self, prefixo):
        no = self.raiz
        for letra in prefixo.lower():
            if letra not in no.filhos:
                return []
            no = no.filhos[letra]
        resultados = []
        self._coletar(no, prefixo.lower(), resultados)
        return resultados

    def _coletar(self, no, palavra_atual, resultados):
        if no.fim:
            resultados.append((palavra_atual, no.registros))
        for letra, filho in no.filhos.items():
            self._coletar(filho, palavra_atual + letra, resultados)
