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






class Network:
    nodes = []
    def __init__(self, nodes):
        self.nodes = nodes

    def find(self, name):
        for node in self.nodes:
            if node.name == name:
                return node





def main():
    nodes = []
    inputnodes = input()
    print(inputnodes)
    nodes = inputnodes.replace(' ', '').split(',')
    #nodes = inputnodes.split(',')
    for i in range(len(nodes)):
        nodes[i] = Node(nodes[i], None)
        print(nodes[i].__dict__)
    print(nodes)

    inputprobs = int(input())
    probs = []
    for i in range(inputprobs):

        probs.append(input())
        probs[i] = probs[i].replace(' ', '').replace('=', '@').replace('|', '@').split('@')
        #if len(probs[i]) > 0:

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
