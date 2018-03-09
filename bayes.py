import re
import sys

class Node:
    parents = []
    name = ""
    ptable = {}
    def __init__(self, name, parents):
        self.name = name
        self.parents = parents

    def setParents(self, parents):
        self.parents = parents

    def setName(self, name):
        self.name = name

    def setProbability(self, key, probability):
        print(key + 'p:' + probability)
        self.ptable.update({key:probability})
        print(self.ptable)

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
    #nodes = inputnodes.split(',')
    for i in range(len(nodes)):
        nodes[i] = Node(nodes[i], None)
    net = Network(nodes)
    inputprobs = int(input())
    probs = []
    for i in range(inputprobs):
        probs.append(input())
        probs[i] = probs[i].replace(' ', '').replace('=', '@').replace('|', '@').split('@')
        current = net.find(str(probs[i][0][1:]))
        print("current" + str(current))
        print(str(probs[i][0][1:]))

        if len(probs[i]) > 2:
            current.setProbability(''.join(probs[i][1:-2]), probs[i][-1])
        else:
            current.setProbability(probs[i][0], probs[i][-1])


        print("local result " + str(probs[i]))
        #probs[i] = probs[i][-1].split('=')
    print(probs)
    print(probs[0][0])
    inputqueries = int(input())
    queryarr = []
    for i in range(inputqueries):
        queryarr.append(input())
    #print(queryarr)


if __name__ == "__main__":
    main()
