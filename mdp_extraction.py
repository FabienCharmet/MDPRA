import json,itertools,re,os,subprocess
import sys

c1=[30,40]
c2=[20,30,40]
# c2=[40]
p=[0.5,0.6,0.7,0.8,0.9]
size=[6]

for cf in c1:
    for cc in c2:
        for s in size:
            for p1 in p:
                if(cc<=cf):
                    print("Current file: model-"+str(s) + "-" + str(cf) + "-" + str(cc) + "-3-normal-topo"+str(s)+"-p"+str(p1))
                    subprocess.Popen(["python viextraction.py model-"+str(s) + "-" + str(cf) + "-" + str(cc) + "-3-normal-topo"+str(s) +"-p" + str(p1) + " " + str(s) +  " check"],shell=True, preexec_fn=os.setpgrp)
            os.system("python viextraction.py model-"+str(s) + "-" + str(cf) + "-" + str(10) + "-3-normal-topo"+str(s) +"-p" + str(p1) + " " + str(s) +  " check")

