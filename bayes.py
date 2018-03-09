import re
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



if __name__ == "__main__":
    main()
