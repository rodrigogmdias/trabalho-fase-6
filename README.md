# SCIC - Sistema de Comunicação Interplanetária da Colônia

Projeto da Fase 6 (Comunicação Interplanetária) - Ciência da Computação FIAP.

O SCIC é um protótipo em Python que analisa os dados operacionais e de comunicação dos módulos da colônia Aurora Siger. Ele carrega uma base simulada, calcula indicadores de latência, erro absoluto e erro relativo, treina um modelo simples de regressão para prever a latência, prioriza alertas com heap, faz busca por prefixo com trie e relaciona os sensores com bases numéricas e eletricidade básica.

## Arquivos

| Arquivo | Descrição |
|---|---|
| `codigo_fonte.py` | Arquivo principal do sistema (menu no terminal) |
| `scic/config.py` | Constantes: arquivo de dados, pasta de gráficos e limites de erro |
| `scic/dados.py` | Leitura do CSV, colunas calculadas, resumo e consultas |
| `scic/indicadores.py` | Indicadores de comunicação, erro absoluto/relativo e ponto flutuante |
| `scic/modelo.py` | Regressão linear, métricas (MAE, MSE, RMSE, R²) e AIC/BIC |
| `scic/simulacao.py` | Simulação da latência com o método de Euler |
| `scic/heap.py` | Max-heap (fila de prioridade) com heapify-up e heapify-down |
| `scic/alertas.py` | Pontuação e priorização dos alertas usando o heap |
| `scic/trie.py` | Estrutura trie com inserção, busca e autocomplete |
| `scic/busca.py` | Montagem da trie com os registros e busca por prefixo |
| `scic/eletrica.py` | Bases numéricas, potência, Lei de Ohm e energia |
| `scic/relatorio.py` | Análise final e recomendações |
| `dados_aurora_siger.csv` | Base de dados simulada com 12 módulos em 4 ciclos (48 registros) |
| `relatorio_tecnico.md` | Relatório técnico com a explicação e análise dos resultados |
| `pyproject.toml` / `uv.lock` | Dependências do projeto gerenciadas pelo uv |
| `requirements.txt` | Mesmas dependências para instalar com pip |
| `graficos_ou_imagens/` | Gráficos gerados durante a execução (criada automaticamente) |

### Colunas da base de dados

`ciclo`, `modulo`, `tipo`, `codigo_sensor` (hexadecimal), `tensao_v`, `corrente_a`, `carga_rede_pct`, `perda_pacotes_pct`, `latencia_prevista_ms`, `latencia_observada_ms`, `status` (ativo, manutencao, alerta), `prioridade` (1 a 5) e `mensagem`.

## Dependências

- Python 3.12
- NumPy
- Pandas
- Matplotlib
- scikit-learn

Todas foram vistas na fase. O AIC e o BIC foram calculados pela fórmula, sem usar biblioteca extra.

## Como executar

É preciso ter o [uv](https://docs.astral.sh/uv/) instalado.

```bash
uv sync
uv run codigo_fonte.py
```

O `uv sync` cria o ambiente virtual e instala as dependências do `uv.lock`. Depois é só escolher as opções no menu, começando pela opção 1.

Sem o uv, dá para instalar pelo `requirements.txt` (gerado com `uv export`):

```bash
pip install -r requirements.txt
python codigo_fonte.py
```

## Funcionalidades do menu

1. **Carregar dados da colônia**: lê o CSV com Pandas e calcula potência (P = V x I), resistência (R = V / I), erro absoluto, erro relativo e o código do sensor em decimal e binário.
2. **Consultar registros**: por módulo, status ou ciclo.
3. **Calcular indicadores e erros numéricos**: latência média, desvio padrão, perda de pacotes, disponibilidade, erro absoluto e relativo por módulo (aceitável até 5%, atenção até 10%, preocupante acima de 10%) e demonstração de precisão em ponto flutuante.
4. **Treinar e avaliar modelo de previsão**: regressão linear com divisão treino/teste (75/25), métricas MAE, MSE, RMSE e R², comparação de dois modelos com AIC e BIC, gráfico real x previsto e simulação de novas previsões.
5. **Simular latência com método de Euler**: recuperação da latência depois de uma falha, comparando Euler com a solução exata.
6. **Priorizar alertas (heap)**: max-heap feito com heapify-up e heapify-down que devolve os alertas mais urgentes.
7. **Buscar por prefixo (trie)**: autocomplete por nome de módulo, tipo, código do sensor ou palavra do alerta.
8. **Bases numéricas e eletricidade**: conversão de código hexadecimal para decimal, binário e octal, potência, Lei de Ohm e energia do transmissor.
9. **Análise final**: resumo dos módulos críticos, modelo recomendado e recomendações.

## Exemplo de execução

```
========== SCIC - AURORA SIGER ==========
1 - Carregar dados da colônia
...
Escolha uma opção: 6

===== PRIORIZAÇÃO DE ALERTAS COM HEAP =====
26 alertas inseridos no heap.
Quantos alertas mais urgentes deseja ver? 3
1º [ 96.36] ciclo 4 | Suporte Medico (0x1A43) | alerta | Perda de pacotes elevada | erro rel 11.96%
2º [ 94.56] ciclo 2 | Comando Orbital (0x1A10) | alerta | Queda de tensao no transmissor | erro rel 8.14%
3º [ 90.73] ciclo 4 | Comunicacao Central (0x1A04) | alerta | Perda de pacotes elevada | erro rel 6.65%
```
