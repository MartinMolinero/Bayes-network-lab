import re
import copy
import sys
from decimal import Decimal

#define the node class, with its ptable, parents and name
class Node:
    parents = []
    name = ""
    ptable = {}
    def __init__(self, name, parents):
        self.name = name
        self.parents = parents
        self.ptable = {}

    #set parents of a node = a receiving list
    def setParents(self, parents):
        for i in range(len(parents)):
            parents[i] = parents[i].replace('+', '').replace('-', '')
        self.parents = parents

    #set node name
    def setName(self, name):
        self.name = name
    #set node probability
    def setProbability(self, key, probability):
        probability = float(probability)
        self.ptable.update({key:probability})
    #return ptable value given key
    def getProbability(self, key):
        if (self.ptable.get(str(key))):
            return self.ptable.get(str(key))
        else:
            return -1
    #return all probability table
    def getProbabilityTable(self):
        return self.ptable
    #return parents
    def getParents(self):
        return self.parents




#define a network class with a list of nodes
class Network:
    nodes = []
    def __init__(self, nodes):
        self.nodes = nodes

    def find(self, name):
        for node in self.nodes:
            if node.name == str(name):
                return node

#return a string without sign
def stringWithoutSign(string):
    return string[1:]

#receives a list of nodes and returns a set having those nodes and possible ancestors
def getWithHiddenNodes(nodes):
    result = copy.deepcopy(nodes)
    for i in range(len(result)):
        result[i] = result[i].replace('+','').replace('-', '')

    for node in result:
        print(result)
        node = net.find(node)
        if node.parents is not None:
            for parent in node.parents:
                if not parent in result:
                    result.append(parent)
        else:
            pass
    return result

def conditional(query):
    print("CONDITIONAL QUERY", query)
    query = query.split('|')
    hypothesis = query[0]
    evidence = query[1]
    print("QUERY", query, "HYP", hypothesis, "EVI", evidence)
    total = evidence + hypothesis
    print("TOTAL", total)
    upper = hypothesis + "," + evidence
    print("UPPER", upper, "EVIDENCE", evidence)
    result = newComputeProbability(upper) / newComputeProbability(evidence)
    return result

def totalProbability(query):
    node_name = stringWithoutSign(query)
    node = net.find(node_name)
    sum = 0.0
    for key, value in node.ptable.items():
        if query in key:

            a = key.split(query)[1]
            print("KEY", key, "A", a,  "QUERY", query)
            sum += newComputeProbability(a)*value
    return(sum)


def chainRule(query):
    query_array = query.split(',')

    pass

def newComputeProbability(query):
    print("Thequery", query)
    query_array = query.split(',')
    unsigned = []
    if(len(query_array) > 1 ):
        #generatequeries
        #sum(chainRule(current_query))
        for prob in query_array:
            if(prob.find('+') == -1 and prob.find('-') == -1):
                unsigned.append(prob)
        if (not unsigned):
            node = net.find(stringWithoutSign(query_array[0]))
            new_query = ''.join(query).replace(',', '')
            print("Encuentra el nodo con", node.__dict__, new_query)
            sp = returnSingleProbability(node, new_query)
            print("SP", sp)
            return(sp)
        else:
            #chain rule
            tot_with_hidden = getWithHiddenNodes(query)
            added =list( set(tot_with_hidden) - set(query))
        pass
    else:
        query_probability = str(query_array[0])
        node_name = stringWithoutSign(query_probability)
        node = net.find(node_name)
        print("NODE NAME, NODE", node_name, node.__dict__)
        if(node.parents is None):
            #get direct probability from ptable
            sp = returnSingleProbability(node, query_probability)
            print("ENTERED AND SHOULD RETURN", sp)
            return(sp)
        else:
            #total probability
            #si el nodo sí tiene padres entonces hacer total probability
            cp = totalProbability(query_probability)
            return(cp)




def returnSingleProbability(node, string):
    p = node.getProbability(string)
    return p

def processQueries():
    inputqueries = int(input())
    queryarr = []
    for i in range(inputqueries):
        a= input()
        queryarr.append(a)
    current = []
    for q in queryarr:
        current = q.split('|')
        print("\nCURRENT QUERY", current)
        if (len(current) > 1):
            current = '|'.join(current)
            prob = conditional(current)
        else:
            current = str(current[0])
            prob = newComputeProbability(current)
        print(prob)

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
        for node in net.nodes:
            print(node.__dict__)
    processQueries()



if __name__ == "__main__":
    main()
