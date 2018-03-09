import fileinput
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
    inputnodes = inputnodes.replace(' ', '')
    nodes = inputnodes.split(',')
    for i in range(0, len(nodes)):
        nodes[i] = Node(nodes[i], None)
        print(nodes[i].__dict__)
    net = Network(nodes)
    print(net.__dict__)
    inputprobs = int(input())
    probs = []
    for i in range(0,inputprobs):
        probs.append(input())

    inputqueries = int(input())
    queryarr = []
    for i in range(inputqueries):
        queryarr.append(input())
    #print(queryarr)


if __name__ == "__main__":
    main()
