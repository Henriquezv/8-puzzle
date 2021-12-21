from collections import deque

import heapq

import time

class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """
    def __init__(self, estado, pai, acao, custo, custoHeuristico = 0):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo
        self.custoHeuristico = custoHeuristico

    # Utilizado para comparação na fila de prioridades
    def __lt__(self, secondNode):
        return self.custoHeuristico < secondNode.custoHeuristico

    def debug(self):
        print('Pai: ' + self.pai.estado)
        print('Acao: ' + self.acao)
        print('Estado: ' + self.estado)
        print('Custo: ' + str(self.custo))

def getPlayerPosition(estado):
    return estado.index('_')

def generateChunks(estado):
    estado = list(estado)
    return estado[0:3], estado[3:6], estado[6:9]

def getChunksAsAList(estado):
    firstChunk, secondChunk, thirdChunk = generateChunks(estado)
    return firstChunk + secondChunk + thirdChunk

def upwardMove(estado):
    playerPosition = getPlayerPosition(estado)
    listOfChunks = getChunksAsAList(estado)
        
    auxiliarList = listOfChunks
    auxiliarList[playerPosition], auxiliarList[playerPosition - 3] = auxiliarList[playerPosition - 3], auxiliarList[playerPosition]
    result = "".join(auxiliarList)

    return result

def downwardMove(estado):
    playerPosition = getPlayerPosition(estado)
    listOfChunks = getChunksAsAList(estado)
        
    auxiliarList = listOfChunks
    auxiliarList[playerPosition], auxiliarList[3 + playerPosition] = auxiliarList[3 + playerPosition], auxiliarList[playerPosition]
    result = "".join(auxiliarList)

    return result

def rightMove(estado):
    playerPosition = getPlayerPosition(estado)
    listOfChunks = getChunksAsAList(estado)
        
    auxiliarList = listOfChunks
    auxiliarList[playerPosition], auxiliarList[1 + playerPosition] = auxiliarList[1 + playerPosition], auxiliarList[playerPosition]
    result = "".join(auxiliarList)

    return result

def leftMove(estado):
    playerPosition = getPlayerPosition(estado)
    listOfChunks = getChunksAsAList(estado)
        
    auxiliarList = listOfChunks
    auxiliarList[playerPosition], auxiliarList[playerPosition - 1] = auxiliarList[playerPosition - 1], auxiliarList[playerPosition]
    result = "".join(auxiliarList)

    return result

def sucessor(estado):
    """
    Recebe um estado (string) e retorna uma lista de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """

    position = getPlayerPosition(estado)

    solutions = []

    if(position == 0):
        solutions.append(('direita', rightMove(estado)))
        solutions.append(('abaixo', downwardMove(estado))) 
    elif(position == 1):
        solutions.append(('esquerda', leftMove(estado)))
        solutions.append(('abaixo', downwardMove(estado))) 
        solutions.append(('direita', rightMove(estado)))
    elif(position == 2):
        solutions.append(('esquerda', leftMove(estado)))
        solutions.append(('abaixo', downwardMove(estado)))                  
    elif(position == 3):
        solutions.append(('acima', upwardMove(estado)))
        solutions.append(('direita', rightMove(estado)))
        solutions.append(('abaixo', downwardMove(estado)))  
    elif(position == 4):
        solutions.append(('esquerda', leftMove(estado)))
        solutions.append(('acima', upwardMove(estado)))
        solutions.append(('direita', rightMove(estado)))
        solutions.append(('abaixo', downwardMove(estado)))   
    elif(position == 5):
        solutions.append(('esquerda', leftMove(estado)))
        solutions.append(('acima', upwardMove(estado)))
        solutions.append(('abaixo', downwardMove(estado)))                     
    elif(position == 6):
        solutions.append(('acima', upwardMove(estado)))
        solutions.append(('direita', rightMove(estado)))
    elif(position == 7):
        solutions.append(('esquerda', leftMove(estado)))
        solutions.append(('acima', upwardMove(estado)))
        solutions.append(('direita', rightMove(estado)))
    elif(position == 8):
        solutions.append(('esquerda', leftMove(estado)))
        solutions.append(('acima', upwardMove(estado))) 
    else:
        pass

    return solutions

def expande(nodo):
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um iterable de nodos.
    Cada nodo do iterable é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
    sucessores = sucessor(nodo.estado)
    nodelist = []

    for item in sucessores:
        newNode = Nodo(item[1], nodo, item[0], nodo.custo + 1)
        nodelist.append(newNode)

    return nodelist

def getDescendants(nodo):
    solutions = []

    while(True):
        if(nodo.pai == None):
            break
        else:
            solutions.append(nodo)
            nodo = nodo.pai

    return solutions

def fronteiraIsEmpty(fronteira):
    return len(fronteira) == 0

def bfs(estado):
    # Cria o conjunto de explorados e uma fila
    explorados = set()
    fronteira = deque([Nodo(estado, None, '', 0)])

    while(True):
        if(fronteiraIsEmpty(fronteira)):
            break

        nodo = fronteira.popleft()

        if(nodo.estado == '12345678_'):
            return getDescendants(nodo)

        if(nodo.estado not in explorados):
            explorados.add(nodo.estado)

            vizinhanca = expande(nodo)
            for vizinho in vizinhanca:
                fronteira.append(vizinho)

    return None

def dfs(estado):
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """

    # Cria o conjunto de explorados e uma fila
    explorados = set()
    fronteira = deque([Nodo(estado, None, '', 0)])

    while(True):
        if(fronteiraIsEmpty(fronteira)):
            break

        nodo = fronteira.pop()
        
        if(nodo.estado == '12345678_'):
            return getDescendants(nodo)

        
        if(nodo.estado not in explorados):
            explorados.add(nodo.estado)

            vizinhanca = expande(nodo)
            for vizinho in vizinhanca:
                fronteira.append(vizinho)

    return None

def hammingDistance(estado):
    h = 0
    estadoFinal = "12345678_"
        
    for x in range(9):
        if(estado[x] == '_'):
            pass
        else:
            if(estado[x] != estadoFinal[x]):
                h += 1
    
    return h

def isSolvable(estado):
    count = 0
    estado = list(estado)

    for i in range(8):
        for j in range(i + 1, 9):
                if estado[j] != '_' and estado[i] != '_' and estado[i] > estado[j]:
                    count += 1

    return count % 2 == 0

def astar_hamming(estado):
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """

    if(isSolvable(estado)):
        explorados = set()

        custoHeuristico = hammingDistance(estado)
        fronteira = [Nodo(estado, None, '', 0, custoHeuristico)]
        
        while(True):

            if(fronteiraIsEmpty(fronteira)):
                break

            #heapq.heapify(fronteira)
            #nodo = heapq.heappop(fronteira)
            fronteira.sort(key = lambda nodo: nodo.custoHeuristico) 
            nodo = fronteira.pop(0)

            if(nodo.estado == '12345678_'):
                return getDescendants(nodo)
            
            if(nodo.estado not in explorados):
                explorados.add(nodo.estado)

                vizinhanca = expande(nodo)
                for vizinho in vizinhanca:
                    vizinho.custoHeuristico = vizinho.custo + hammingDistance(vizinho.estado)
                    fronteira.append(vizinho)
    else:
        return None
'''
def manhattanDistance(estado):
    pass
'''

'''
initial_state = [8,1,3,4,0,2,7,6,5]
goal_state = [1,2,3,4,5,6,7,8,0]
def calculateManhattan(initial_state):
    
    initial_config = initial_state
    manDict = 0
    delta = 0
    for i,item in enumerate(initial_config):
        if(item == 0):
            pass
        else:
            prev_row,prev_col = int(i/3) , i % 3
            goal_row,goal_col = int(item/3),item % 3
            delta = abs(prev_row-goal_row) + abs(prev_col - goal_col)

            manDict += delta
            print(i, item, delta)
            print(prev_row, prev_col)
            print(goal_row, goal_col)
            break
    return manDict
''' 
#print(calculateManhattan(initial_state))
def manhattanDistance(estado):
    dict_dist = {0 : {'1': 0, '2': 1, '3': 2, '4': 1, '5': 2, '6': 3, '7': 2, '8': 3},
              1: {'1': 1, '2': 0, '3': 1, '4': 2, '5': 1, '6': 2, '7': 3, '8': 2},
              2: {'1': 2, '2': 1, '3': 0, '4': 3, '5': 2, '6': 1, '7': 4, '8': 3},
              3: {'1': 1, '2': 2, '3': 3, '4': 0, '5': 1, '6': 2, '7': 1, '8': 2},
              4: {'1': 2, '2': 1, '3': 2, '4': 1, '5': 0, '6': 1, '7': 2, '8': 1},
              5: {'1': 3, '2': 2, '3': 1, '4': 2, '5': 1, '6': 0, '7': 3, '8': 2},
              6: {'1': 2, '2': 3, '3': 4, '4': 1, '5': 2, '6': 3, '7': 0, '8': 1},
              7: {'1': 3, '2': 2, '3': 3, '4': 2, '5': 1, '6': 2, '7': 1, '8': 0},
              8: {'1': 4, '2': 3, '3': 2, '4': 3, '5': 2, '6': 1, '7': 2, '8': 1},
              }
    h = 0
    estadoFinal = "12345678_"
        
    for x in range(8):
        if(estado[x] == '_'):
            pass
        else:
            h += dict_dist[x][estado[x]]
    
    return h

def astar_manhattan(estado):
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    if(isSolvable(estado)):
        explorados = set()

        custoHeuristico = manhattanDistance(estado)
        print(custoHeuristico)
        fronteira = [Nodo(estado, None, '', 0, custoHeuristico)]
        
        while(True):

            if(fronteiraIsEmpty(fronteira)):
                break

            #heapq.heapify(fronteira)
            #nodo = heapq.heappop(fronteira)
            fronteira.sort(key = lambda nodo: nodo.custoHeuristico)
            nodo = fronteira.pop(0)

            if(nodo.estado == '12345678_'):
                return getDescendants(nodo)

            if(nodo.estado not in explorados):
                explorados.add(nodo.estado)

                vizinhanca = expande(nodo)
                for vizinho in vizinhanca:
                    vizinho.custoHeuristico = vizinho.custo + manhattanDistance(vizinho.estado)
                    fronteira.append(vizinho)
    else:
        return None


