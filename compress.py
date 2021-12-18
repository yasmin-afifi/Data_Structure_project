from final_formatting import *
from bitstring import BitArray

#compress file by deleting spaces and new lines
def minify_file(text):
    k = 0
    t = ('>'.join([subtext.strip('\n' ' ' '\t') for subtext in text.split('>')]))
    i = 0
    while i < len(t) - 2:
        if t[i] == '<' and t[i + 1] == '/':
            z = i
            if (t[i - 1] == '/n' or t[i - 1] == '/t' or t[i - 1] == ' '):
                while (t[i - 1] == '/n' or t[i - 1] == '/t' or t[i - 1] == ' '):
                    k -= 1
                    i -= 1
                    if (i == 0): break
                t = t[:i - 1] + t[z:]

        k += 1
        i += 1
    return t


Tree = {}
class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ''

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


#function to count freq of act char in compressed spaces and lines file
def frequency_of_chars(name):
    f = open(name,'r')
    frequency = {}
    Lines = f.read()
    for char in Lines:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    return frequency


#create tree of HUffman algotirhm
def creat_Tree(name):
    Nodes= []
    frequency = frequency_of_chars(name)
    for char in frequency:
        Nodes.append(Node(frequency[char], char))

    while len(Nodes) > 1:
        Nodes = sorted(Nodes, key=lambda x: x.freq)

        left = Nodes[0]
        right = Nodes[1]

        left.huff = 0
        right.huff = 1

        newNode = Node(left.freq + right.freq, left.symbol + right.symbol, left, right)

        Nodes.remove(left)
        Nodes.remove(right)
        Nodes.append(newNode)
    compress_Huffman(Nodes[0])
    return Nodes[0]


#store encoded data in array
def compress_Huffman(node, val=''):
    # huffman code for current node
    newVal = val + str(node.huff)

    # if node is not an edge node
    # then traverse inside it
    if node.left:
        compress_Huffman(node.left, newVal)
    if node.right:
        compress_Huffman(node.right, newVal)

        # if node is edge node then
        # display its huffman code
    if not node.left and not node.right:
        Tree[node.symbol] = newVal

def generate_compress_code(name):
    file = open(name,'r')
    root = creat_Tree(name)
    s= ''
    text = file.read()
    trieBits = []
    restore_huffman_tree(root, trieBits)
    trieBits = "".join(trieBits)
    for i in text:
        s+= Tree[i]
    with open(name.split('.')[0]+'.Huffman', 'wb') as compress_file:
        compressed_data = format(len(trieBits), '064b') + trieBits + format(len(text), '064b') + s
        bitArray = BitArray(bin=compressed_data)
        bitArray.tofile(compress_file)
    return s

#function udes to restore Huffman tree to use it in decompression
def restore_huffman_tree(node, bitArray):
    if node.is_leaf():
        bitArray.append('1')
        bitArray.append(format(ord(node.symbol), '08b'))
        return

    bitArray.append('0')
    restore_huffman_tree(node.left, bitArray)
    restore_huffman_tree(node.right, bitArray)

#function udes to store Huffman tree to use it in decompression
def store_Huffman_tree(trieBits):
    isLeaf = int(trieBits.pop(0))
    if isLeaf:
        char = chr(int("".join([trieBits.pop(0) for _ in range(8)]), 2))
        return Node(-1, char, None, None)

    return Node(-1, '\0', store_Huffman_tree(trieBits), store_Huffman_tree(trieBits))

def decompress_Huffman(file_name) :
    # Read file bits as string
    with open(file_name, 'rb') as compressed_file:
        data = compressed_file.read()
        bitArray = "".join(map(lambda byte: format(byte, '08b'), data))

    # Get the length of the trie model
    BitsLength = int(bitArray[:64], 2)

    # Get the trie bits
    Bits = list(bitArray[64: 64 + BitsLength])

    # Construct the trie
    root = store_Huffman_tree(Bits)

    # Get characters number
    charsLength = int(bitArray[64 + BitsLength: 64 + BitsLength + 64], 2)

    # Get the encoded bits
    encoded_text = bitArray[64 + BitsLength + 64:]

    # Decode the text using the trie
    chars = []
    index = 0
    for i in range(charsLength):
        x = root
        while not x.is_leaf():
            bit = int(encoded_text[index])
            if bit:
                x = x.right
            else:
                x = x.left

            index += 1

        chars.append(x.symbol)
    text = ''
    for c in chars:
        text += c
    return formatting(text)
