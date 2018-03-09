import fileinput
import sys

class Node:
    def __init__(self, name, parents):
        self.name = name
        self.parents = parent

class Network:
    def __init__(self, nodes):
        self.nodes = nodes






def main():
    nodes = []
    inputnodes = sys.stdin.readline().rstrip()
    inputnodes = inputnodes.replace(' ', '')
    nodes = inputnodes.split(',')
    for node in nodes:
        
    print(nodes)
    inputprobs = int(sys.stdin.readline().rstrip())
    print("probs" + str(inputprobs))
    for i in range(0,inputprobs):


if __name__ == "__main__":
    main()
