import re
import json

class Node:
    def __init__(self,label):
        self.tag = label
        self.children = []
        self.tagProp = ""
        self.printed = False
        self.parent_comma = False

    
    def add_child(self,childNode):
        self.children.append(childNode)
    
    def get_children(self):
        return self.children

    def add_prop(self, property):
        self.tagProp = property

    def get_prop(self):
        dictofProp = {}
        # if there is no properties
        if len(self.tagProp) == 0:
            return dictofProp
        #slicing the properties string to get a list of the properties
        properties = self.tagProp.partition(' ')
        #for each property separate the key and the value and add them to the dict of properties
        for Property in properties:
            if Property != '' and Property != ' ':
                propKeyVal = Property.partition('=')
                dictofProp[propKeyVal[0]] = propKeyVal[2]
        return dictofProp
    
    def is_leaf(self):
        return len(self.children) == 0
    
    def height(self):
        node_height = -1
        sum = 0
        stackOfNodes = [self]
        while len(stackOfNodes) > 0:
            popped = stackOfNodes.pop()
            if popped.is_leaf():
                if sum > node_height:
                    node_height = sum
                sum = 0
            sum += 1
            for child in popped.get_children():
                stackOfNodes.append(child)
        return node_height


class XmlTree:
    def __init__(self,file):
        self.xml_file=file
        self.cleanerXML = []
        #converting the xml file into a list without the spaces and new lines
        datalist = re.split('<', self.xml_file)
        for i in datalist:
            self.cleanerXML.append(i.strip())
        #the following line removes every '' element in the resulting list as split gives a space element before the splitting pattern
        self.cleanerXML = [j for j in self.cleanerXML if j != '']
        #Creating the root of the tree choosing the first element in the created list and removing any tags or unwanted charecters
        self.root = Node(re.sub("[>/]", '', self.cleanerXML.pop()))
        self.createTree(self.root)

    def createTree(self,node):
        #poping every element of the list to check whether it's an opening tag, information or closing tag
        while len(self.cleanerXML):
            topElement = self.cleanerXML.pop()
            #extracting the attributes
            if topElement[0] != '/':
                propertyString = re.findall('(?<=\s).*?(?=>)', topElement)
                if len(propertyString) > 0:
                    node.add_prop(propertyString[0])
                if topElement[-1] != '>':
                    # if there's data, extract it by splitting the element to remove the > tag
                    info = topElement.partition('>')
                    node.add_child(Node(info[2]))
                return
            #if it was a closing tag
            elif topElement[0] == '/':
                #create a new node and add it to the current one
                newNode = Node(re.sub("[>/]", '', topElement))
                node.add_child(newNode)
                #a recursive call to build the whole tree
                self.createTree(newNode)
        return
    
    def getRoot(self):
        return self.root

#an object string to be as if it's passed by refrence not by value
class StrObj:

    def __init__(self, stri=""):
        self.stri = stri

    def __add__(self, stri):
        self.stri += stri
        return self

    def __str__(self):
        return self.stri


def xmlToJson(xmltree):
    #creating a string in json format and adding the first bracket in the json format to it
    jsonString = StrObj("{\n")
    square = False
    #filling the string with content of the xml tree but in json format by doing a depth first traversal starting with the root
    #and adding spaces to maintain the json format shape according to the depth of each node which indicates the nodes role whether it's a parent or a child or both   
    depth_traversal(xmltree.getRoot(), 1, jsonString, square, False, False)
    #adding the last bracket closing to the first one in json format
    jsonString += "\n}"
    print(jsonString)
    return jsonString


def depth_traversal(node, depth, js_str, square, last, comma):
    open_bracket = False

    if not node.is_leaf():
        js_str += f'{"  " * depth}'
    #if the node isn't there put it and check if it's a leaf put a "," according to json format and enter a new line
    if not node.printed:
        js_str += f'"{node.tag}"'
        if node.is_leaf():
            if comma or node.parent_comma:
                js_str += ","
            js_str += "\n"
    #if the node isn't a leaf then it's a tag so add ":" after it
        elif not node.is_leaf():
            js_str += ":"
    #if a tag has more than a value open a square bracket and go for a new line 
    if square:
        square = False
        js_str += "[\n"
        js_str += f'{"  " * depth}'

    if node.height() > 1 or len(node.get_prop()) > 0:
        open_bracket = True
        js_str += "{\n"
        key = list(node.get_prop().keys())
        val = list(node.get_prop().values())
        for i in range(len(node.get_prop())):
            js_str += f'{"  " * depth} "{key[i]}": {val[i]},\n'
        if len(node.get_prop()) > 0 and node.get_children()[0].is_leaf():
            js_str += f'{"  " * depth} "#text": '

    for i in reversed(range(len(node.get_children()))):
        comma = False
        if i != 0:
            if node.get_children()[i].get_children()[0].is_leaf():
                node.get_children()[i].get_children()[0].parent_comma = True
            comma = True

        for j in range(len(node.get_children())):
            if node.get_children()[i].tag == node.get_children()[j].tag and i != j:
                last = False
                if i == 0:
                    last = True
                square = False
                if not node.get_children()[i].printed:
                    square = True
                    node.get_children()[j].printed = True

        depth_traversal(node.get_children()[i], depth + 1, js_str, square, last, comma)
    #checking if we opened a bracket to fill the keys and values to close it
    if open_bracket:
        if depth > 1:
            js_str += f'{"  " * depth}}}'
            if comma or node.parent_comma or not last:
                js_str += ","
            js_str += "\n"
        else:
            js_str += f'{"  " * depth}}}'

    if node.printed and last:
        js_str += f'{"  " * depth}]'
        if comma:
            js_str += ","
        js_str += "\n"



def main():
    #passing xml data as a string in str
    str = " "

    tree = XmlTree(str)
    print(xmlToJson(tree))


    with open("given.json", "w") as json_file:
        json_file.write(xmlToJson(tree).__str__())
        json_file.close()
    
main()
