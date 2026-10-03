# Max-heap para a fila de prioridade dos alertas (o maior valor fica na raiz)
class FilaAlertas:
    def __init__(self):
        self.heap = []

    def pai(self, i):
        return (i - 1) // 2

    def filho_esquerdo(self, i):
        return 2 * i + 1

    def filho_direito(self, i):
        return 2 * i + 2

    def trocar(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    # Sobe o elemento enquanto ele for maior que o pai
    def heapify_up(self, i):
        while i > 0 and self.heap[i][0] > self.heap[self.pai(i)][0]:
            self.trocar(i, self.pai(i))
            i = self.pai(i)

    # Desce o elemento trocando com o maior filho até a propriedade do heap voltar
    def heapify_down(self, i):
        n = len(self.heap)
        maior = i
        esq = self.filho_esquerdo(i)
        dir = self.filho_direito(i)
        if esq < n and self.heap[esq][0] > self.heap[maior][0]:
            maior = esq
        if dir < n and self.heap[dir][0] > self.heap[maior][0]:
            maior = dir
        if maior != i:
            self.trocar(i, maior)
            self.heapify_down(maior)

    def inserir(self, pontuacao, alerta):
        self.heap.append((pontuacao, alerta))
        self.heapify_up(len(self.heap) - 1)

    # Remove a raiz (alerta mais urgente), coloca o último no lugar e reorganiza
    def remover_mais_urgente(self):
        if not self.heap:
            return None
        topo = self.heap[0]
        ultimo = self.heap.pop()
        if self.heap:
            self.heap[0] = ultimo
            self.heapify_down(0)
        return topo

    def tamanho(self):
        return len(self.heap)
