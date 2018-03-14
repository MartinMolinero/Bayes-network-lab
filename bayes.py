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

def chainRule(query):
    pass




def probability(query):

    if(query.find('|') != -1):
        print("QUE | ", query)
        query = query.split('|')
        #numerator
        hypothesis = query[0]
        hypothesis = hypothesis.split(',')
        #denominator
        evidence = query[1]
        evidence = evidence.split(',')
        intersection =  evidence + hypothesis
        intersection = ','.join(intersection)
        denominator = evidence
        denominator = ','.join(denominator)
        result = probability(intersection) / probability(denominator)
        return(result)


    else:
        print("QUE ,", query)
        query = query.split(",")
        if(len(query) > 1 ):
            #chain rule
            pass
        else:
            hypothesis = query
            print("QUERYY", hypothesis)
            node = net.find(stringWithoutSign(hypothesis[0]))
            print("my node", node.__dict__)
            # si el nodo obtenido no tiene padres
            if node.parents is None:
                #obtener singleProbability del nodo dado
                sp = returnSingleProbability(node, hypothesis[0])
                return(sp)
            else:
                #si el nodo sí tiene padres entonces hacer total probability
                n = stringWithoutSign(hypothesis[0])
                print("n", n)
                node = net.find(n)
                print("node", node.__dict__)
                sum = 0.0
                for key, value in node.ptable.items():
                    if hypothesis[0] in key:
                        a = key.split(hypothesis[0])[1]
                        print("AAAA", a)
                        sum += probability(a)*value
                return(sum)




#compute probability
def computeProbability(query):
    print("recibe", query)
    #hypothesis = primera localidad del arreglo query
    hypothesis = query[0]
    #si el query es una sola sentencia
    if len(query) == 1:
        #encuentra el nodo
        node = net.find(stringWithoutSign(hypothesis))
        # si el nodo obtenido no tiene padres
        if node.parents is None:
            #obtener singleProbability del nodo dado
            sp = returnSingleProbability(node, hypothesis)
            return(sp)
        else:
            #si el nodo sí tiene padres entonces hacer total probability
            n = stringWithoutSign(hypothesis)
            node = net.find(n)
            sum = 0.0
            for key, value in node.ptable.items():
                if hypothesis in key:
                    a = key.split(hypothesis)[1]
                    sum += computeProbability(a)*value
            return(sum)
    #si el query es mayor a un elemento i.e. ['+ill', '-test']
    elif len(query) > 1:
        #encontrar el nodo de la hipotesis
        node = net.find(stringWithoutSign(hypothesis))
        #evidence = segunda localidad
        evidence = query[1]
        # numerator = separar cada nodo contenido en la hip
        numerator = query[0].split(',')
        # denominator = separar por coma cada nodo contenido en el evidencia
        denominator = query[1].split(',')
        #total igual a un arreglo que tiene los elementos de numerator y denominator
        total = numerator + denominator
        print("Total", total)
        #tot_with_hidden igual a un arreglo que tiene los nodos de total y sus ancestros
        tot_with_hidden = getWithHiddenNodes(total)
        #armar nueva query de la concatenacion de total
        newQuery = ''.join(total)
        print("nq", newQuery, node.name)
        #hacer query de probabilidad con el nuevo query construido
        sp = returnSingleProbability(node, newQuery)
        #si encontró el query, es decir, es un nodo que tiene dicha key en el ptable
        if( sp > -1):
            #regresar sp
            return(sp)
        else:
            #added = al arreglo de la diferencia de elementos del total con ancestros y el total,
            #es decir, solo los nodos que se añadieron
            added =list( set(tot_with_hidden) - set(total))

            print("Added", added)
            print("tot", tot_with_hidden)
            print("La", total)
            #resultado = 1
            result = 1
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
        #current = q.split('|')
        print(probability(q))






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
