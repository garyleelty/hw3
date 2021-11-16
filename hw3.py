import sys
import random

# print the output out.
def output(counts,total,nonTerminal_states,all):
    
    print("Count: ")
    b=[]
    for i in (counts):
        print(i[0:2],i[2])
    print("\nTotal:")
    for i in (total):
        print(i[0:2], i[2])
    for i in range(nonTerminal_states):
        best = [0,0,-1]
        act_num=0
        for c in all:
            if(c[0]==i):
                act_num+=1
        for t in range(act_num):
            if(readTable(i,t,counts)!=0):
                bc=readTable(i,t,total)/readTable(i,t,counts)
            else:
                bc=0
            if(bc > best[2]):
                best=[i,t,bc]
        b.append(best[0:2])
    print("Best action: " ,b)

def getBest(s,counts,total,nonTerminal_states):
    #get the best action of state s
    best = [0, 0, -1]
    for t in range(nonTerminal_states):
        if (readTable(s, t, counts) != 0):
            # get the best 
            bc = readTable(s, t, total) / readTable(s, t, counts)
        else:
            bc = 0
        if (bc > best[2]):
            best = [s, t, bc]
    print(best)



def MDP(s,nonTerminal_states,terminal_states,M,dictR,all,counts,total):
    touched =[]
    # all act that being done
    current_state = s
    while(current_state<nonTerminal_states):
        state = readState(current_state,all)
        n = len(state)
        
        act_list = [a for a in range(n)]
        
        possibility,judge = chooseAction(current_state,counts,total,M,all,dictR)
        if(judge):
            a = possibility[1]
        else:
            a = (random.choices(act_list, possibility))[0]
        touched.append([current_state,a])
        current_state=randomMove(current_state,a,all)
    reward=(getReward(current_state, dictR))
    used_list(touched, reward, counts, total)
    return 0

# get the reward in the dict
def getReward(current_state,dictR):
    return dictR.get(current_state)

def used_list(touched, reward, counts, total):
    used_list=[]
    for item in touched:
        if (not (item in used_list)):
            used_list.append(item)
    # check the used list if is same count+=1
    for a in used_list:
        for b in counts:
            if(a==b[0:2]):
                b[2]+=1
    # check the used list if is same total+=reward
    for a in used_list:
        for b in total:
            if(a==b[0:2]):
                b[2]+=reward

# get the random move choose to start 
def randomMove(s,a,all):
    possibility = []
    t=[]
    start=[]
    for item in all:
        if (s == item[0]):
            if(a==item[1]):
                start=item[2:]
                break
    for rd in (start):
        t.append(rd[0])
        possibility.append(rd[1])
    
    a = (random.choices(t, possibility))[0]
    return a

#choose the action according to the following algorithm
def chooseAction(s,counts,total,M,all,dictR):
    state=readState(s,all)
    n = len(state)
    for act in counts:
        if(act[0]==s):
            if(act[2]==0):
                return(act[0:2],True)
    avg = []
    for i in range(0,n):
        t = state[i][1]
        avg.append(readTable(s,t,total)/readTable(s,t,counts))
    bottom = 9999
    top = -100
    for a in range(len(dictR)):
        if(list(dictR.values())[a]<bottom):
            bottom = list(dictR.values())[a]
        if(list(dictR.values())[a]>top):
            top = list(dictR.values())[a]
    savg = []
    for i in range(n):
        savg.append(0.25+0.75*(avg[i]-bottom)/(top-bottom))
    c=0
    for i in range(n):
        c+=readTable(s,i,counts)
    up=[]
    for i in range(n):
        up.append(savg[i]**(c/M))
    norm = 0 
    for i in range(n):
        norm+=up[i]
    p=[]
    for i in range(n):
        p.append(up[i]/norm)
    return  p,False

# read the table 
def readTable(s,t,table):
    for act in table:
        if(act[0]==s):
            if(act[1]==t):
                return act[2]

# read the state by compare
def readState(s,all):
    readState = []
    for item in all:
        if(s == item[0]):
            readState.append(item)
    return readState

    
# get all the input from txt
def main(argv):
    nonTerminal_states = 0
    terminal_states = 0
    rounds = 0
    frequency = 0
    M = 0
    dictR = {}
    all = []
    counts = []
    total = []
    count = 1
    inputfile = argv[1]
    #print(inputfile)
    with open(inputfile,"r") as f:
        for line in f:
            if count == 1:
                line1 = line.split()
                #print(line1)
                nonTerminal_states = int(line1[0])
                terminal_states = int(line1[1])
                rounds = int(line1[2])
                frequency = int(line1[3])
                M = int(line1[4])
                count += 1
            elif count == 2:
                line1 = line.split()
                for a in range(0,len(line1)-1,2):
                    #print(a)
                    dictR[int(line1[a])] = int(line1[a+1])
                #print(dictR)
                count+=1
            else: 
                line1 = line.split()
                temp= []
                a = line1[0].split(":")
                temp.append(int(a[0]))
                temp.append(int(a[1]))
                counts.append([int(a[0]),int(a[1]),0])
                total.append([int(a[0]),int(a[1]),0])
                for i in range(1,len(line1),2):
                    temp.append([int(line1[i]),float(line1[i+1])])
                all.append(temp)
                #print(all)
    for i in range(rounds):
        s=random.randint(0,nonTerminal_states-1)
        # start random
        MDP(s,nonTerminal_states,terminal_states,M,dictR,all,counts,total)
        
        if((i+1)%frequency==0 ):
            print("\nAfter ", i+1, " rounds")
            output(counts,total,nonTerminal_states,all)
    print("\nFinally: ")
    output(counts, total, nonTerminal_states,all)

if __name__ == "__main__":
   main(sys.argv)