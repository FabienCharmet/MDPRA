import sys,re,difflib,time,datetime
import numpy as np
from array import array
from collections import deque, namedtuple


np.set_printoptions(threshold=sys.maxsize)

class Graph(object):

    def __init__(self, graph_dict=None):
        """ initializes a graph object 
            If no dictionary or None is given, an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict


    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in 
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list; 
            between two vertices can be multiple edges! 
        """
        edge = set(edge)
        vertex1 = edge.pop()
        if edge:
            # not a loop
            vertex2 = edge.pop()
        else:
            # a loop
            vertex2 = vertex1
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res

    def find_isolated_vertices(self):
        """ returns a list of isolated vertices. """
        graph = self.__graph_dict
        isolated = []
        for vertex in graph:
            print(isolated, vertex)
            if not graph[vertex]:
                isolated += [vertex]
        return isolated

    def find_path(self, start_vertex, end_vertex, path=[]):
        """ find a path from start_vertex to end_vertex 
            in graph """
        graph = self.__graph_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return path
        if start_vertex not in graph:
            return None
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_path = self.find_path(vertex, 
                                               end_vertex, 
                                               path)
                if extended_path: 
                    return extended_path
        return None
    

    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        """ find all paths from start_vertex to 
            end_vertex in graph """
        graph = self.__graph_dict 
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex, 
                                                     end_vertex, 
                                                     path)
                for p in extended_paths: 
                    paths.append(p)
        return paths

    def is_connected(self, 
                     vertices_encountered = None, 
                     start_vertex=None):
        """ determines if the graph is connected """
        if vertices_encountered is None:
            vertices_encountered = set()
        gdict = self.__graph_dict        
        vertices = list(gdict.keys()) # "list" necessary in Python 3 
        if not start_vertex:
            # chosse a vertex from graph as a starting point
            start_vertex = vertices[0]
        vertices_encountered.add(start_vertex)
        if len(vertices_encountered) != len(vertices):
            for vertex in gdict[start_vertex]:
                if vertex not in vertices_encountered:
                    if self.is_connected(vertices_encountered, vertex):
                        return True
        else:
            return True
        return False

filename = sys.argv[1]
N = int(sys.argv[2])
mig_size = int(sys.argv[3])

print(filename)
f = open(filename,"r")


mon_a = []
unmon_a = []
luring_a = []
states_a = []
states_names =[]

monitoring_links = []
unmonitoring_links = []
luring_links = []
states = []

a1 = 10 #financial cost of monitoring
a2 = 10 #computational cost of monitoring
a3 = 1 #financial cost of luring
 
proba = 0.9 #probability of detecting an attack
alpha = 0.7 #probability of an attack

node_value = {}
for i in range(N+1):
    if(i<=mig_size):
        node_value[i]=1.5
    else:
        node_value[i]=1


# TOPOLOGY DECLARATION ####################
source = 5 #location of the attacker
graph = { "1" : ["2","3","4"],
      "2" : ["1","3","4"],
      "3" : ["1","2","4","5"],
      "4" : ["1","2","3","5"],
      "5" : ["3","4"]
    }

dij = Graph(graph)
###########################################


#sys.setrecursionlimit(100000)


def reward_attack(i,x,y,z):
    #If there is no attack
    if(i==0):
        temp=0
        for j in range(1,N+1):
            temp=temp+node_value[j]
        return 10*temp
    else:
    #If there is an attack we check if global attack is completed
        for j in z:
            #path = dij.find_path(str(source),str(j))
            if(j!=0):
                path = dij.find_path(str(j),str(source))
                #Converting the list of int to str so we can compare them to see if the attack was succesful
                path2 = map(int, path)
                #print("path: " + str(path2) + " z: " + str(z))
                if(all(elem in z for elem in path2)):
                    #print("toto")
                    temp=0
                    for j in range(1,N+1):
                        temp=temp+node_value[j]
                    for j in z:
                        temp = temp - node_value[j]
                    return 10*temp
        temp=0
    #If the attack is not completed
        for j in range(1,N+1):
            temp=temp+node_value[j]
        temp = temp - (2 * float(detection_proba(y,i)) - 1) * node_value[i]
        return 10*temp

def detection_proba(y,i):
    nb_monitoring=0
    path = dij.find_path(str(i),str(source))
    #print(path)
    for j in y:
        if str(j) in path:
            nb_monitoring=nb_monitoring+1
    res = alpha *(1-(1-(1-proba)**nb_monitoring))
    #if(nb_monitoring>=1):
    #    print("Number of monitoring nodes: " + str(nb_monitoring))
    return '%.3f' % res


def target_proba(x,y,z,i):
    total_value=0
    check = 0
    res=0.0
    z2=list(z)
    z2.pop(len(z2)-1)
    nodes = set()
    zset = set()
    tset = set()
    #Adding nodes belonging to Z
    for j in range(1,mig_size+1): 
        if(j not in z2):
            nodes.add(j)
            zset.add(j)
    #Adding nodes belonging to T
    for j in range(1,N+1):
        for k in z2:
            if(k>0):
                path = dij.find_path(str(j),str(k))
                if(path!=None):
                    if(len(path)==2):
                        nodes.add(j)
                        tset.add(j)
            # else:
                # print("j :" + str(j) + " k: " + str(k))
    #We suppose we always migrate nodes starting from 1 to mig_size
    if(i in zset):    
        res = alpha * 3*float(node_value[i])
        check = check + node_value[i]
        #nodes.add(i)
    elif(i in tset):
        res = alpha * float(node_value[i])
        check = check + node_value[i]
    else:
        res=0.0
    for j in zset:
        total_value=total_value+3* node_value[j]
    for j in tset:
        total_value=total_value+ node_value[j]
        #if no match was found for the node we setup total_value to 1 so there is no division byu zero
    if(total_value==0):
        #total_value=1
        #print(tset)
        print("x: " + str(x) +" y: " + str(y) +" z: " + str(z) + "i: " + str(i))
    res = float(res)/float(total_value)
    # print("Check = " + str(check) + " Total = " + str(total_value) + " Node: " + str(i) + " res = " + str(res))
    return '%.5f' % res



print datetime.datetime.now()
print("Starting process")




for line in f:
    if(line[0]=='S'):
        states_a.append(line)
    if(line[:3]=="L_M"):
        mon_a.append(line)
    if(line[:4]=="L_UM"):
        unmon_a.append(line)
for l in mon_a:
    #print("--------------------------------------------\n\n")
    #print(l)
    p = re.compile("(L_M_)(\d{1,})([a-zA-Z0-9,\[\] ]+)_([a-zA-Z0-9,\[\] ]+)_(1|0.[0-9]+)_([-+]?[0-9]*\.?[0-9]+)")
    r = p.search(l)
    #print(r.group(6))
    monitoring_links.append([r.group(1), r.group(2), r.group(3), r.group(4), r.group(5), r.group(6)])

for l in unmon_a:
    #print("--------------------------------------------\n\n")
    #print(l)
    p = re.compile("(L_UM_)(\d{1,})([a-zA-Z0-9,\[\] ]+)_([a-zA-Z0-9,\[\] ]+)_(1|0.[0-9]+)_([-+]?[0-9]*\.?[0-9]+)")
    r = p.search(l)
    unmonitoring_links.append([r.group(1), r.group(2), r.group(3), r.group(4), r.group(5), r.group(6)])

# for l in luring_a:
    # #print("--------------------------------------------\n\n")
    # #print(l)
    # p = re.compile("(L_H_)(\d{1,})([a-zA-Z0-9,\[\] ]+)_([a-zA-Z0-9,\[\] ]+)_(1|0.[0-9]+)_(-?[0-9]+)")
    # r = p.search(l)
# luring_links.append([r.group(1), r.group(2), r.group(3), r.group(4), r.group(5), r.group(6)])

for s in states_a:
    p = re.compile("(S)([0-9]+),([0-9]+),(\[.*\]),(\[.*\]),(\[.*\])")
    r = p.search(s)
    states.append([s[:-1],int(r.group(2)),int(r.group(3)),eval(r.group(4)),eval(r.group(5)),eval(r.group(6))])
    
ftest = open("test","w+")
insert=""
for l in monitoring_links:
    print(l[2])
    print(l[3])
    print("\n")
    if(l[2]!=l[3]):
        p = re.compile("(S)([0-9]+),([0-9]+),(\[.*\]),(\[.*\]),(\[.*\])")
        r = p.search(l[3])
        migration_set = eval(r.group(4))
        monitoring_set = eval(r.group(5))
        attack_set = eval(r.group(6))
        target=attack_set[len(attack_set)-1]
        if(target>0):
            l[4]=target_proba(migration_set,monitoring_set,attack_set,target)
        else:
            l[4]=1-alpha
        l[5] = reward_attack(target,migration_set,monitoring_set,attack_set)
    insert = str(l[0]) + str(l[1]) + "_" +str(l[2]) + "_" + str(l[3]) + "_" + str(l[4]) + "_" + str(l[5]) + "_" + "\n"
    ftest.write(insert)

for l in unmonitoring_links:
    if(l[2]!=l[3]):
        p = re.compile("(S)([0-9]+),([0-9]+),(\[.*\]),(\[.*\]),(\[.*\])")
        r = p.search(l[3])
        migration_set = eval(r.group(4))
        monitoring_set = eval(r.group(5))
        attack_set = eval(r.group(6))
        target=attack_set[len(attack_set)-1]
        if(target>0):
            l[4]=target_proba(migration_set,monitoring_set,attack_set,target)
        else:
            l[4]=1-alpha
        l[5] = reward_attack(target,migration_set,monitoring_set,attack_set)
    insert = str(l[0]) + str(l[1]) + "_" +str(l[2]) + "_" + str(l[3]) + "_" + str(l[4]) + "_" + str(l[5]) + "_" + "\n"
    ftest.write(insert)

ftest.close()

# i=0
# for s in states_a:
    # states_names.append([s,"S"+str(i)])
    # for l in monitoring_links:
      # if(l[2] == s[:-1]):
          # l[2]="S"+str(i)
      # if(l[3] == s[:-1]):
          # l[3]="S"+str(i)

    # for l in unmonitoring_links:
      # if(l[2] == s[:-1]):
          # l[2]="S"+str(i)
      # if(l[3] == s[:-1]):
          # l[3]="S"+str(i)
    # i=i+1

    # # for l in luring_links:
      # # if(l[2] in s):
          # # l[2]="S"+str(i)
      # # if(l[3] in s):
          # # l[3]="S"+str(i)


# f2 = open("states_name-"+filename,"w+")
# for s in states_names:
    # f2.write(str(s)+"\n")
# f2.close()

# print("It's over now")
# print datetime.datetime.now()

# print("SUMMARY: \n Number of states: " + str(len(states_names)) + "\n Number of links: " + str(len(monitoring_links) + len(unmonitoring_links) + len(luring_links)))

# counter = open("counter","r")
# for l in counter:
    # sys.stdout.write(" " +l)
# print("\n")
# counter.close()
    # #if(isinstance(r,type(None))):
    #    print("error")
    #else:
    #    print(r.group())
    #print("--------------------------------------------\n\n")
#print(monitoring_links)
#print(unmonitoring_links)
