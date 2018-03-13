import re
import copy
import sys
from decimal import Decimal

class Node:
    parents = []
    name = ""
    ptable = {}
    def __init__(self, name, parents):
        self.name = name
        self.parents = parents
        self.ptable = {}

    def setParents(self, parents):
        for i in range(len(parents)):
            parents[i] = parents[i].replace('+', '').replace('-', '')
        #checar esto, puede que después sobreescriba la lista de padres, preferiría tener un append a self parents
        #y que cada padre se agregara en el for de arriba a menos que ya esté antes
        self.parents = parents


    def setName(self, name):
        self.name = name

    def setProbability(self, key, probability):
        probability = float(probability)
        self.ptable.update({key:probability})

    def getProbability(self, key):
        if (self.ptable.get(str(key))):
            return self.ptable.get(str(key))
        else:
            return -1

    def getProbabilityTable(self):
        return self.ptable

    def getParents(self):
        return self.parents






class Network:
    nodes = []
    def __init__(self, nodes):
        self.nodes = nodes

    def find(self, name):
        for node in self.nodes:
            if node.name == str(name):
                return node

def stringWithoutSign(string):
    return string[1:]

def getWithHiddenNodes(nodes):
    result = nodes
    for i in range(len(result)):
        result[i] = result[i].replace('+','').replace('-', '')
    for node in result:
    #for node in nodes:
        node = net.find(node)
        if node.parents is not None:
            for parent in node.parents:
                if not parent in result:
                    result.append(parent)
        else:
            pass
    return result


def computeProbability(query):
    print("Q", query)
    hypothesis = query[0]
    if len(query) == 1:
        node = net.find(stringWithoutSign(hypothesis))
        if node.parents is None:
            sp = returnSingleProbability(node, hypothesis)
            return(sp)
        else:
            n = [stringWithoutSign(hypothesis)]
            #total_nodes = getWithHiddenNodes(n)
            print("query actual", query)
            #compute total probability
            result = 0.0


            return result





    elif len(query) > 1:
        node = net.find(stringWithoutSign(hypothesis))
        evidence = query[1]
        numerator = query[0].split(',')
        denominator = query[1].split(',')
        total = numerator + denominator
        tot_with_hidden = getWithHiddenNodes(total)
        print("DICK", tot_with_hidden)
        newQuery = ''.join(numerator)
        newQuery += ''.join(denominator)
        print("Node", node.__dict__)
        print("newQuery", newQuery)

        sp = returnSingleProbability(node, newQuery)
        if( sp > -1):
            print(sp)
        else:

            pass



def returnSingleProbability(node, string):
    p = node.getProbability(string)
    return p

def processQueries():
    inputqueries = int(input())
    queryarr = []
    for i in range(inputqueries):
        a= input()
        a = a.replace(',', '')
        queryarr.append(a)
    print(queryarr)
    current = []
    for q in queryarr:
        current = q.split('|')
        computeProbability(current)






def main():
    #arreglo de nodos vacío
    nodes = []
    #leer nodos de input
    inputnodes = input()
    #limpiar el input y separar los nodos por coma
    nodes = inputnodes.replace(' ', '').split(',')
    #para cada estructura en el arreglo local, crear estructura de datos nodo
    for i in range(len(nodes)):
        #crear un nodo sólo con su nombre
        nodes[i] = Node(nodes[i], None)
    #crear la red con los nodos preeliminares
    global net
    net = Network(nodes)
    #preparación para leer los nodos del input
    inputprobs = int(input())
    #arreglo de probabilidades
    probs = []
    #leer cada probabilidad por separado
    for i in range(inputprobs):
        #leer de input
        probs.append(input())
        #procesarla
        probs[i] = probs[i].replace(' ', '').replace('=', '@').replace('|', '@').split('@')
        #quité el deepcopy porque lo que necesitabamos era que sí hiciera los cambios en la estructura net,
        #si dejábamos deepcopy sólo hacía el cambio en una variable local, la tabla de probs ya se hace bien de acuerdo a los inputprobs
        #buscar el nodo actual que se insertó en la probabilidad dentro de la network
        current = net.find(str(probs[i][0][1:]))
        #si es una probabilidad con padres
        if len(probs[i]) > 2:
            #concatenar el string con los nombres de nodos con ''.join...
            string = ''.join(probs[i][0:-1])
            string = string.replace(',','')
            #sort alfabeticamente
            #igualar ese string a nuestro hash de probabilidades con la probabilidad dada en el input
            current.setProbability(string, probs[i][-1])
            if (string[0] == '+'):
                current.setProbability('-' + string[1:],'%.7f'%(Decimal('1') - Decimal(str(current.getProbability(string)))))
            else:
                current.setProbability('+' + string[1:],'%.7f'%(Decimal('1') - Decimal(str(current.getProbability(string)))))
            #asignar los padres al nodo
            current.setParents(probs[i][1:-1][0].split(','))


        else:
        #si es una probabilidad sencilla (sin padres)
            #construye su probabilidad dada
            current.setProbability(probs[i][0], probs[i][-1])
            #asignar la probabilidad a su complemento, 1- prob dada anterior
            string = ''.join(probs[i][0:-1])
            if (string[0] == '+'):
                current.setProbability('-' + string[1:],'%.7f'%(Decimal('1') - Decimal(str(current.getProbability(string)))))
            else:
                current.setProbability('+' + string[1:],'%.7f'%(Decimal('1') - Decimal(str(current.getProbability(string)))))
    processQueries()



if __name__ == "__main__":
    main()
