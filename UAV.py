from tkinter import W
from src import Node, costUAV, TotalflightTime

INF = float('inf')

-12.5, 12.5 
-7.5, 12.5
-2.5, 12.5
2.5, 12.5
7.5, 12.5
12.5, 12.5

locations = [[0, 0], [-12.5, 12.5], [-7.5, 12.5], [-2.5, 12.5], [2.5, 12.5], [7.5, 12.5], [12.5, 12.5],
             [-12.5, 7.5], [-7.5, 7.5], [-2.5, 7.5], [2.5, 7.5], [7.5, 7.5], [12.5, 7.5],
             [-12.5, 2.5], [-7.5, 2.5], [-2.5, 2.5], [2.5, 2.5], [7.5, 2.5], [12.5, 2.5],
             [-12.5, -2.5], [-7.5, -2.5], [-2.5, -2.5], [2.5, -2.5], [7.5, -2.5], [12.5, -2.5],
             [-12.5, -7.5], [-7.5, -7.5], [-2.5, -7.5], [2.5, -7.5], [7.5, -7.5], [12.5, -7.5],
             [-12.5, -12.5], [-7.5, -12.5], [-2.5, -12.5], [2.5, -12.5], [7.5, -12.5], [12.5, -12.5],
             ]
priority = [0, 0.1, 0.1, 0.3, 0.4, 0.3, 0.6,
            0.1, 0.1, 0.3, 0.4, 0.3, 0.6,
            0.1, 0.1, 0.3, 0.4, 0.3, 0.6,
            0.1, 0.1, 0.3, 0.4, 0.3, 0.6,
            0.1, 0.1, 0.3, 0.4, 0.3, 0.6,
            0.1, 0.1, 0.3, 0.4, 0.3, 0.6,
            ]
data = [0, 30, 42, 54, 31, 12, 10,
        30, 42, 54, 31, 12, 10,
        30, 42, 54, 31, 12, 10,
        30, 42, 54, 31, 12, 10,
        30, 42, 54, 31, 12, 10,
        30, 42, 54, 31, 12, 10,
        ]

n_nodes = len(locations)
nodes = [Node(locations[i][0], locations[i][1], priority[i], data[i]) for i in range(n_nodes)]

CL = []
ANS = []

dp = [[-1 for i in range(TotalflightTime + 1)] for j in range(n_nodes + 1)]
def addLocation(sequence, W, n):
    global ANS
    if n == 1 or W == 0:
        if sum([nodes[i].utility() for i in ANS]) < sum([nodes[i].utility() for i in sequence]):
            ANS = sequence[:]
        elif sum([nodes[i].utility() for i in ANS]) == sum([nodes[i].utility() for i in sequence]):
            if sum([costUAV(nodes[i],nodes[i-1]) for i in ANS]) > sum([costUAV(nodes[i],nodes[i-1]) for i in ANS]):
                ANS= sequence[:]
        return 0
    if nodes[n-1].visited:
        addLocation(sequence, W, n-1)
        return 0
    if dp[n][W] != -1:
        if sum([nodes[i].utility() for i in ANS]) < sum([nodes[i].utility() for i in sequence]):
            ANS = sequence[:]
        elif sum([nodes[i].utility() for i in ANS]) == sum([nodes[i].utility() for i in sequence]):
            if sum([costUAV(nodes[i],nodes[i-1]) for i in ANS]) > sum([costUAV(nodes[i],nodes[i-1]) for i in ANS]):
                ANS= sequence[:]
        return dp[n][W]
    
    flag = False
    minCost = INF
    bestNode = []
    for j in range(1, len(sequence)):
        tempCost = 0
        tempCost -= costUAV(nodes[sequence[j]], nodes[sequence[j-1]])
        tempCost += costUAV(nodes[sequence[j]], nodes[n-1])
        tempCost += costUAV(nodes[sequence[j-1]], nodes[n-1])
        
        if tempCost < minCost:
            bestNode.clear()
            bestNode.append(j)
            minCost = tempCost
        elif tempCost == minCost:
            bestNode.append(j)
            
    if minCost <= W:
        for j in bestNode:
            tempSeq = sequence[:]
            tempSeq2 = sequence[:]
            tempSeq.insert(j, n-1)
            dp[n][W] = max(dp[n][W], nodes[n-1].utility() + addLocation(tempSeq, W-minCost, n-1), addLocation(tempSeq2, W, n-1))

        if sum([nodes[i].utility() for i in ANS]) < sum([nodes[i].utility() for i in sequence]):
            ANS = sequence[:]
        elif sum([nodes[i].utility() for i in ANS]) == sum([nodes[i].utility() for i in sequence]):
            if sum([costUAV(nodes[i],nodes[i-1]) for i in ANS]) > sum([costUAV(nodes[i],nodes[i-1]) for i in ANS]):
                ANS= sequence[:]
        return dp[n][W]
    
    else:
        dp[n][W] = addLocation(sequence, W, n-1)
        if sum([nodes[i].utility() for i in ANS]) < sum([nodes[i].utility() for i in sequence]):
            ANS = sequence[:]
        elif sum([nodes[i].utility() for i in ANS]) == sum([nodes[i].utility() for i in sequence]):
            if sum([costUAV(nodes[i],nodes[i-1]) for i in ANS]) > sum([costUAV(nodes[i],nodes[i-1]) for i in ANS]):
                ANS= sequence[:]
        return dp[n][W]
    # return dp[n][W]

def GRASP():
    global CL
    global ANS
    global dp
    
    for node in nodes:
        if 2*costUAV(node, nodes[0]) > TotalflightTime:
            nodes.remove(node)
    
    nodes[0].visited = True
    while(sum([not node.visited for node in nodes]) > 0):
        # print(sum([not node.visited for node in nodes]))
        path = [nodes[0], nodes[0]]
        sequence = [0, 0]
        W = TotalflightTime
        n = n_nodes
        
        dp = [[-1 for i in range(TotalflightTime + 1)] for j in range(n_nodes + 1)]
        addLocation(sequence, W, n)
        CL.append(ANS)
        for i in ANS:
            nodes[i].visited = True
        ANS = []
    return CL
            
    # for cl in CL:
    #     print([nodes[i] for i in cl])
    
GRASP()
j=0
for cl in CL:
    f= open(f'uav.dat{j}', 'w')
    for i in cl:
        f.write(f'{nodes[i].x}, {nodes[i].y} \n')
    f.close()
    j=j+1
    
f= open('uav0.dat', 'w')
for i in CL:
    for j in i:
        f.write(f'{nodes[j].x}, {nodes[j].y} \n')