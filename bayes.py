import fileinput
import sys

class Node:
    def __init__(self, name, parents):
        self.name = name
        self.parents = parents

class Network:
    def __init__(self, nodes):
        self.nodes = nodes






def main():
    nodes = []
    inputnodes = input()
    print(inputnodes)
    inputnodes = inputnodes.replace(' ', '')
    nodes = inputnodes.split(',')
    for i in range(0, len(nodes)):
        auxnode = Node(nodes[i], None)
        nodes[i] = auxnode
        print(nodes[i].__dict__)
    print(nodes)
    inputprobs = int(input())
    probs = []
    for i in range(0,inputprobs):
        probs[i] = input()


if __name__ == "__main__":
    main()
