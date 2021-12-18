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


def main():
    #passing xml data as a string in str
    str = " "

    tree = XmlTree(str)
    print(xmlToJson(tree))


main()
