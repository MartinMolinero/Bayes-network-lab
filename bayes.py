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
    result = copy.deepcopy(nodes)
    for i in range(len(result)):
        result[i] = result[i].replace('+','').replace('-', '')

    for node in result:
    #for node in nodes:
        print(result)
        node = net.find(node)
        if node.parents is not None:
            for parent in node.parents:
                if not parent in result:
                    result.append(parent)
        else:
            pass
    return result


def computeProbability(query):
    print("recibe", query)
    hypothesis = query[0]
    if len(query) == 1:
        node = net.find(stringWithoutSign(hypothesis))
        if node.parents is None:
            sp = returnSingleProbability(node, hypothesis)
            return(sp)
        else:
            n = stringWithoutSign(hypothesis)
            node = net.find(n)
            sum = 0.0
            for key, value in node.ptable.items():
                if hypothesis in key:
                    a = key.split(hypothesis)[1]
                    sum += computeProbability([a])*value
            return(sum)
    elif len(query) > 1:
        node = net.find(stringWithoutSign(hypothesis))
        evidence = query[1]
        numerator = query[0].split(',')
        denominator = query[1].split(',')
        total = numerator + denominator
        print("Total", total)
        tot_with_hidden = getWithHiddenNodes(total)
        newQuery = ''.join(numerator)
        newQuery += ''.join(denominator)
        print("nq", newQuery, node.name)
        sp = returnSingleProbability(node, newQuery)
        if( sp > -1):
            print(sp)
            return(sp)
        else:
            added =list( set(tot_with_hidden) - set(total))
            print("Added", added)
            print("tot", tot_with_hidden)
            print("La puta", total)
            result = 0
            querystr = ""
            for position in total:
                node = net.find(stringWithoutSign(position))
                print("N: ",node.__dict__)
                parents = node.parents
                if(parents is None):
                    print("Parents none for", node.__dict__)
                else:
                    if node.name in position:
                        querystr += position
                    for p in parents:
                        for element in total:
                            if p in element:
                                print("found in", p, element)
                                querystr += element
                        else:
                            pass
            querystr = re.findall('[+|-][a-zA-Z0-9]*', querystr)
            #chain rule
            result += computeProbability(querystr)
            return result

            pass




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
        print(computeProbability(current))






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
