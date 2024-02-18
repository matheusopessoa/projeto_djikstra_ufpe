# Projeto de Algoritmo de Dijkstra

Este projeto implementa o algoritmo de Dijkstra para encontrar o menor caminho em um banco de dados de grafos. Ele foi desenvolvido como parte do curso de Algoritmos e Estrutura de Dados da UFPE (Sistema de Informação).

## Descrição do Projeto

O algoritmo de Dijkstra é utilizado para encontrar o menor caminho entre dois vértices em um grafo ponderado. Neste projeto, o algoritmo é aplicado a bancos de dados de grafos, onde os vértices e arestas são armazenados em um banco de dados SQLite.

### Funcionalidades Implementadas

- **Algoritmo de Dijkstra**: Implementado para encontrar o menor caminho em um grafo.
- **Interface Gráfica**: Utiliza Tkinter para criar uma interface simples para inserir os vértices de origem e destino.
- **Visualização de Grafos**: Utiliza NetworkX e Matplotlib para visualizar o grafo.

### Detalhes da Implementação

- **Automatização da Exclusão do Arquivo `grafo.db`, utilizando a biblioteca OS**: O código inclui uma função para encontrar e apagar automaticamente o arquivo `grafo.db` gerado durante a execução, evitando conflitos.
- **Mapa de Adjacências**: O grafo é representado na forma de lista de adjacências, onde cada vértice tem uma lista de seus vértices adjacentes, juntamente com os pesos das arestas.
- **Uso da Biblioteca `time`**: A biblioteca `time` é utilizada para calcular o tempo de execução do algoritmo de Dijkstra.
- **Número de Iterações do Algoritmo**: O código monitora o número de iterações realizadas pelo algoritmo de Dijkstra para encontrar o menor caminho.
- **Exibição do Menor Caminho**: O menor caminho encontrado pelo algoritmo de Dijkstra é exibido como uma lista no output, não sendo visualizado no grafo.

## Instruções de Uso

1. Clone o repositório para o seu ambiente local.
2. Certifique-se de ter as bibliotecas necessárias instaladas (especialmente `sqlite3`, `networkx`, `matplotlib` e `tkinter`).
3. Execute o arquivo principal do código (`main.py`).
4. Insira os vértices de origem e destino na interface gráfica e clique em "Calcular".
5. O menor caminho entre os vértices será calculado e exibido no output, juntamente com o número de iterações e o tempo de execução.

## Contribuição

Matheus Oliveira Pessoa e André Campos, da turma 2023.1 de Sistemas de Informação UFPE

## Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
