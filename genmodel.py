import sys, datetime, os
from collections import deque, namedtuple

#sys.setrecursionlimit(100000)

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

    def find_path2(self, start_vertex, end_vertex, path=[]):
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

    def find_path(self, start_vertex, end_vertex, path=[]):
        res = self.find_all_paths(start_vertex,end_vertex)
        minlen=len(res[0])
        srcp=0
        resp=res[0]
        for p in res:
            if(minlen>len(p)):
                    minlen=len(p)
                    resp=p
        return resp



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



N = int(sys.argv[1])
c1_init = int(sys.argv[2])
c2_init = int(sys.argv[3])
x_init = []
y_init = []
z_init = []
mig_size = int(sys.argv[4]) 
rootdir=""
a1 = 10 #financial cost of monitoring
a2 = 10 #computational cost of monitoring
a3 = 1 #financial cost of luring
 
p = float(sys.argv[7]) #probability of detecting an attack


node_value = {} 

for i in range(N+1):
    if (i<=mig_size):
        node_value[i]=10
    else:
        node_value[i]=5
        

def reward_attack(i,x,y,z):
    #If there is no attack
    z=list(dict.fromkeys(z))
    if(i==0):
        temp=0
        for j in range(1,N+1):
            temp=temp+node_value[j]
        return temp
    else:
    #If there is an attack we check if global attack is completed
        for j in z:
            #path = dij.find_path(str(source),str(j))
            if(j!=0):
                path = dij.find_path(str(j),str(source[j]))
                #Converting the list of int to str so we can compare them to see if the attack was succesful
                path2 = map(int, path)
                # print("source: " + str(j) + " dst: " + str(source) + " path: " + str(path2) + " z: " + str(z))
                if(all(elem in z for elem in path2)):
                    #print("toto")
                    temp=0
                    for j in range(1,N+1):
                        temp=temp+node_value[j]
                    for j in z:
                        if(j>0):
                            # temp = temp - node_value[j]
                            temp = temp - (1- float(detection_proba(y,j)))*node_value[j]
                    return temp
        temp=0
    #If the attack is not completed
        for j in range(1,N+1):
            temp=temp+node_value[j]
        temp = temp - (1- float(detection_proba(y,i))) * node_value[i]
        #temp = temp - (1- float(detection_proba(y,i))) * node_value[i]
        return temp


def detection_proba(y,i):
    nb_monitoring=0
    path = dij.find_path(str(i),str(source[i]))
    for j in y:
        if str(j) in path:
            nb_monitoring=nb_monitoring+1
    res = (1-p)**nb_monitoring
    res = 1 - res
    return '%.5f' % res


def target_proba(x,y,z,i):
    total_value=0
    check = 0
    res=0.0
    z2=list(z)

    nodes = set()
    zset = set()
    tset = set()
    #Adding nodes belonging to Z
    for j in range(1,mig_size+1): 
        if(j not in z2 and j in x and bool(set(x) & set(z))==False):
            nodes.add(j)
            zset.add(j)
    #Adding nodes belonging to T
    for j in range(1,N+1):
        for k in z2:
            if(k>0):
                path = dij.find_path(str(j),str(k))
                if(path!=None):
                    if(len(path)==2 and j not in zset and j not in z2):
                        nodes.add(j)
                        tset.add(j)
    #We suppose we always migrate nodes starting from 1 to mig_size
    if(source[0] not in tset and source[0] not in z2):
        tset.add(source[0])
    if(i in zset):    
        res = alpha * 3
    elif(i in tset):
        res = alpha
    else:
        res=0.0
        return 0
    for j in zset:
        total_value=total_value+3* node_value[j]
    for j in tset:
        total_value=total_value+ node_value[j]
    total_value=3 * len(zset) + len(tset)
    res = float(res)/float(total_value)
    return '%.2f' % res



def create_state(c1,c2,x,y,z):
    s = "S" + str(c1) + "," + str(c2) + "," + str(x) + "," + str(y) + "," + str(z)
    #print(s)
    return s

def create_link(action,s,s1,proba,reward):
    s = "L_"+action+s+"_"+s1+"_"+str(proba)+"_"+str(reward)+"\n"
    #print(s)
    return s

# TO CHANGE IF WE ADAPT BUDGET CONSUMATION
def getc1(i,mode="m"):
    # res = a1*node_value[i]
    res = a1
    if(mode=="u"):
        res/=2
    if(mode=="n"):
        res/=5
    return int(a1)

mem_line = []
def insert_sl(s):
    # print(s)
    mem_line.append(s)
    if(sys.getsizeof(mem_line)>10000000):
        try:
            f = open(rootdir+"model_log-"+str(N)+"-"+str(c1_init)+"-"+str(c2_init)+"-"+str(mig_size)+"-"+str(runmode)+"-"+str(topofile)+"-p"+str(p),"a+")
        except IOError: 
            print "Error: File does not appear to exist."
        for a in mem_line:
            f.write(a+"\n")
        f.close()
        del mem_line[:]


def generate(c1, c2, x, y, z, last_attack):

    global nonfinal_counter #number of non absorbing states
    global final_counter #number of absorbing states
    x2=list(x)
    if(len(x)<mig_size):
        x2.append(node_migr[len(x)])

    curr_s=create_state(c1,c2,x,y,z)
    curr_reward = reward_attack(last_attack,x,y,z)
    #print(curr_s)
    insert_sl(curr_s)
    if (c1<getc1(0,"n")):
        final_counter=final_counter+1
        for i in range(1,N+1):
            linkm = create_link("M_"+str(i),curr_s,curr_s,1,0)
            linkum = create_link("UM_"+str(i),curr_s,curr_s,1,0)
            insert_sl(linkm)
            insert_sl(linkum)
        linkn = create_link("N_"+str(0),curr_s,curr_s,1,curr_reward)
        insert_sl(linkn)

        return 0
    nonfinal_counter=nonfinal_counter+1 
    
    # DO NOTHING ACTION
    for i in range(N+1):
        z2 = list(z)
        z2.append(i)
        z2.sort()
        next_s = create_state(c1-getc1(0,"n"),c2,x2,y,z2)
        proba=0.0
        if(i==0):
            proba=1-alpha
            link = create_link("N_"+str(0),curr_s,next_s,1-alpha,curr_reward)
        else:
            proba = target_proba(x,y,z,i)
            link = create_link("N_"+str(0),curr_s,next_s,proba,curr_reward)
        if(proba>0.0):
            insert_sl(link)
            generate(c1-getc1(0,"n"),c2,x2,y,z2,i)
    del z2

    for n in range(1,N+1):
    # NOT ENOUGH BUDGET TO DO THIS ACTION i.e. expensive node
        if (c1<getc1(n)):
            next_s = create_state(0,c2,x2,y,z)
            linkm = create_link("M_"+str(n),curr_s,next_s,1,0)
            insert_sl(linkm)
            generate(0,c2,x2,y,z,0)

        if (c1<getc1(n,"u")):
            next_s = create_state(0,c2,x2,y,z)
            linkum = create_link("UM_"+str(n),curr_s,next_s,1,0)
            insert_sl(linkum)
            generate(0,c2,x2,y,z,0)

    # ENOUGH BUDGET TO MONITOR
        if (c1>=getc1(n)) and (c2>=a2):
            y2 = list(y)
            if n in y2:
                for i in range(N+1):
                    z2 = list(z)
                    z2.append(i)
                    z2.sort()
                    next_s = create_state(c1-getc1(n),c2,x2,y2,z2)
                    proba=0.0
                    if(i==0):
                        link = create_link("M_"+str(n),curr_s,next_s,1-alpha,0)
                        proba=1-alpha
                    else:
                        proba = target_proba(x,y,z,i)
                        link = create_link("M_"+str(n),curr_s,next_s,proba,0)
                    if(proba>0.0):
                        insert_sl(link)
                        generate(c1-getc1(n),c2,x2,y2,z2,i)
                del z2
            else:
                y2.append(n)
                y2.sort()
                for i in range(N+1):
                    z2 = list(z)
                    z2.append(i)
                    z2.sort()
                    next_s = create_state(c1-getc1(n),c2-a2,x2,y2,z2)
                    proba=0.0
                    if(i==0):
                        proba=1-alpha
                        link = create_link("M_"+str(n),curr_s,next_s,1-alpha,curr_reward)
                    else:
                        proba = target_proba(x,y,z,i)
                        link = create_link("M_"+str(n),curr_s,next_s,proba,curr_reward)
                    if(proba>0.0):
                        insert_sl(link)
                        generate(c1-getc1(n),c2-a2,x2,y2,z2,i)
                del z2
            del(y2)
    # NOT ENOUGH C2 BUDGET TO MONITOR
        if (c1>=getc1(n) and (c2<a2)):
            y2 = list(y)
            for i in range(N+1):
                z2 = list(z)
                z2.append(i)
                z2.sort()
                next_s = create_state(c1-getc1(n),c2,x2,y2,z2)
                proba=0.0
                if(i==0):
                    proba=1-alpha
                    link = create_link("M_"+str(n),curr_s,next_s,1-alpha,0)
                else:
                    proba = target_proba(x,y,z,i)
                    link = create_link("M_"+str(n),curr_s,next_s,proba,0)
                if(proba>0.0):
                    insert_sl(link)
                    generate(c1-getc1(n),c2,x2,y2,z2,i)
            del z2
            del(y2)
    # ENOUGH BUDGET TO UNMONITOR
        if (c1>=getc1(n,"u")):
            y2 = list(y)
            if n in y2:
                y2.remove(n)
                for i in range(N+1):
                    z2 = list(z)
                    z2.append(i)
                    z2.sort()
                    next_s = create_state(c1-getc1(n,"u"),c2+a2,x2,y2,z2)
                    proba=0.0
                    if(i==0):
                        proba=1-alpha
                        link = create_link("UM_"+str(n),curr_s,next_s,1-alpha,curr_reward)
                    else:
                        proba = target_proba(x,y,z,i)
                        link = create_link("UM_"+str(n),curr_s,next_s,proba,curr_reward)
                    if(proba>0.0):
                        insert_sl(link)
                        generate(c1-getc1(n,"u"),c2+a2,x2,y2,z2,i)
            else:
                for i in range(N+1):
                    z2 = list(z)
                    z2.append(i)
                    z2.sort()
                    next_s = create_state(c1-getc1(n,"u"),c2,x2,y2,z2)
                    proba=0.0
                    if(i==0):
                        link = create_link("UM_"+str(n),curr_s,next_s,1-alpha,0)
                        proba=1-alpha
                    else:
                        proba = target_proba(x,y,z,i)
                        link = create_link("UM_"+str(n),curr_s,next_s,proba,0)
                    if(proba>0.0):
                        insert_sl(link)
                        generate(c1-getc1(n,"u"),c2,x2,y2,z2,i)
            del(y2)
    del(x2)

tstart = datetime.datetime.now()
print(tstart)

# TOPOLOGY DECLARATION ####################
topofile = sys.argv[6]
execfile(topofile)
###########################################


final_counter=0
nonfinal_counter=0
runmode=sys.argv[5]
os.system("rm " + rootdir+"model_log-"+str(N)+"-"+str(c1_init)+"-"+str(c2_init)+"-"+str(mig_size)+"-"+str(runmode)+"-"+str(topofile)+"-p"+str(p)) 
if(runmode=="normal"):
    alpha=0.7
    generate(c1_init,c2_init,x_init,y_init,z_init,0)


print("Generation over")


counter = open(rootdir+"counter-"+str(N)+"-"+str(c1_init)+"-"+str(c2_init)+"-"+str(mig_size)+"-"+str(runmode)+"-"+str(topofile)+"-p"+str(p),"w+")
counter.write("Number of calls: " + str(final_counter + nonfinal_counter)+"\n")
counter.write("Number of absorbing calls: " + str(final_counter)+"\n")
counter.write("Number of non absorbing calls: " + str(nonfinal_counter))
counter.close()

f = open(rootdir+"model_log-"+str(N)+"-"+str(c1_init)+"-"+str(c2_init)+"-"+str(mig_size)+"-"+str(runmode)+"-"+str(topofile)+"-p"+str(p),"a+")
for a in mem_line:
    f.write(a+"\n")
f.close()

os.system("sort " + rootdir+"model_log-"+str(N)+"-"+str(c1_init)+"-"+str(c2_init)+"-"+str(mig_size)+"-"+str(runmode)+"-"+str(topofile)+"-p"+str(p) + " | uniq > " + rootdir+"model-"+str(N)+"-"+str(c1_init)+"-"+str(c2_init)+"-"+str(mig_size)+"-"+str(runmode)+"-"+str(topofile)+"-p"+str(p))


print("It's over now")
print("Summary: N = " + str(N) + " c1 = " + str(c1_init) + " c2 = " + str(c2_init) + " p = " + str(p))
tend = datetime.datetime.now()
print(tend)

ftime = open(rootdir+"generation_time.log","a+")
ftime.write("N = " + str(N) + " c1 = " + str(c1_init) + " c2 = " + str(c2_init) + " migration size: " + str(mig_size) +" topofile: " + str(topofile) + " tstart: " + str(tstart) + " tend: " + str(tend) + "\n")
ftime.close()
