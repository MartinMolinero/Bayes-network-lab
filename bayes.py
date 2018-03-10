import re
import copy
import sys

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
            print(parents[i])
        self.parents = parents

    def setName(self, name):
        self.name = name

    def setProbability(self, key, probability):
        probability = float(probability)
        self.ptable.update({key:probability})

    def getProbability(self, key):
        return self.ptable.get(str(key))

    def getProbabilityTable():
        return self.ptable;





class Network:
    nodes = []
    def __init__(self, nodes):
        self.nodes = nodes

    def find(self, name):
        for node in self.nodes:
            if node.name == str(name):
                return node





def main():
    nodes = []
    inputnodes = input()
    nodes = inputnodes.replace(' ', '').split(',')
    for i in range(len(nodes)):
        nodes[i] = Node(nodes[i], None)
    net = Network(nodes)
    inputprobs = int(input())
    probs = []
    for i in range(inputprobs):
        probs.append(input())
        probs[i] = probs[i].replace(' ', '').replace('=', '@').replace('|', '@').split('@')
        current = copy.deepcopy(net.find(str(probs[i][0][1:])))
        if len(probs[i]) > 2:
            current.setProbability(''.join(probs[i][0:-1]), probs[i][-1])
            current.setParents(probs[i][1:-1][0].split(','))
            print(current.__dict__)
        else:
            current.setProbability(probs[i][0], probs[i][-1])
            current.setProbability('-' + str(probs[i][0][1:]),1 - current.getProbability(probs[i][0]))
        print(current.__dict__)
    inputqueries = int(input())
    queryarr = []
    for i in range(inputqueries):
        queryarr.append(input())
    #print(queryarr)


if __name__ == "__main__":
    main()
