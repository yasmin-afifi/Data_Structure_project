
Tree = {}
#compress file by deleting spaces and new lines
def minify_file(name):
    file2 = open(name,'r')
    text = file2.read()
    return '>'.join([subtext.strip('\n' '\t' ' ') for subtext in text.split('>')])


#function to count freq of act char in compressed spaces and lines file
def frequency_of_chars(name):
    frequency = {}
    Lines = minify_file(name)
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
    minify_file(name)
    creat_Tree(name)
    s= ''
    text = minify_file(name)
    for i in text:
        s+= Tree[i]
    return s



def Huffman_Decompress(encoded_data, huffman_tree):
    tree_head = huffman_tree
    decoded_output = []
    for x in encoded_data:
        if x == '1':
            huffman_tree = huffman_tree.right
        elif x == '0':
            huffman_tree = huffman_tree.left
        if huffman_tree.left is None and huffman_tree.right is None:
            decoded_output.append(huffman_tree.symbol)
            huffman_tree = tree_head

    string = ''.join([str(item) for item in decoded_output])
    return string

def Decode_Huffman(name):
    bin = generate_compress_code(name)
    node = creat_Tree(name)
    return Huffman_Decompress(bin, node)

class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ''

