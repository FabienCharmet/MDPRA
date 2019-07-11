import json,itertools,re,os,subprocess,sys

c1=[30,40]
c2=[10,20,30,40]
size=[6]
p = [0.5,0.6,0.7,0.8,0.9]

DETACHED_PROCESS = 0x00000008

for p1 in p:
    for s in size:
        for cf in c1:
            for cc in c2:
                if(cc<=cf):
                    # subprocess.Popen(["python genmodel.py "+str(s) + " " + str(cf) + " " + str(cc) + " 3 normal topo"+ str(s) +"m2 " + str(p1)],shell=True, preexec_fn=os.setpgrp)

                    os.system("python genmodel.py "+str(s) + " " + str(cf) + " " + str(cc) + " 3 normal topo"+str(s) + "m2 " + str(p1))
