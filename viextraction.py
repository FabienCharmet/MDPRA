import sys,re,difflib,time,datetime,mdptoolbox,gc,mdptoolbox.example,os
import numpy as np
from array import array
import json
import pickle
from scipy import sparse
np.set_printoptions(threshold=sys.maxsize)
np.seterr(divide='ignore', invalid='ignore')

#print sys.argv[1]

filename = sys.argv[1]
f = open(filename,"r")

N = int(sys.argv[2])

mon_a = []
unmon_a = []
donothing_a = []
states_a = []
states_names =[]

monitoring_links = []
unmonitoring_links = []
donothing_links = []
states = []

print(datetime.datetime.now())
print("Starting process")


class myE(Exception):
    def __init__(self, foo):
        self.foo = foo


for line in f:
    if(line[0]=='S'):
        states_a.append(line)
    if(line[:3]=="L_N"):
        donothing_a.append(line)
    if(line[:3]=="L_M"):
        mon_a.append(line)
    if(line[:4]=="L_UM"):
        unmon_a.append(line)
for l in mon_a:
    #print("--------------------------------------------\n\n")
    #print(l)
    p = re.compile("(L_M_)(\d{1,})([a-zA-Z0-9,\[\] ]+)_([a-zA-Z0-9,\[\] ]+)_(.*)_([-+]?[0-9]*\.?[0-9]+)")
    r = p.search(l)
    #print(r.group(6))
    monitoring_links.append([r.group(1), r.group(2), r.group(3), r.group(4), r.group(5), r.group(6)])

for l in unmon_a:
    #print("--------------------------------------------\n\n")
    #print(l)
    p = re.compile("(L_UM_)(\d{1,})([a-zA-Z0-9,\[\] ]+)_([a-zA-Z0-9,\[\] ]+)_(.*)_([-+]?[0-9]*\.?[0-9]+)")
    r = p.search(l)
    unmonitoring_links.append([r.group(1), r.group(2), r.group(3), r.group(4), r.group(5), r.group(6)])

for l in donothing_a:
    #print("--------------------------------------------\n\n")
    # print(l)
    p = re.compile("(L_N_)(\d{1,})([a-zA-Z0-9,\[\] ]+)_([a-zA-Z0-9,\[\] ]+)_(.*)_([-+]?[0-9]*\.?[0-9]+)")
    r = p.search(l)
    donothing_links.append([r.group(1), r.group(2), r.group(3), r.group(4), r.group(5), r.group(6)])


i=0
for s in states_a:
    states_names.append([s[:-1],"S"+str(i)])
    for l in monitoring_links:
      # print("debut " + l[3] + "fin " + s)
      # a=s
      # b=l[3]
      # print('{} => {}'.format(a,b))  
      # for i,s in enumerate(difflib.ndiff(a, b)):
         # if s[0]==' ': continue
         # elif s[0]=='-':
             # print(u'Delete "{}" from position {}'.format(s[-1],i))
         # elif s[0]=='+':
             # print(u'Add "{}" to position {}'.format(s[-1],i))    
             # print() 
          
      if(l[2] == s[:-1]):
          l[2]="S"+str(i)
      if(l[3] == s[:-1]):
          l[3]="S"+str(i)

    for l in unmonitoring_links:
      if(l[2] == s[:-1]):
          l[2]="S"+str(i)
      if(l[3] == s[:-1]):
          l[3]="S"+str(i)

    for l in donothing_links:
      if(l[2] == s[:-1]):
          l[2]="S"+str(i)
      if(l[3] == s[:-1]):
          l[3]="S"+str(i)
    i=i+1

f2 = open("states_name-"+filename,"w+")
for s in states_names:
    f2.write(str(s)+"\n")
f2.close()

P=[]
monitoring_rewards = []
unmonitoring_rewards = []
donothing_rewards = []
check = sys.argv[3]

# PARSING MONITORING ACTIONS
# NODES ARE NAMED FROM 1 TO N+1 NOW - DONT FORGET TO MODIFY
for i in range(1,N+1):
    transition = sparse.lil_matrix((len(states_names),len(states_names))) 
    reward = [0 for x in range(len(states_names))] 
    for l in monitoring_links:
        if(l[1]==str(i)):
            #print(l)
            a = int(l[2][1:])
            b = int(l[3][1:])
            transition[a,b] = l[4]
            reward[int(l[2][1:])]=l[5]
    monitoring_rewards.append(reward)

# SANITY CHECK FUNCTION: SUM OF ALL ELEMENTS IN LINE MUST EQUAL 1
    if(check=="check"):
        for n in range(len(states_names)):
            verif = transition[n,:].toarray()
            argmax = verif.argmax()
            sanitize = transition[n,:].sum()
            rem = transition[n,argmax]
            if(sanitize<1):
                transition[n,argmax] += (1-sanitize)
            if(sanitize>1):
                transition[n,argmax] -= (sanitize-1)

    P.append(transition)

# PARSING DO NOTHING ACTIONS
transition = sparse.lil_matrix((len(states_names),len(states_names))) 
reward = [0 for x in range(len(states_names))] 
for l in donothing_links:
    #print(l)
    a = int(l[2][1:])
    b = int(l[3][1:])
    transition[a,b] = l[4]
    reward[int(l[2][1:])]=l[5]
donothing_rewards.append(reward)

# SANITY CHECK FUNCTION: SUM OF ALL ELEMENTS IN LINE MUST EQUAL 1
if(check=="check"):
    for n in range(len(states_names)):
        verif = transition[n,:].toarray()
        argmax = verif.argmax()
        sanitize = transition[n,:].sum()
        rem = transition[n,argmax]
        if(sanitize<1):
            transition[n,argmax] += (1-sanitize)
        if(sanitize>1):
            transition[n,argmax] -= (sanitize-1)
P.append(transition)

# PARSING UNMONITORING ACTIONS
for i in range(1,N+1):
    transition = sparse.lil_matrix((len(states_names),len(states_names))) 
    reward = [0 for x in range(len(states_names))] 
    for l in unmonitoring_links:
        if(l[1]==str(i)):
            #print(l)
            a = int(l[2][1:])
            b = int(l[3][1:])
            transition[a,b] = l[4]
            reward[int(l[2][1:])]=l[5]
    unmonitoring_rewards.append(reward)

# SANITY CHECK FUNCTION: SUM OF ALL ELEMENTS IN LINE MUST EQUAL 1

    if(check=="check"):
        for n in range(len(states_names)):
            verif = transition[n,:].toarray()
            argmax = verif.argmax()
            sanitize = transition[n,:].sum()
            rem = transition[n,argmax]
            if(sanitize<1):
                transition[n,argmax] += (1-sanitize)
            if(sanitize>1):
                transition[n,argmax] -= (sanitize-1)
    P.append(transition)

R = []
for m in monitoring_rewards:
   temp = []
   for n in m:
       temp.append(n)
   R.append(temp)

for m in donothing_rewards:
   temp = []
   for n in m:
       temp.append(n)
   R.append(temp)

for m in unmonitoring_rewards:
   temp = []
   for n in m:
       temp.append(n)
   R.append(temp)

# P = np.array(P).astype(np.float)
R = np.asarray(R).astype(np.float)
R = np.transpose(R)

#print(mdptoolbox.util.check(P,R))
vi = mdptoolbox.mdp.PolicyIteration(P, R, 0.9)
vi.run()
# for i in range(len(vi.policy)):
     # print("State : " + str(states_names[i]) + " policy: " + str(vi.policy[i]))
np.set_printoptions(threshold=sys.maxsize)

exec(open("mdpbox.py","r").read())

P1,R1 = computePR(len(states_names),2*N+1,vi.policy,P,R)

print(len(states_names))
np.savetxt("test2",P1.toarray(), fmt='%s')
print("check")
#Determining which states belong to the main tree graph
members = mconnected(P1,len(states_names))
tinit=members[len(members)-1]

#Storing the IDs of states
P2ins=[]
for j in range(len(members)):
    t=members[j]
    if(t==tinit):
        P2ins.append(j)

#Generating the transition matrix, removing unnecessary nodes
P2=[]
R2=[]
for i in P2ins:
    Ptemp = P1[i,:].toarray()[0]
    temp=[Ptemp[j] for j in P2ins]
    P2.append(temp)
    R2.append(R1[i])

P2 = np.asarray(P2).astype(np.float)
# solution = solveStationary(P2)

stationaryD,RewardA=treeprob(P2,R2)
# stationaryD,RewardA=treeprob(P2,vi.V)
a={}
RewardA=RewardA.tolist()

a["filename"]=filename
a["distribution"]=str(stationaryD)
a["members"]=str(members)
a["policy"]=str(vi.policy)
a["Value"]=str(vi.V)
a["Reward"]=str(R2)
a["GReward"]=str(RewardA)
with open("mdp-results-"+filename,"w+") as f:
    f.write(json.dumps(a))
f2.close()

# print(len(RewardA))
# print(len(stationaryD))


print("It's over now")
print(datetime.datetime.now())

print("SUMMARY: \n Number of states: " + str(len(states_names)) + "\n Number of links: " + str(len(monitoring_links) + len(unmonitoring_links) + len(donothing_links)))

counter = open("counter"+filename[5:],"r")
for l in counter:
    sys.stdout.write(" " +l)
print("\n")
counter.close()
