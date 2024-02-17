#MAIN

import sqlite3
import math
import random
import time
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import os

def encontrar_e_apagar_arquivo(nome_pasta, nome_arquivo):
    if not os.path.isdir(nome_pasta):
        return
    for root, dirs, files in os.walk(nome_pasta):
        if nome_arquivo in files:
            arquivo = os.path.join(root, nome_arquivo)
            os.remove(arquivo)
            return


nome_pasta = r'C:\Users\USER\Documents\proj_alg\projeto_djikstra_ufpe\bancos_de_dados'
nome_arquivo = 'grafo.db'
encontrar_e_apagar_arquivo(nome_pasta, nome_arquivo)


class HeapMin:
    """
    Implementação de uma estrutura de Heap Mínima.
    """
    def __init__(self):
        self.tamanho = 0
        self.heap = []

    def adiciona_no(self, valor, indice):
        """
        Adiciona um nó ao heap.
        """
        self.heap.append([valor, indice])
        self.tamanho += 1
        corrente = self.tamanho
        while True:
            if corrente == 1:
                break
            pai = corrente // 2
            if self.heap[pai - 1][0] <= self.heap[corrente - 1][0]:
                break
            else:
                self.heap[pai - 1], self.heap[corrente - 1] = self.heap[corrente - 1], self.heap[pai - 1]
                corrente = pai

    def mostrar_heap(self):
        """
        Mostra a estrutura atual do heap.
        """
        print('A estrutura do heap é a seguinte:')
        nivel = int(math.log(self.tamanho, 2))
        corrente = 0
        for i in range(nivel):
            for j in range(2 ** i):
                print(f'{self.heap[corrente]}', end='  ')
                corrente += 1
            print('')
        for i in range(self.tamanho - corrente):
            print(f'{self.heap[corrente]}', end='  ')
            corrente += 1
        print('')

    def remove_no(self):
        """
        Remove o nó com menor valor do heap.
        """
        menor_no = self.heap[0]
        self.heap[0] = self.heap[self.tamanho - 1]
        self.heap.pop()
        self.tamanho -= 1
        corrente = 1
        while True:
            filho = 2 * corrente
            if filho > self.tamanho:
                break
            if filho + 1 <= self.tamanho:
                if self.heap[filho][0] < self.heap[filho - 1][0]:
                    filho += 1
            if self.heap[corrente - 1][0] <= self.heap[filho - 1][0]:
                break
            else:
                self.heap[corrente - 1], self.heap[filho - 1] = self.heap[filho - 1], self.heap[corrente - 1]
                corrente = filho

        return menor_no

    def tamanho_heap(self):
        """
        Retorna o número de nós no heap.
        """
        return self.tamanho

    def menor_elemento(self):
        """
        Retorna o nó com o menor valor no heap.
        """
        if self.tamanho != 0:
            return self.heap[0]
        return 'O heap está vazio'

    def filho_esquerda(self, indice):
        """
        Retorna o filho esquerdo de um nó.
        """
        if self.tamanho >= 2 * indice:
            return self.heap[2 * indice - 1]
        return 'Esse nó não tem filho'

    def filho_direita(self, indice):
        """
        Retorna o filho direito de um nó.
        """
        if self.tamanho >= 2 * indice + 1:
            return self.heap[2 * indice]
        return 'Esse nó não tem filho à direita'

    def pai(self, indice):
        """
        Retorna o pai de um nó.
        """
        return self.heap[indice // 2]

class Grafo:
    """
    Implementação de um Grafo com o algoritmo de Dijkstra.
    """
    def __init__(self):
        self.vertices = {}
        self.num_vertices = 0

    def adicionar_aresta(self, vertice_origem, vertice_destino, peso):
        """
        Adiciona uma aresta ao grafo.
        """
        if vertice_origem not in self.vertices:
            self.vertices[vertice_origem] = []
            self.num_vertices += 1
        if vertice_destino not in self.vertices:
            self.vertices[vertice_destino] = []
            self.num_vertices += 1
        self.vertices[vertice_origem].append((vertice_destino, peso))
        self.vertices[vertice_destino].append((vertice_origem, peso))

    def mostrar_grafo(self):
        """
        Mostra o grafo na forma de lista de adjacências.
        """
        print('O grafo na forma de lista de adjacências é:')
        for vertice in self.vertices:
            print(vertice, "->", self.vertices[vertice])

    def dijkstra(self,origem,destino):
        """
        Algoritmo de Dijkstra para encontrar os caminhos mais curtos a partir de um vértice de origem.
        """

        custo_vem = [[-1, 0] for _ in range(self.num_vertices)]
        custo_vem[origem - 1] = [0, origem]
        heap = HeapMin()
        heap.adiciona_no(0, origem)
        visitados = set()  # Conjunto para manter os vértices visitados
        iterações = 0
        inicio = time.time()
        while heap.tamanho_heap() > 0:
            iterações += 1
            dist, vertice = heap.remove_no()
            if vertice in visitados:  # Verifica se o vértice já foi visitado
                continue
            visitados.add(vertice)  # Marca o vértice como visitado
            if self.vertices.get(vertice) is None:
                continue
            for adjacente, peso in self.vertices[vertice]:
                if custo_vem[adjacente - 1][0] == -1 or custo_vem[adjacente - 1][0] > dist + peso:
                    custo_vem[adjacente - 1] = [dist + peso, vertice]
                    heap.adiciona_no(dist + peso, adjacente)
        fim = time.time()
        messagebox.showinfo("Resultado",f"Número de iterações: {iterações}\nTempo gasto: {fim - inicio}segundos")

        return custo_vem[destino - 1][0]  # Retorna o custo mínimo para o destino
    
    def printar_menor_caminho(custo_vem, origem, destino):
        caminho = []
        atual = destino
        while atual != origem:
            caminho.append(atual)
            atual = custo_vem[atual - 1][1]
        caminho.append(origem)
        caminho.reverse()
        print("Menor caminho de", origem, "a", destino, ":", caminho)

    def carregar_de_banco_de_dados(self, arquivo_banco):
        """
        Carrega o grafo a partir de um banco de dados SQLite.
        """
        conexao = sqlite3.connect(arquivo_banco)
        cursor = conexao.cursor()

        cursor.execute("SELECT vertice_origem, vertice_destino, peso FROM arestas")
        arestas = cursor.fetchall()
        for origem, destino, peso in arestas:
            self.adicionar_aresta(origem, destino, peso)

        conexao.close()


def criar_banco_de_dados(arquivo_banco):
    conexao = sqlite3.connect(arquivo_banco)
    cursor = conexao.cursor()

    cursor.execute("CREATE TABLE arestas (origem INTEGER, destino INTEGER, peso REAL)")

    conexao.commit()
    conexao.close()

def preencher_banco_de_dados(arquivo_banco, arquivo_edges):
    with open(arquivo_banco, 'w') as db:
        # Inicialize o banco de dados SQLite
        conexao = sqlite3.connect(db.name)
        cursor = conexao.cursor()

        # Crie a tabela de arestas
        cursor.execute('''CREATE TABLE IF NOT EXISTS arestas (
                            vertice_origem INTEGER,
                            vertice_destino INTEGER,
                            peso REAL
                          )''')

        # Abra o arquivo de arestas e insira os dados no banco de dados
        with open(arquivo_edges, 'r') as f:
            for linha in f:
                # Divida a linha em partes
                partes = linha.split()
                if len(partes) == 2:
                    vertice_origem, vertice_destino = partes
                    # Atribua um peso aleatório
                    peso = round(random.uniform(1, 10), 2)  # Arredonda para 2 casas decimais
                    # Verifique se os valores são dígitos antes de convertê-los
                    if vertice_origem.isdigit() and vertice_destino.isdigit():
                        cursor.execute("INSERT INTO arestas VALUES (?, ?, ?)",
                                       (int(vertice_origem), int(vertice_destino), peso))
                    else:
                        print("Ignorando linha com valores não numéricos:", linha)
                else:
                    print("Ignorando linha com formato inválido:", linha)

        # Salve as alterações e feche a conexão com o banco de dados
        conexao.commit()
        conexao.close()
class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Algoritmo de Dijkstra")
        
        self.label_origem = tk.Label(master, text="Vértice de origem:")
        self.label_origem.grid(row=0, column=0, padx=5, pady=5)
        self.entry_origem = tk.Entry(master)
        self.entry_origem.grid(row=0, column=1, padx=5, pady=5)
        
        self.label_destino = tk.Label(master, text="Vértice de destino:")
        self.label_destino.grid(row=1, column=0, padx=5, pady=5)
        self.entry_destino = tk.Entry(master)
        self.entry_destino.grid(row=1, column=1, padx=5, pady=5)
        
        self.button_calcular = tk.Button(master, text="Calcular", command=self.calcular_dijkstra)
        self.button_calcular.grid(row=2, columnspan=2, padx=5, pady=5)
        
    def calcular_dijkstra(self):
        origem = self.entry_origem.get()
        destino = self.entry_destino.get()
        
        try:
            origem = int(origem)
            destino = int(destino)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira números inteiros para origem e destino.")
            return
        
        if origem <= 0 or destino <= 0:
            messagebox.showerror("Erro", "Os vértices devem ser números positivos.")
            return
        
        arquivo_banco = r"C:\Users\USER\Documents\proj_alg\projeto_djikstra_ufpe\bancos_de_dados\grafo.db"
        criar_banco_de_dados(arquivo_banco)

        #arquivo_edges = r"C:\dev\git-projects\projeto_djikstra_ufpe\bancos_de_dados\test.edges"
        arquivo_edges = r"C:\Users\USER\Documents\proj_alg\projeto_djikstra_ufpe\bancos_de_dados\inf-euroroad.edges" 
        preencher_banco_de_dados(arquivo_banco, arquivo_edges)

        grafo = Grafo()  # Criando uma instância da classe Grafo
        # Adicione aqui suas chamadas de métodos para adicionar arestas ao grafo
        grafo.carregar_de_banco_de_dados(arquivo_banco)
        grafo.mostrar_grafo()
        # Chamada do método Dijkstra
        custo=grafo.dijkstra(origem,destino)
        print("Esee foi o custo:",custo)
        #grafo.printar_menor_caminho(custo, origem, destino)

        #Desenho dos Grafos
        G = nx.Graph()
        for vertice in grafo.vertices:
            for adjacente, peso in grafo.vertices[vertice]:
                G.add_edge(vertice, adjacente, weight=peso)

        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw(G, pos, with_labels=True, node_size=70, node_color='skyblue')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.show()
    

root = tk.Tk()
gui = GUI(root)
root.mainloop()
