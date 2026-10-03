# Relatório Técnico - SCIC (Sistema de Comunicação Interplanetária da Colônia)

**Fase 6 - Comunicação Interplanetária | Ciência da Computação - FIAP**

## 1. Contexto da solução

Com o crescimento da colônia Aurora Siger, não basta mais só guardar registros: a equipe precisa saber se as previsões de latência são confiáveis, quais módulos estão com erro acima do aceitável e quais alertas devem ser atendidos primeiro. Um alerta ignorado ou uma busca lenta por um registro pode atrasar a resposta técnica e comprometer módulos essenciais, como o Suporte Médico ou a Comunicação Central.

O SCIC é um protótipo em Python que funciona como uma camada de avaliação e organização dos dados de comunicação da colônia. Ele roda no terminal com um menu e permite:

- carregar e consultar os dados dos módulos;
- calcular indicadores de comunicação e erros numéricos;
- treinar um modelo de regressão para prever a latência e avaliar o desempenho dele;
- simular a recuperação da latência com o método de Euler;
- priorizar alertas com heap;
- buscar registros por prefixo com trie;
- relacionar os sensores com bases numéricas e eletricidade básica;
- gerar uma análise final com recomendações.

O sistema não se conecta a sensores reais nem a APIs externas. Todos os dados são simulados, como permitido no enunciado.

## 2. Descrição dos dados

A base `dados_aurora_siger.csv` foi criada pela equipe com 12 módulos da colônia registrados em 4 ciclos, totalizando 48 registros. Os módulos cobrem os tipos comunicação, habitação, agricultura, laboratório, suporte médico e armazenamento de dados.

| Campo | Descrição |
|---|---|
| `ciclo` | Ciclo de registro (1 a 4) |
| `modulo` / `tipo` | Nome e tipo do módulo |
| `codigo_sensor` | Identificador do sensor em hexadecimal (ex: `0x1A08`) |
| `tensao_v` / `corrente_a` | Tensão e corrente do transmissor do módulo |
| `carga_rede_pct` | Ocupação da rede de comunicação do módulo (%) |
| `perda_pacotes_pct` | Perda de pacotes no enlace (%) |
| `latencia_prevista_ms` / `latencia_observada_ms` | Latência estimada e latência medida (ms) |
| `status` | ativo, manutencao ou alerta |
| `prioridade` | Nível de 1 a 5 (módulos essenciais começam mais alto) |
| `mensagem` | Resumo do evento ou alerta |

O arquivo é lido com Pandas (`scic/dados.py`) e o sistema cria algumas colunas novas:

- potência (`P = V x I`);
- resistência pela Lei de Ohm (`R = V / I`);
- erro absoluto e erro relativo da latência;
- código do sensor em decimal e em binário.

Distribuição dos status: 26 registros ativos, 17 em alerta e 5 em manutenção.

## 3. Indicadores de comunicação

Calculados com NumPy e Pandas em `scic/indicadores.py`:

| Indicador | Valor |
|---|---|
| Latência média observada | 308,34 ms |
| Desvio padrão da latência | 58,65 ms |
| Maior latência registrada | 455,24 ms (Agricultura Norte, ciclo 3) |
| Perda média de pacotes | 1,52 % |
| Disponibilidade (registros sem alerta) | 64,6 % |

O desvio padrão de quase 59 ms mostra que a latência varia bastante entre os módulos. A disponibilidade de 64,6% é baixa para uma colônia: mais de um terço dos registros estão em alerta. Isso justifica a necessidade de priorizar o atendimento.

## 4. Análise dos erros numéricos

### 4.1 Erro absoluto e erro relativo

Para cada registro, o sistema calcula:

- **Erro absoluto:** `|latência observada - latência prevista|`, em ms.
- **Erro relativo:** `erro absoluto / latência prevista`. Ele permite comparar módulos com latências de escalas diferentes.

Definimos três faixas para interpretar o erro relativo no contexto da colônia:

| Faixa | Erro relativo | Interpretação |
|---|---|---|
| Aceitável | até 5% | Variação normal do enlace |
| Atenção | de 5% a 10% | A previsão está se afastando do real; vale acompanhar |
| Preocupante | acima de 10% | Possível falha ou previsão inadequada; precisa de ação |

Média por módulo nos 4 ciclos (os três maiores e o menor):

| Módulo | Erro absoluto médio | Erro relativo médio | Faixa |
|---|---|---|---|
| Armazenamento de Dados | 20,09 ms | 7,63 % | atenção |
| Suporte Médico | 23,57 ms | 7,39 % | atenção |
| Habitação Alfa | 23,91 ms | 6,39 % | atenção |
| Antena Redundante | 5,76 ms | 2,02 % | aceitável |

Habitação Alfa e Suporte Médico têm erros absolutos parecidos (cerca de 23 ms). Mesmo assim, o erro relativo do Suporte Médico é maior, porque a latência prevista dele é menor. Esse é o motivo de usar o erro relativo: 23 ms pesam mais em um enlace de 307 ms do que em um de 371 ms. Os mesmos três módulos tiveram pelo menos um ciclo com erro acima de 10% (faixa preocupante).

### 4.2 Ponto flutuante e precisão numérica

O sistema também mostra que o computador representa números reais de forma aproximada:

- `0.1 + 0.2` resulta em `0.30000000000000004`, então `0.1 + 0.2 == 0.3` é `False`;
- `math.isclose(0.1 + 0.2, 0.3)` é `True`, porque compara com uma tolerância;
- somar as 48 latências com um laço `for` deu `14800.140000000003`, e com `np.sum` deu `14800.139999999999`, uma diferença de `3,64e-12`.

Essas diferenças são irrelevantes para a latência em milissegundos. Mesmo assim, por causa delas o sistema nunca compara erros com `==`: ele usa limites (5% e 10%) e arredonda os valores mostrados ao usuário.

### 4.3 Erro do método numérico (Euler)

Na opção 5, a recuperação da latência depois de uma falha é modelada pela equação `dL/dt = -k (L - L_alvo)` e resolvida com o método de Euler, com `k = 0,4` e passo `h = 0,5`. Para a Comunicação Central, a latência começa em 530,65 ms e volta para o alvo de 258,84 ms.

Como essa equação tem solução exata (`L(t) = L_alvo + (L0 - L_alvo)e^(-kt)`), dá para medir o erro do método:

| t | Euler | Exata | Erro absoluto |
|---|---|---|---|
| 0 | 530,65 | 530,65 | 0,000 |
| 2 | 370,17 | 380,97 | 10,799 |
| 4 | 304,44 | 313,71 | 9,276 |
| 10 | 261,97 | 263,81 | 1,845 |

O erro é maior no começo, quando a latência muda mais rápido, e diminui conforme ela se estabiliza. Um passo `h` menor reduziria o erro, mas exigiria mais iterações. O gráfico está em `graficos_ou_imagens/euler_latencia.png`.

## 5. Modelo simples e avaliação de performance

Usamos regressão linear (`LinearRegression` do scikit-learn) para prever a latência observada (`scic/modelo.py`). Os dados foram divididos com `train_test_split`: 75% para treino (36 registros) e 25% para teste (12 registros), com `random_state=42`. Comparamos dois modelos:

| Métrica | Modelo 1 (carga da rede) | Modelo 2 (carga, potência e perda) |
|---|---|---|
| MAE | 24,90 ms | 11,56 ms |
| MSE | 920,39 | 191,47 |
| RMSE | 30,34 ms | 13,84 ms |
| R² | 0,7852 | 0,9553 |
| AIC | 244,21 | 187,57 |
| BIC | 247,37 | 193,91 |

**Interpretação:**

- **MAE:** o Modelo 2 erra em média 11,56 ms, menos da metade do Modelo 1.
- **RMSE e MAE:** no Modelo 2 eles estão próximos (13,84 e 11,56). Isso indica que não há muitos registros com erro muito grande. Se o RMSE fosse bem maior que o MAE, alguns registros estariam puxando o erro para cima.
- **R²:** o Modelo 2 explica cerca de 95,5% da variação da latência. Um R² alto não significa que o modelo é perfeito: com só 12 registros de teste, outra divisão dos dados poderia dar outro valor. Por isso olhamos todas as métricas juntas.
- **AIC e BIC:** calculados pela fórmula `n·ln(SSE/n) + 2k` (AIC) e `n·ln(SSE/n) + k·ln(n)` (BIC). O Modelo 2 tem mais parâmetros e mesmo assim tem AIC e BIC menores. Ou seja, as variáveis extras (potência e perda de pacotes) melhoram o ajuste o suficiente para compensar a complexidade. O sistema escolhe automaticamente o modelo com menor BIC.

Faz sentido que a perda de pacotes aumente a latência (retransmissões) e que mais potência no transmissor ajude a reduzi-la (sinal mais forte). O gráfico real x previsto está em `graficos_ou_imagens/real_vs_previsto.png`. O usuário também pode digitar novos valores e obter uma previsão.

## 6. Priorização de alertas com heap

**Representação:** cada alerta é um dicionário com ciclo, módulo, código do sensor, status, mensagem e erro relativo. No heap ele é guardado como uma tupla `(pontuação, alerta)`.

**Critério de prioridade** (`scic/alertas.py`):

```
pontuação = prioridade x 10
          + erro relativo (%)
          + perda de pacotes x 2
          + 20 se o status for "alerta"
          + 10 se o módulo for essencial (comunicação ou suporte médico)
```

Entram no heap os registros que não estão ativos ou que têm erro relativo acima de 5%. Na base atual são 26 alertas.

**Organização** (`scic/heap.py`): implementamos um max-heap em uma lista, como visto em aula. O pai do índice `i` fica em `(i-1)//2` e os filhos em `2i+1` e `2i+2`.

- Na inserção, o alerta entra no fim da lista e sobe com **heapify-up** enquanto for maior que o pai.
- Na remoção, a raiz (o alerta mais urgente) sai, o último elemento vai para o lugar dela e desce com **heapify-down**, trocando com o maior filho.

Resultado com os 3 mais urgentes:

```
1º [ 96.36] ciclo 4 | Suporte Medico (0x1A43) | alerta | Perda de pacotes elevada | erro rel 11.96%
2º [ 94.56] ciclo 2 | Comando Orbital (0x1A10) | alerta | Queda de tensao no transmissor | erro rel 8.14%
3º [ 90.73] ciclo 4 | Comunicacao Central (0x1A04) | alerta | Perda de pacotes elevada | erro rel 6.65%
```

**Vantagem em relação a uma lista simples:** em uma lista desordenada, achar o alerta mais urgente custa O(n) a cada consulta. Manter a lista sempre ordenada custa O(n) a cada inserção. No heap, inserir e remover custam O(log n) e o mais urgente está sempre na raiz. Isso é importante porque novos alertas chegam o tempo todo.

## 7. Busca de registros com trie

**Implementação** (`scic/trie.py` e `scic/busca.py`): cada nó (`NoTrie`) tem um dicionário `filhos`, uma marcação `fim` e a lista de registros da palavra que termina nele. A trie é montada com quatro tipos de chave de cada registro, todos em minúsculas:

- o nome do módulo;
- o código do sensor;
- o tipo do módulo;
- as palavras das mensagens com mais de 3 letras.

Exemplos:

- Prefixo `com`: retorna "comunicacao" (16 registros, todos os módulos do tipo comunicação), "comunicacao central" e "comando orbital".
- Prefixo `0x1a4`: retorna os sensores cujo código começa com 0x1A4, como os do Suporte Médico (0x1A40 a 0x1A43).

**Por que trie:** a busca anda só pelas letras do prefixo. O custo depende do tamanho do prefixo (O(m)) e não do número total de registros. Depois disso, basta coletar as palavras abaixo do nó. Em uma lista, seria preciso comparar o prefixo com todos os registros. Isso deixa a trie ideal para autocomplete de comandos, módulos e códigos de sensores, que crescem conforme a colônia aumenta.

## 8. Dispositivos, bases numéricas e eletricidade básica

**Dispositivos de entrada e saída:**

- **Entrada:** sensores de latência, tensão e corrente em cada módulo, além de medidores de carga da rede. No protótipo, eles são simulados pelo arquivo CSV.
- **Saída:** o terminal (menu e relatórios), os gráficos salvos em PNG e este relatório. Em uma versão real poderia ser um painel na central de controle.
- **Interfaces (conceitual):** os sensores enviariam as leituras por rede cabeada ou Wi-Fi até a central. A Antena Redundante funcionaria como enlace de reserva.

**Bases numéricas** (`scic/eletrica.py`): os sensores são identificados por códigos em hexadecimal, que é mais compacto para identificadores de hardware. O sistema converte usando `int(codigo, 16)`, `bin()`, `oct()` e `hex()`. Exemplo com o sensor `0x1A08`:

| Base | Valor |
|---|---|
| Hexadecimal | 0x1a08 |
| Decimal | 6664 |
| Binário | 0b1101000001000 |
| Octal | 0o15010 |

**Eletricidade básica:** para o mesmo sensor (Controle de Missão, ciclo 1), com tensão de 23,85 V e corrente de 2,85 A:

- Potência: `P = V x I = 23,85 x 2,85 = 67,97 W`
- Resistência pela Lei de Ohm: `R = V / I = 8,37 Ω`
- Energia em 24 h: `67,97 W x 24 h / 1000 = 1,631 kWh`

Os módulos de comunicação têm potência média de 56,20 W, mais que o dobro dos outros tipos (17 a 27 W), porque os transmissores trabalham em 24 V. A potência também aparece no modelo de regressão como uma das variáveis que explicam a latência.

## 9. Gerenciamento inteligente da comunicação

Os resultados do SCIC mostram como os conceitos de redes inteligentes se aplicariam na Aurora Siger:

- **Sensores e medidores inteligentes:** o SCIC depende de leituras de latência, tensão, corrente e perda de pacotes por módulo e por ciclo. Em uma rede real, essas leituras viriam de medidores inteligentes (como na telemetria avançada, AMI), que enviam dados periodicamente para a central.
- **Monitoramento contínuo e detecção de anomalias:** a análise do erro relativo mostrou que Armazenamento de Dados, Suporte Médico e Habitação Alfa estão na faixa de atenção. Também tiveram ciclos acima de 10%. Com monitoramento contínuo, como em um sistema de supervisão (SCADA), essas variações seriam detectadas assim que acontecessem, e não só ao final de um ciclo.
- **Automação de decisões:** o heap já faz uma decisão automática, a ordem de atendimento. O Suporte Médico no ciclo 4 ficou em primeiro lugar por combinar módulo essencial, status de alerta, perda de pacotes alta e erro de quase 12%. Um sistema de gerenciamento avançado (ADMS) poderia usar essa fila para acionar respostas, como trocar de enlace.
- **Armazenamento de dados e redundância:** a Antena Redundante teve o menor erro relativo (2,02%), ou seja, é o enlace mais previsível da colônia. Por isso a análise final recomenda usá-la quando a Comunicação Central passar do limite. Guardar o histórico dos ciclos também permite retreinar o modelo.
- **Manutenção preditiva:** com o modelo de regressão (MAE de 11,56 ms), a equipe pode comparar a latência prevista com a observada. Quando a diferença cresce ciclo após ciclo, é sinal de desgaste, e a manutenção pode ser agendada antes da falha. A simulação de Euler ajuda a estimar quanto tempo um enlace leva para se recuperar depois de uma falha.
- **Redes inteligentes e microrredes:** a latência depende da potência do transmissor, e a energia da colônia é limitada. A comunicação e a microrrede de energia precisam ser gerenciadas juntas. Por exemplo, transmissões não essenciais podem ser adiadas em horários de carga alta, liberando energia e banda para módulos críticos.

## 10. Reflexão social, cultural e sustentável

- **Uso eficiente da comunicação e sustentabilidade:** cada transmissor de comunicação consome em média 56 W, cerca de 1,6 kWh por dia. Priorizar o que é crítico e adiar transmissões não essenciais reduz retransmissões causadas por perda de pacotes e economiza energia, que é um recurso escasso em Marte. Usar menos recursos para o mesmo resultado é uma decisão sustentável.
- **Conhecimentos tradicionais e respeito aos recursos:** muitas culturas indígenas tiram da natureza só o necessário e pensam nas próximas gerações. Essa ideia pode inspirar o gerenciamento da colônia: em vez de aumentar a potência dos transmissores sempre que a latência sobe, o sistema primeiro verifica se o problema pode ser resolvido com manutenção ou redistribuição da carga. A oralidade, forte nas tradições afro-brasileiras e indígenas, também lembra que a comunicação serve para manter a comunidade unida e passar conhecimento adiante, não só para transmitir dados.
- **Diversidade e sistemas não enviesados:** o critério de prioridade do heap foi escrito de forma explícita e mostrado ao usuário. Assim, qualquer pessoa pode questionar por que um módulo vem antes de outro. Um sistema que prioriza sem explicar pode favorecer sempre os mesmos grupos ou áreas da colônia. Uma equipe diversa ajuda a perceber esses vieses, assim como a Lei 10.639/2003 reconhece a importância de incluir histórias e saberes que antes eram deixados de lado.
- **Responsabilidade humana sobre decisões automatizadas:** o SCIC recomenda e prioriza, mas não decide sozinho. A análise final avisa que as decisões automáticas devem ser validadas pela equipe humana. O modelo tem erro médio de 11,56 ms e foi treinado com poucos dados, então pode errar em situações que nunca viu.
- **Transparência:** todas as métricas (MAE, RMSE, R², AIC, BIC) e as faixas de erro são exibidas, e não só um resultado final. Isso permite que a comunidade entenda e confie nas decisões tomadas com base nos dados.

## 11. Limitações

- A base é pequena (48 registros) e simulada. As métricas do modelo podem mudar bastante com outra divisão de treino e teste.
- A latência foi modelada como linear em relação à carga, potência e perda, o que é uma simplificação.
- Os pesos da pontuação do heap foram definidos pela equipe e não foram validados com dados reais de falhas.
- A simulação de Euler usa uma equação simples, com `k` fixo para todos os módulos.
- Não há integração real com sensores, rede ou sistemas de supervisão; tudo é conceitual ou simulado.
- Os dados são lidos de um arquivo fixo, sem atualização em tempo real.

## 12. Possíveis melhorias

- Aumentar a base com mais ciclos e usar validação cruzada para ter métricas mais confiáveis.
- Testar outros modelos e ajustar hiperparâmetros com Grid Search ou Random Search, comparando com AIC e BIC.
- Permitir cadastrar novos registros pelo menu e salvar no CSV.
- Inserir alertas no heap à medida que chegam novos registros, simulando monitoramento contínuo.
- Usar passos menores no Euler ou estimar `k` para cada módulo a partir dos dados.
- Gerar mais gráficos com Matplotlib ou Seaborn, como a latência por ciclo de cada módulo.
- Simular a troca automática para a Antena Redundante quando o erro passar de 10%.
