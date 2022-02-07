# First networkx library is imported
# along with matplotlib
import networkx as nx
import matplotlib.pyplot as plt
from compress import *



# Defining a Class
class GraphVisualization:

    def __init__(self):
        # visual is a list which stores all
        # the set of edges that constitutes a
        # graph
        self.visual = []

    # addEdge function inputs the vertices of an
    # edge and appends it to the visual list
    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    # In visualize function G is an object of
    # class Graph given by networkx G.add_edges_from(visual)
    # creates a graph with a given list
    # nx.draw_networkx(G) - plots the graph
    # plt.show() - displays the graph
    def visualize(self):
        G = nx.DiGraph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()

graph = []
def add_follower_edges(lines):
    col = []
    flag = False
    lines = minify_file(lines)
    G = GraphVisualization()
    for i in range(len(lines)):
        if (i + 5 < len(lines) and lines[i] == '<' and lines[i + 1] == 'u' and lines[i + 2] == 's' and lines[
            i + 3] == 'e' and lines[i + 4] == 'r' and lines[i + 5] == '>'):
            while (i + 3 < len(lines) and (
                    lines[i] != '<' or lines[i + 1] != 'i' or lines[i + 2] != 'd' or lines[i + 3] != '>')):
                i += 1
            i += 4
            id = ''
            while (lines[i] != '<'):
                id += (lines[i])
                i += 1
            if(flag):
                print(col)
                graph.append(col)
                col = []
            u = int(id)
        elif (i + 9 < len(lines) and lines[i] == '<' and lines[i + 1] == 'f' and lines[i + 2] == 'o' and lines[
            i + 3] == 'l' and lines[i + 4] == 'l' and lines[i + 5] == 'o' and lines[i + 6] == 'w' and lines[
                  i + 7] == 'e' and lines[i + 8] == 'r' and lines[i + 9] == '>'):
            flag = True
            while (i + 1 < len(lines) and (lines[i] != 'i' or lines[i + 1] != 'd')):
                i += 1
            i += 3
            id = ''
            while (lines[i] != '<'):
                id += (lines[i])
                i += 1
            f = int(id)
            G.addEdge(u, f)
            col.append(f)
        else:
            i += 1
    G.visualize()
    graph.append(col)
    print(graph)

def network_analysis():
    s = 'The id of the most influncer user:'
    x = 0
    #know the user that has most followers
    for i in range(len(graph)):
        if len(graph[i]) > x:
            x = len(graph[i])
            f = i + 1
    for i in range(len(graph)):
        if len(graph[i]) == x:
            f = i + 1
            s += str(f)+ ' '

    s += '\n'
    s += 'The id of the most active user:'
    x = 0
    l = 0
    # know the user that connected to lots of users
    for i in range(len(graph)):
        for j in range(len(graph)):
            if(i+1 in graph[j]):
                print(i+1,graph[j])
                x +=1
        print(x)
        if(x >l):
            l = x
            f = i + 1
        x = 0
    x = 0
    for i in range(len(graph)):
        for j in range(len(graph)):
            if(i+1 in graph[j]):
                x +=1
        if(x == l):
            f = i + 1
            s+= str(f) + ' '
        x = 0
    s+= '\n'
    #know the mutual friends between 2 users
    for j in range (len(graph)):
        for i in range(len(graph)):
            if( i > j):
                s += 'The mutual friends between user ' + str(j + 1) + ' and ' + str(i+1) + ': '
                for k in range(len(graph)):
                    if( k+1 in graph[j] and k+1 in graph[i]):
                        s+= str(k+1) + ' '
                s+='\n'
    #know the followers of his followers
    for i in range(len(graph)):
        sett = set()
        s+= "The suggest list of user "+ str(i+1) + ':'
        for j in (graph[i]):
            for k in (graph[j - 1]):
                if (k not in graph[i] and k != i+1):
                    sett.add(k)
        for l in (sett):
            s+= str(l) + ' '
        s+= '\n'
    return s