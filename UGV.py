from src import Node, costUGV

INF = float('inf')


locations = [[0, 0], [0, 5], [0, 10], [0, 15], [0, -5], [0, -10], [0, -15], [5, 0], [10, 0], [15, 0], [-5, 0], [-10, 0], [-15, 0],
            [10, 5], [10, 10], [10, 15], [10, -5], [10, -10], [10, -15], [5, 5], [5, 10], [5, 15], [5, -5], [5, -10], [5, -15],
            [-10, 5], [-10, 10], [-10, 15], [-10, -5], [-10, -10], [-10, -15], [-5, 5], [-5, 10], [-5, 15], [-5, -5], [-5, -10], [-5, -15],
            [-15, 5], [-15, 10], [-15, 15], [-15, -5], [-15, -10], [-15, -15], [15, 5], [15, 10], [15, 15], [15, -5], [15, -10], [15, -15],
             ]
priority = [0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
            0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
            0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
            0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
            ]
data = [0, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
        30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
        30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
        30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
        ]

n_nodes = len(locations)
nodes = [Node(locations[i][0], locations[i][1], priority[i], data[i]) for i in range(n_nodes)]

TotalcostUGV = sum([costUGV(nodes[i], nodes[(i+1)%n_nodes]) for i in range(n_nodes)])

ANS = []

dp = [[-1 for i in range(TotalcostUGV + 1)] for j in range(n_nodes + 1)]
def addLocation(sequence, W, n):
    global ANS
    if n == 1 or W == 0:
        if sum([nodes[i].utility() for i in ANS]) < sum([nodes[i].utility() for i in sequence]):
            ANS = sequence[:]
        return 0
    # if nodes[n-1].visited:
    #     addLocation(sequence, W, n-1)
    #     return 0
    if dp[n][W] != -1:
        if sum([nodes[i].utility() for i in ANS]) < sum([nodes[i].utility() for i in sequence]):
            ANS = sequence[:]
        return dp[n][W]
    
    flag = False
    minCost = INF
    bestNode = []
    for j in range(1, len(sequence)):
        tempCost = 0
        tempCost -= costUGV(nodes[sequence[j]], nodes[sequence[j-1]])
        tempCost += costUGV(nodes[sequence[j]], nodes[n-1])
        tempCost += costUGV(nodes[sequence[j-1]], nodes[n-1])
        
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
        return dp[n][W]
    
    else:
        dp[n][W] = addLocation(sequence, W, n-1)
        if sum([nodes[i].utility() for i in ANS]) < sum([nodes[i].utility() for i in sequence]):
            ANS = sequence[:]
        return dp[n][W]

sequence = [0, 0]
cost = 0
utility=0
W = TotalcostUGV
n = n_nodes
addLocation(sequence, W, n)
print(ANS)
f= open('ugv.dat', 'w')
for i in ANS:
    f.write(f'{nodes[i].x}, {nodes[i].y} \n')