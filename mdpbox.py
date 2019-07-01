import numpy as np
import scipy.sparse as sp
from scipy.linalg import eig 
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
#from discreteMarkovChain import markovChain
from numpy.linalg import matrix_power

sys.setrecursionlimit(150000)
def check_mat(P):
    i=0
    for m in P:
        for j in range(len(m)):
            temp=0
            cset = []
            for k in range(len(m[j])):
                temp=temp+m[j][k]
                if(m[j][k]>0):
                    cset.append(m[j][k])
            if(temp<1):
                print("Matrix: " + str(i) + " Sanitize: " + str(temp) + " Line: " + str(j) + " Set : " + str(cset))
    i=i+1

def computePR(S,A,policy,P,R):
    # Compute the transition matrix and the reward matrix for a policy.
    #
    # Arguments
    # ---------
    # Let S = number of states, A = number of actions
    # P(SxSxA)  = transition matrix
    #     P could be an array with 3 dimensions or a cell array (1xA),
    #     each cell containing a matrix (SxS) possibly sparse
    # R(SxSxA) or (SxA) = reward matrix
    #     R could be an array with 3 dimensions (SxSxA) or
    #     a cell array (1xA), each cell containing a sparse matrix (SxS) or
    #     a 2D array(SxA) possibly sparse
    # policy(S) = a policy
    #
    # Evaluation
    # ----------
    # Ppolicy(SxS)  = transition matrix for policy
    # PRpolicy(S)   = reward matrix for policy
    #
    Ppolicy = sparse.lil_matrix((S,S))
    Rpolicy = []
    for ind in range(len(policy)):  # avoid looping over S
        act = policy[ind]
       # print(len(R))
       # print(len(R[0]))
        Ppolicy[ind,:]=P[act][ind,:]
        Rpolicy.append(R[ind][act])
        if(R[ind][act]<0):
            print(R[ind][act])
        # R cannot be sparse with the code in its current condition, but
    # it should be possible in the future. Also, if R is so big that its
    # a good idea to use a sparse matrix for it, then converting PRpolicy
    # from a dense to sparse matrix doesn't seem very memory efficient
    if type(R) is sp.csr_matrix:
        Rpolicy = sp.csr_matrix(Rpolicy)
    if type(P) is sp.csr_matrix:
        Ppolicy = sp.csr_matrix(Ppolicy)
    # Ppolicy = Ppolicy
    # Rpolicy = Rpolicy
    return (Ppolicy, Rpolicy)

def computePRreward(S,A,policy,P,R):
    # Compute the transition matrix and the reward matrix for a policy.
    #
    # Arguments
    # ---------
    # Let S = number of states, A = number of actions
    # P(SxSxA)  = transition matrix
    #     P could be an array with 3 dimensions or a cell array (1xA),
    #     each cell containing a matrix (SxS) possibly sparse
    # R(SxSxA) or (SxA) = reward matrix
    #     R could be an array with 3 dimensions (SxSxA) or
    #     a cell array (1xA), each cell containing a sparse matrix (SxS) or
    #     a 2D array(SxA) possibly sparse
    # policy(S) = a policy
    #
    # Evaluation
    # ----------
    # Ppolicy(SxS)  = transition matrix for policy
    # PRpolicy(S)   = reward matrix for policy
    #
    Ppolicy = sparse.lil_matrix((S,S))
    Rpolicy = sparse.lil_matrix((S,S))
    for ind in range(len(policy)):  # avoid looping over S
        act = policy[ind]
       # print(len(R))
       # print(len(R[0]))
        Ppolicy[ind,:]=P[act][ind,:]
        Rpolicy[ind,:]=R[act][ind,:]
        # R cannot be sparse with the code in its current condition, but
    # it should be possible in the future. Also, if R is so big that its
    # a good idea to use a sparse matrix for it, then converting PRpolicy
    # from a dense to sparse matrix doesn't seem very memory efficient
    # Ppolicy = Ppolicy
    # Rpolicy = Rpolicy
    return (Ppolicy, Rpolicy)

def computePpolicyPRpolicy(S,A,policy,P,R):
    # Compute the transition matrix and the reward matrix for a policy.
    #
    # Arguments
    # ---------
    # Let S = number of states, A = number of actions
    # P(SxSxA)  = transition matrix
    #     P could be an array with 3 dimensions or a cell array (1xA),
    #     each cell containing a matrix (SxS) possibly sparse
    # R(SxSxA) or (SxA) = reward matrix
    #     R could be an array with 3 dimensions (SxSxA) or
    #     a cell array (1xA), each cell containing a sparse matrix (SxS) or
    #     a 2D array(SxA) possibly sparse
    # policy(S) = a policy
    #
    # Evaluation
    # ----------
    # Ppolicy(SxS)  = transition matrix for policy
    # PRpolicy(S)   = reward matrix for policy
    #
    Ppolicy = []
    Rpolicy = []
    for ind in range(len(policy)):  # avoid looping over S
        act = policy[ind]
       # print(len(R))
       # print(len(R[0]))
        Ppolicy.append(P[act][ind])
        Rpolicy.append(R[ind][act])
        # R cannot be sparse with the code in its current condition, but
    # it should be possible in the future. Also, if R is so big that its
    # a good idea to use a sparse matrix for it, then converting PRpolicy
    # from a dense to sparse matrix doesn't seem very memory efficient
    if type(R) is sp.csr_matrix:
        Rpolicy = sp.csr_matrix(Rpolicy)
    if type(P) is sp.csr_matrix:
        Ppolicy = sp.csr_matrix(Ppolicy)
    # Ppolicy = Ppolicy
    # Rpolicy = Rpolicy
    return (Ppolicy, Rpolicy)

            
def treeprob(P,value):
    V1=[0 for x in range(len(P))]
    Rcount=[0.0 for x in range(len(P))]
    Reward=[0.0 for x in range(len(P))]
    P=np.asarray(P).astype(float)
    #f=open("test3","w+")
    def treep(curr_i,V,R):
        # print(curr_i)
        # print(len(V))
        # print(len(P))
        # print(len(P[curr_i]))
        # f.write("P["+str(curr_i)+"] = "+str(P[curr_i][curr_i])+"\n")
        R+=value[curr_i]
        if(P[curr_i][curr_i]==1):
            V1[curr_i]+=V
            Reward[curr_i]+=R*V
            return 0 
        for j in range(len(P)):
            Vtemp = V
            if(P[curr_i][j]>0.0):
                Vtemp=V*P[curr_i][j]
                treep(j,Vtemp,R)
            # if(Vtemp<0):
                # print("i:" + str(curr_i) + " " + str(j))
    treep(len(P)-1,1,0)
    Reward = np.divide(Reward,V1)
    #f.close()
    return (V1,Reward)

def treeprobreward(P,value):
    V1=[0 for x in range(len(P))]
    Rcount=[0.0 for x in range(len(P))]
    Reward=[0.0 for x in range(len(P))]
    P=np.asarray(P).astype(float)
    #f=open("test3","w+")
    def treep(curr_i,V,R):
        # print(curr_i)
        # print(len(V))
        # print(len(P))
        # print(len(P[curr_i]))
        # f.write("P["+str(curr_i)+"] = "+str(P[curr_i][curr_i])+"\n")
        if(P[curr_i][curr_i]==1):
            V1[curr_i]+=V
            Reward[curr_i]+=R*V
            return 0 
        for j in range(len(P)):
            Vtemp = V
            if(P[curr_i][j]>0.0):
                treep(j,V*P[curr_i][j],R+value[curr_i,j])
            # if(Vtemp<0):
                # print("i:" + str(curr_i) + " " + str(j))
    treep(len(P)-1,1,0)
    Reward = np.divide(Reward,V1)
    #f.close()
    return (V1,Reward)

def mconnected(P,plen):
    V1=[0 for x in range(plen)]
    # f=open("test3","w+")
    def treep(curr_i):
        # print(P[curr_i,curr_i])
        # print(P[curr_i,:].nonzero())
        V1[curr_i]=1
        if(P[(curr_i,curr_i)]==1):
            return 0 
        for j in range(plen):
            if(P[curr_i,j]>0.0):
                treep(j)
    treep(plen-1)
    # f.close()
    return V1
