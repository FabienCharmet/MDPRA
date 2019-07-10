import json,itertools,re,os,sys
import numpy as np
import math
c1=[30,40]
c2=[10,20,30,40]
size=[6]
proba=[0.5,0.6,0.7,0.8,0.9]

if(len(sys.argv)==2):
    path = sys.argv[1]
    print(path)
else:
    path = ""

for i in proba:
    os.system("rm mdptable-p"+str(i))

os.system("rm tablefile")
os.system("rm statfile")

# NODE STATS  ONLY WORKS WHEN PARSING ONE SIZE AT A TIME e.g. len(size)==1
stat_dict = dict.fromkeys(range(size[0]+1),0.0) 
stat_array = []
for p1 in proba:
    pstat_dict = dict.fromkeys(range(size[0]+1),0.0) 
    gtfile = open("tablefile","a+")
    insert="\\begin{table*}[]\n"
    insert+="\\resizebox{\\textwidth}{!}{%\n"
    insert+="\\begin{tabular}{|l|l|l|l|l|}\n"
    insert+="\\hline\n"
    insert+= "\\diagbox{($C_f,C_c$)}{Results} & Monitoring sets & Monitoring reward  & Average reward & Maximum reward \\\\ \hline\n"
    insert+="\\multicolumn{5}{|l|}{p="+str(p1)+" Attack source : Node 4} \\\\ \hline\n"
    gtfile.write(insert)

    statfile = open("statfile","w+")

    for cf in c1:
        for cc in c2:
                for s in size:
                        if(cc<=cf):
                            constr = str(s) + "-" + str(cf) + "-" + str(cc) + "-3-simple2-topo" + str(s) + "m2-p" + str(p1)
                            # constr = str(s) + "-" + str(cf) + "-" + str(cc) + "-3-simple2-topo" + str(s) + "-p" + str(p1)
                            continueb = True
                            try:
                                f = open(path+"mdp-results-model-" + constr)
                            except IOError:
                                continueb=False
                                print("Failed to openfile " + path + "mdp-results-model-" + constr )
                            if(continueb):
                                print(constr)
                                myj = json.loads(f.read())
                                try:
                                    test=myj["GReward"]
                                except:
                                    print("Failed to reward " + path + "mdp-results-model-" + constr )
                                    break
                                f.close()
                                myj["members"]=myj["members"].replace("  "," ")
                                myj["members"]=myj["members"].replace("\n","")  
                                myj["members"]=myj["members"].replace("[ ","[")
                                myj["members"]=myj["members"].replace(" ",",")  
                                myj["members"]=myj["members"].replace(",,",",")  
                                myj["members"]=myj["members"].replace("[,","[")
                                myj["members"]=myj["members"].replace("[,","[")
                                myj["members"]=eval(myj["members"])
                                for k in myj.keys():
                                    try:
                                        myj[k]=eval(myj[k])
                                    except:
                                        pass
                                        # print("Failed for: " + str(k))

                                # SV is the list of indexes of the states belonging to the optimal policy
                                SV = []
                                tinit = myj["members"][len(myj["members"])-1]
                                avgV=0.0
                                j=0
                                # print("Distribution sum: " + str(np.array(myj["distribution"]).sum()))
                                temp=0.0
                                for l in range(len(myj["members"])):
                                    if myj["members"][l] == tinit:
                                        avgV += myj["Value"][l] * myj["distribution"][j]
                                        temp+=myj["distribution"][j]
                                        SV.append(l)
                                        j+=1
                                    elif(myj["distribution"][j]>0):
                                        pass
                                        # print("State: " + str(l) + " " + str(myj["distribution"][j]))
                                print("Final distribution : " + str(temp))
                                states_a = []
                                states_names =[] 
                                states = []
                                monset_state = []
                                statepolicy = []
                                stat_monset = {}  
                                # print("Len dist: " + str(len(myj["distribution"])))
                                # print("Len val: " + str(len(myj["Value"])))

                                i=0
                                #Parsing the states names finding absorbing states
                                f = open(path + "model-" + constr)
                                p = re.compile("S([0-9]+),([0-9]+),(\[.*\]),(\[.*\]),(\[.*\])")
                                temp=0.0
                                
                                #PREPARING THE GLOBAL REWARD
                                GReward=myj["GReward"]
                                GReward = GReward.replace("nan","0")
                                GReward = GReward.replace("\n","")
                                GReward = GReward.replace("\t","")
                                GReward = GReward.replace("\r","")
                                GReward = GReward.replace("[ ","[")
                                GReward = GReward.replace("  "," ")
                                GReward = GReward.replace("  "," ")
                                GReward = GReward.replace(" ",",")
                                GReward = GReward.replace(",,",",")
                                GReward = GReward.replace(",,",",")
                                GReward = GReward.replace("[,","[")
                                GReward = np.array(eval(GReward))
                                # print(myj.keys())

                                for line in f:
                                        if(line[0]=='S'):
                                            states_a.append(line)
                                            r = p.search(line)
                                        #print(r.group(1))
                                        #STORING ALL STATES AND THEIR POLICY
                                        #IS IT A FINAL STATE ? (No budget left)
                                        # statepolicy.append([line,myj["policy"][i],myj["Value"][i],i])
                                            if(i in SV):
                                                statepolicy.append([line,myj["policy"][i],myj["Reward"][SV.index(i)],i])
                                                temp+=myj["distribution"][SV.index(i)]
                                            if(int(r.group(1))<5 and i in SV):
                                                # print(myj["distribution"][SV.index(i)])
                                                monset_state.append([line[:-1],r.group(4),myj["Value"][i],myj["distribution"][SV.index(i)],GReward[SV.index(i)],i,SV.index(i)])
                                                # except:
                                                    # monset_state.append([line[:-1],r.group(4),myj["Value"][i],myj["distribution"][SV.index(i)],myj["GReward"],i,SV.index(i)])
                                                # temp+=myj["distribution"][i]
                                            # elif(int(r.group(1))>5 and i in SV) and myj["distribution"][SV.index(i)]>0:
                                                # print("erreur")
                                                # print(myj["distribution"][SV.index(i)])
                                                # print(r.group(1))
                                                # temp+=myj["distribution"][SV.index(i)]
                                            i+=1
            
                                print("Global end distribution: " + str(temp))
                
                                                #if(not stat_monset.has_key(r.group(4))):
                                                # Presumabely useless  
                                                # if(r.group(4) not in stat_monset):
                                                    # stat_monset[r.group(4)]=0
                                f.close()
                                gr = open(path + "globalresults-model-" + constr,"w+")
                                avgR = sum(GReward)/len(GReward)
                                gr.write("Size = " +str(s) +" Cf = " + str(cf) + " Cc = " + str(cc) + " Average reward: " + str(avgR)+ " Maximum reward: " + str(int(max(GReward)))  + "\n")
                                dict_moni=dict.fromkeys([m[1] for m in monset_state],0.0)
                                value_moni=dict.fromkeys([m[1] for m in monset_state],0.0)
                                count_moni=dict.fromkeys([m[1] for m in monset_state],0.0)
                                reward_moni=dict.fromkeys([m[1] for m in monset_state],0.0)
                                temp=0.0
                                for m in monset_state:
                                    #gr.write(str(m)+"\n")
                                    #print(m[4])
                                    dict_moni[m[1]]+=m[3]
                                    reward_moni[m[1]]+=m[4]*m[3]
                                    value_moni[m[1]]+=m[2]*m[3]
                                    count_moni[m[1]]+=1
                                    temp+=m[3]
                                for v in value_moni.keys():
                                    value_moni[v]/=dict_moni[v]
                                for r in reward_moni.keys():
                                    reward_moni[r]/=dict_moni[r]



                                fpol = open(path + "policy-"+ constr,"w+")
                                for st in statepolicy:
                                    fpol.write("State: " + str(st[0])[:-1] + " Action: " + str(st[1]) + " Value : " + str(st[2]) + " ID: " + str(st[3]) + "\n" )
                                    
                                    #ARE THERE UNMONITORING ACTIONS IN THE OPTIMAL POLICY ?
                                    if int(st[1])>=s:
                                        pass
                                        #print("State: " + str(st[0]) + " Action: " + str(st[1]))

                                # print(len(reward_moni))
                                # print(len(value_moni))
                                # PREPARING LATEX TABLE
                                tablefile = open(path + "mdptable-p"+str(p1),"a+")
                                insert= "("+str(cf)+","+str(cc)+") " 
                                insert+="& \\begin{tabular}[c]{@{}l@{}} "
                                for dkey in dict_moni.keys():
                                    insert += " " + str(dkey) + " : " + str(dict_moni[dkey]) + "\\\\"
                                insert+=" \\end{tabular} & \\begin{tabular}[c]{@{}l@{}} "
                                for dkey in reward_moni.keys():
                                    insert += " " + str(dkey) + " : " + str(int(reward_moni[dkey])) + "\\\\"
                                insert+=" \\end{tabular} & " + str(int(avgR)) + "& " + str(int(max(GReward))) + " \\\\ \\hline\n"
                                insert=insert.replace("[","{[}")
                                insert=insert.replace("]","{]}")
                                insert=insert.replace("{[}c{]}","[c]")
                                tablefile.write(insert)
                                gtfile.write(insert)
                                tablefile.close()
                                
                                for node in range(1,s+1):
                                    for dkey in dict_moni.keys():
                                        if node in eval(dkey):
                                            stat_dict[node]+=dict_moni[dkey]
                                            pstat_dict[node]+=reward_moni[dkey]
                                        pstat_dict[0]+=dict_moni[dkey]
                                stat_dict[0]+=1



                                gr.write("Distribution: " + str(dict_moni)+ "\n")
                                gr.write("Reward: " + str(reward_moni)+ "\n")
                                gr.write("Value: " + str(value_moni) + "\n")
                                gr.write("Count: " + str(count_moni) + "\n")
                                # print a


                                print("Size = " +str(s) +" Cf = " + str(cf) + " Cc = " + str(cc) + " Average value: " + str(avgR)+ " Maximum reward: " + str(int(max(GReward))) +  "\n")
    insert="\\end{tabular}%\n"
    insert+="}\n"
    insert+="\\caption{Statistical distribution of monitoring sets}\n"
    insert+="\\label{tab:mdpresults}\n"
    insert+="\\end{table*}\n\n"
    gtfile.write(insert)
    gtfile.close()
    for i in range(1,s+1):
        pstat_dict[i]/=pstat_dict[0]
    stat_array.append(pstat_dict)
    # statfile.write(str(pstat_dict)+"\n")

for i in range(1,s+1):
    stat_dict[i]/=stat_dict[0]
print(stat_dict)
insert="\\begin{figure}[h]\n"
insert+="\\begin{tikzpicture}\n"
insert+="\\begin{axis}[\n"
insert+="  xlabel={Detection probability},\n"
insert+="  ylabel={Average reward of the node },\n"
insert+="  y label style={at={(0.06,0.5)}},\n"
insert+="  xtick={0.5,0.6,0.7,0.8,0.9,1.0},\n"
insert+="  legend style={at={(0.5,-0.22)},cells={align=right}, anchor=north,legend columns=3},\n"
insert+="  cycle list name=black white,\n"
insert+="  grid style=dashed,\n"
insert+="]\n\n"
statfile.write(insert)


legend="\\legend{"
for i in range(1,size[0]+1):
    legend+="Node " + str(i)+ ", "
    insert="\\addplot+[]\n"
    insert+="    coordinates {\n"
    for p in range(len(proba)):
        insert+="("+str(proba[p])+","+str(stat_array[p][i])+")"
    insert+="\n"
    insert+="};\n\n"
    statfile.write(insert)
legend=legend[:-2]
legend+="}\n"




statfile.write(legend)

insert="\\end{axis}\n"
insert+="\\end{tikzpicture}\n"
insert+="\\caption{Node impact - Single source}\n"
insert+="\\label{fig:nodeimp_single}\n"
insert+="\\end{figure}\n"
statfile.write(insert)
