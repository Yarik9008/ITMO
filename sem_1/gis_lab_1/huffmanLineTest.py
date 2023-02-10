from huffmanDecode import main
import pickle

from queue import PriorityQueue
from prettytable import PrettyTable
from argparse import ArgumentParser

from dataclasses import dataclass, field
from typing import Any



# Class that helps to bypass the error of comparing incompatible types
# (With the same value, priority PriorityQueue starts comparing the contents of elements. Which leads to an error)
@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)


# Class describing a node of a binary tree
class Node():
    def __init__(self, left=None, right=None, root=None):
        self.left = left
        self.right = right
        self.root = root
    
    # Method that returns the node's children
    # Out:
    #   leftChildren, rightChildren
    def getCildren(self):
        return self.left, self.right


# Class that counts the number of occurrences of characters in a string
# collections.Counter is not suitable because it is case-insensitive
class Counter():
    def __init__(self, string):
        self.string = string
        self.mostCommonDict()

    def mostCommonDict(self):
        symbols = set(self.string)
        self.common = {}
        for i in symbols:
            self.common[i] = self.string.count(i)

        self.common = { elem[0]:elem[1] for elem in sorted(self.common.items(), key=lambda kv: kv[1], reverse=True) }
        
        return self.common

    def mostCommon(self):
        return ( (i, self.common[i]) for i in self.common)

    def __str__(self):
        return f"Counter({self.common})"


# Function that creates a binary Huffman tree
# In:
#   list mostCommon (In the format: (priority, letter))
def createTree(mostCommon):
    queue = PriorityQueue()
    
    # We fill the queue with characters
    for value in mostCommon:
        queue.put(PrioritizedItem(*value))

    
    # Sorting through the queue elements. 
    # First of all, the elements with the lowest priority value are taken
    # That is, the tree is filled from the bottom up
    while queue.qsize() > 1:                     
        left = queue.get()
        right = queue.get() 
         

        # Adding the node containing the elements with the lowest priority to the queue
        # Priority of a node is the sum of priorities of its children  
        node = Node(left, right)
        
        queue.put(PrioritizedItem(left.priority + right.priority, node))            

    return queue.get()  


# We make a table of codes
# In:
#   Node node, str prefix, dict code
# Out:
#   Node node
def walkTree(node, prefix="", code={}):
    if isinstance(node.left.item, Node):
        walkTree(node.left.item ,prefix + "0", code)

    else:
        code[node.left.item] = prefix + "0"

    if isinstance(node.right.item, Node):
        walkTree(node.right.item, prefix + "1", code)

    else:
        code[node.right.item] = prefix + "1"

    return(code)


# Function that converts a string containing a binary character code into bytes
# In:
#   str bitString
# Out:
#   byte bitString
def bitStringToBytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')


def main():
    # Config
    printTable = True
    printEncodedLine = True

    sortedByLen = True
    sortedByCount = False


    # Argument parser
    parser = ArgumentParser(description='Encode and decode a text line using the Huffman algorithm')
    parser.add_argument('line', type=str, help='Input line')
    args = parser.parse_args()

    #inputString = "It's wednesday, my dudes!"

    inputData = args.line


    th = ["Symbol", "Count", "Code"]
    td = []


    # Flipping the dictionary to bring it to the format accepted by Priority Queue
    mostCommon = [ (elem[1] , elem[0]) for elem in Counter(inputData).mostCommon()]
    mostCommonDict = Counter(inputData).mostCommonDict()

    # Creating a binary tree
    tree = createTree(mostCommon)

    # We pass through the tree assigning codes to symbols
    code = walkTree(tree.item)

    decodeDict = { code[elem]:elem for elem in code }

    if printTable:
        # Sorting by code length
        code = { elem[0]:elem[1] for elem in sorted(code.items(), key=lambda kv: len(kv[1])) }

        if sortedByLen:
            # Sorted by code len
            # Forming the rows of the table
            for symbol in code:
                td.append([f'"{symbol}"', mostCommonDict[symbol], code[symbol]])
                td.append([" ", " ", " "])
            
        elif sortedByCount:
            # Sorted by count
            # Forming the rows of the table
            for symbol in mostCommonDict:
                td.append([f'"{symbol}"', mostCommonDict[symbol], code[symbol]])
                td.append([" ", " ", " "])


        table = PrettyTable(th)


        # We cut off the extra space
        table.add_rows(td[:-1])

        print("\vEncoding table:\v")
        print(table)
        print()

    encoded = '1' + ''.join([code[s] for s in inputData])


    if printEncodedLine:
        print("Encoded: ", ' '.join([code[s] for s in inputData]))

    # Decode
    decoded = ""
    key = ""
    decodeKeys = decodeDict.keys()
    for i in encoded[1:]:
        key += i
        if key in decodeKeys:
            decoded += decodeDict[key]
            key = ""
    
    print("Decoded:", decoded)


if __name__ == "__main__":
    main()