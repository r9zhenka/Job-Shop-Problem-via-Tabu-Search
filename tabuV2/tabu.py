import random
import json

from numpy import e


INF = 99999999

NO_EDGE = 0
DIRECTED = 1
NOT_DIRECTED = 2

def PrintGraph(edges):
    print('-' * 10)
    for i in range(len(edges)): print(edges[i])
    print('-' * 10)
    return


def FindLongesPathLen(edges, operations, start, finish) -> int:
    if start == finish: return 0

    longest = 0
    currentWeight = operations[start].weight
    for child in range(len(edges)):
        if start == child: continue
        if edges[start][child] != DIRECTED: continue
        longest = max(longest, currentWeight + FindLongesPathLen(edges, operations, child, finish))

    return longest


class Operation:
    def __init__(self, machine, weight, job, machines) -> None:
        self.job = job
        self.machine = machine
        self.weight = weight
        self.index = job * machines + machine + 1
        self.nextIndex = 0
        return


class Solution:
    def __init__(self, jobsData : list) -> None:
        self.machines = max( max(operation[0] for operation in job) for job in jobsData ) + 1
        self.jobs = len(jobsData)
        self.operations = self.jobs * self.machines
        self.operationArr = [Operation(0, 0, 0, 0) for _ in range(self.operations + 2)] # dummy

        S = []

        for jobInd in range(len(jobsData)):
            for operationInd in range(len(jobsData[jobInd])):
                machine = jobsData[jobInd][operationInd][0]
                weight = jobsData[jobInd][operationInd][1]
                operation = Operation(machine, weight, jobInd, self.machines)
                if (operationInd == 0):
                    S.append(operation.index)

                if (operationInd != len(jobsData[jobInd]) - 1):
                    nextMachine = jobsData[jobInd][operationInd + 1][0]
                    nextOperationIndex = jobInd * self.machines + nextMachine + 1
                    operation.nextIndex = nextOperationIndex

                self.operationArr[operation.index] = operation

        # we also add 2 nodes (start and end)
        self.edgesMat = [[NO_EDGE for i in range(self.operations + 2)] for j in range(self.operations + 2)]
        for i in range(self.operations + 2):
            self.edgesMat[0][i] = DIRECTED
            self.edgesMat[i][self.operations + 1] = DIRECTED

        # construct A - precedence constraints and weights
        for i in range(1, self.operations + 1):
            operation = self.operationArr[i]
            if operation.nextIndex != 0:
                self.edgesMat[operation.index][operation.nextIndex] = DIRECTED

            nextIndex = operation.index + self.machines
            if nextIndex <= self.operations:
                self.edgesMat[operation.index][nextIndex] = NOT_DIRECTED
                self.edgesMat[nextIndex][operation.index] = NOT_DIRECTED

        # PrintGraph(self.edgesMat)

        L = [0]
        while S:
            i = S.pop()
            for j in L:
                if self.edgesMat[i][j] == NOT_DIRECTED:
                    self.edgesMat[i][j] = NO_EDGE
                    self.edgesMat[j][i] = DIRECTED

            L.append(i)

            if self.operationArr[i].nextIndex != 0:
                S.append(self.operationArr[i].nextIndex)

        # PrintGraph(self.edgesMat)
        return


    def GetMakespan(self) -> int:
        return FindLongesPathLen(self.edgesMat, self.operationArr, 0, self.operations + 1)


    def GetNeighbors(self) -> list['Solution']:
        neighbors = []
        return neighbors


def TabuSearch(initialSolution : Solution, iterations : int, tabuSetSize : int):
    currentSolution = initialSolution
    bestSolution = currentSolution

    tabuSet = set()

    for _ in range(iterations):
        neighbors = currentSolution.GetNeighbors()
        bestNeighbor = None
        bestNeighborMakespan = float('inf')

        for neighbor in neighbors:
            if neighbor not in tabuSet:
                neighborMakespan = neighbor.GetMakespan()
                if neighborMakespan < bestNeighborMakespan:
                    bestNeighbor = neighbor
                    bestNeighborMakespan = neighborMakespan

        if bestNeighbor is None:
            # print("No non-tabu neighbors found, terminate the search")
            break

        currentSolution = bestNeighbor
        tabuSet.add(bestNeighbor)

        if len(tabuSet) > tabuSetSize:
            tabuSet.pop()

        if bestNeighbor.GetMakespan() < bestSolution.GetMakespan():
            bestSolution = bestNeighbor

    return bestSolution
