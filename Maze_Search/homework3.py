from collections import deque
from queue import PriorityQueue
import math

actiondict = {1:[1,0,0], 2:[-1,0,0], 3:[0,1,0], 4:[0,-1,0], 5:[0,0,1], 6:[0,0,-1],
            7:[1,1,0], 8:[1,-1,0], 9:[-1,1,0], 10:[-1,-1,0], 11:[1,0,1], 12:[1,0,-1],
            13:[-1,0,1], 14:[-1,0,-1], 15:[0,1,1], 16:[0,1,-1],17:[0,-1,1], 18:[0,-1,-1]}
addict ={}
explored = {}
parent = {}
sol = []
cost = {}
heu = {}
tcost = 0
nosol = -1

with open ("input.txt", "r") as inf:
    algo = inf.readline().strip()
    bound = tuple(map(int, inf.readline().split()))
    start = tuple(map(int, inf.readline().split()))
    goal = tuple(map(int, inf.readline().split()))
    
    #print(algo,bound,start)
    ngrid = int(inf.readline())
    #print(ngrid)

    explored[start] = False
    parent[start] = None
    cost[start] = 0

    for line in inf:
        temp = tuple(map(int,line.split()))
        key = temp[:3]
        action = temp[3:]
        explored[key] = False
        parent[key] = None

        for i in action:
            if (i<=18 and i>=1):
                neigh = tuple([a + b for a, b in zip(key, actiondict[i])])
                #print(neigh)
                if (neigh[0]<bound[0] and neigh[1]<bound[1] and neigh[2]<bound[2] and neigh[0]>=0 and neigh[1]>=0 and neigh[2]>=0):
                    addict.setdefault(key,[])

                    if i < 7:
                        addict[key].append((neigh,10))
                    else:
                        addict[key].append((neigh,14))  

                    explored[neigh] = False
                    parent[neigh] = None
                    

#print(addict)

#print(cost)

if algo == 'BFS':
    queue = deque()
    
    #print("enter")
    cost[start] = 0
    explored[start] = True
    queue.append(start)

    while not len(queue) == 0:
        u = queue.popleft()

        if u == goal:
            nosol = 1
            break

        for k in addict[u]:
            v = k[0]
            if not explored[v]:
                explored[v] = True
                cost[v] = 1
                parent[v] = u
                queue.append(v)



elif algo == 'UCS':
    newcost = 0
    cost[start] = 0
    qu = PriorityQueue()
    explored[start] = True
    qu.put((0, start))
    

    while not qu.empty():
        t = qu.get()
        u = t[1]

        if u == (125, 101, 181):
            print(t)
        #if u ==(126, 101, 181):
         #   print(t)

        if u == goal:
            #tcost = newcost
            nosol = 1
            break
        
        for k in addict[u]:
            v = k[0]
            if not explored[v]:
                explored[v] = True
                parent[v] = u
                cost[v] = k[1]
                newcost = t[0] + k[1]
                qu.put((newcost, v))




else:
    
    newcost = 0
    cost[start] = 0

    heu[start] = 0

    qu = PriorityQueue()
    explored[start] = True
    qu.put((0, start))
    

    while not qu.empty():
        t = qu.get()
        #print(t)
        u = t[1]

        if u == goal:
            #tcost = newcost
            nosol = 1
            break
        
        

        for k in addict[u]:
            v = k[0]
            if not explored[v]:
                explored[v] = True
                parent[v] = u
                heu[v] = math.floor(math.sqrt(sum([(a - b) ** 2 for a, b in zip(v, goal)])))
                cost[v] = k[1]
                newcost = t[0] + k[1] + heu[v] - heu[u]
                qu.put((newcost, v))
                print(t)




#print(cost)

if nosol == 1:
    node = goal

    while node is not None:
        #print(node)
        sol.append(node)

        
        tcost += cost[node]

        node = parent[node]
        
    sol.reverse()    

    with open ("output.txt",'w') as outf:
        print(tcost,file=outf)
        print(len(sol),file=outf)
        for node in sol[:-1]:
            print(node[0],node[1],node[2],cost[node], sep=' ', file = outf)
        node = sol[-1]
        print(node[0],node[1],node[2],cost[node], sep=' ', end ='', file = outf)

else:
    with open ("output.txt",'w') as outf:
        print("FAIL",file = outf,end = '')
