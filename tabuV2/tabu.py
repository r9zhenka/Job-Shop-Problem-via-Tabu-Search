import random
import json
from copy import deepcopy


INF = 99999999

NO_EDGE = 0
DIRECTED = 1
NOT_DIRECTED = 2

def PrintGraph(edges):
    print('-' * 10)
    for i in range(len(edges)): print(edges[i])
    print('-' * 10)
    return


class Operation:
    def __init__(self, machine, weight, job, machines) -> None:
        if machines != 0:
            self.job = job
            self.machine = machine
            self.weight = weight
            self.index = job * machines + machine + 1
            self.nextIndex = 0
        else:
            self.job = -1
            self.machine = -1
            self.weight = 0
            self.index = 0
            self.nextIndex = 0

        return


class Solution:
    def __init__(self, machines, operationArr, edgesMat, startingOperations) -> None:
        self.machines = machines
        self.operations = len(operationArr) - 2
        self.startingOperations = startingOperations

        # those share same indexes
        # we also add 2 nodes (start and end)
        self.operationArr = operationArr
        self.edgesMat = edgesMat


    @classmethod
    def from_list(cls, jobsData : list) -> "Solution":
        machines = max( max(operation[0] for operation in job) for job in jobsData ) + 1
        jobs = len(jobsData)
        operations = jobs * machines

        # those share same indexes
        # we also add 2 nodes (start and end)
        operationArr = [Operation(0, 0, 0, 0) for _ in range(operations + 2)]
        operationArr[-1].index = operations + 1
        edgesMat = [[NO_EDGE for i in range(operations + 2)] for j in range(operations + 2)]

        startingOperations = []

        for jobInd in range(len(jobsData)):
            for operationInd in range(len(jobsData[jobInd])):
                machine = jobsData[jobInd][operationInd][0]
                weight = jobsData[jobInd][operationInd][1]
                operation = Operation(machine, weight, jobInd, machines)

                if operationInd == 0:
                    startingOperations.append(operation.index)

                if (operationInd != len(jobsData[jobInd]) - 1):
                    nextMachine = jobsData[jobInd][operationInd + 1][0]
                    nextOperationIndex = jobInd * machines + nextMachine + 1
                    operation.nextIndex = nextOperationIndex

                operationArr[operation.index] = operation


        for i in range(operations + 2):
            edgesMat[0][i] = DIRECTED
            edgesMat[i][operations + 1] = DIRECTED

        # construct A - precedence constraints and weights
        for i in range(1, operations + 1):
            operation = operationArr[i]
            if operation.nextIndex != 0:
                edgesMat[operation.index][operation.nextIndex] = DIRECTED

            for j in range(1, operations + 1):
                other = operationArr[j]
                if operation.machine == other.machine:
                    edgesMat[operation.index][other.index] = NOT_DIRECTED

        instance = cls(machines, operationArr, edgesMat, startingOperations)
        instance.ListSchedule()
        return instance


    def ListSchedule(self):
        scheduled = [0]
        priority = self.startingOperations.copy()
        while priority:
            i = priority.pop(0)

            for j in scheduled:
                if self.edgesMat[i][j] == NOT_DIRECTED:
                    self.edgesMat[i][j] = NO_EDGE
                    self.edgesMat[j][i] = DIRECTED
            scheduled.append(i)

            if self.operationArr[i].nextIndex != 0:
                priority.append(self.operationArr[i].nextIndex)
        return


    def GetCriticalPath(self) -> list[int]:
        # PLACEHOLDER
        start, finish = 0, self.operations + 1

        longestPath = []
        longestPathWeight = 0

        q = [ ([start], 0) ]
        while q:
            path, weight = q.pop(0)
            curr = path[-1]

            if curr == finish:
                if weight > longestPathWeight:
                    longestPath = path
                    longestPathWeight = weight

            for child in range(self.operations + 2):
                if child == curr: continue
                if self.edgesMat[curr][child] != DIRECTED: continue
                newPath = path.copy()
                newPath.append(child)
                q.append((newPath, weight + self.operationArr[child].weight))

        return longestPath


    def GetMakespan(self) -> int:
        return sum(self.operationArr[i].weight for i in self.GetCriticalPath())


    def GetNeighbors(self) -> list['Solution']:
        flippable = []
        criticalPath = self.GetCriticalPath()
        for i in range(len(criticalPath) - 1):
            operationA = self.operationArr[criticalPath[i]]
            operationB = self.operationArr[criticalPath[i+1]]

            if operationA.machine != operationB.machine:
                continue

            flippable.append( (operationA.index, operationB.index) )

        neighbors = []
        for indA, indB in flippable:
            newEdgesMat = deepcopy(self.edgesMat)
            newEdgesMat[indA][indB] = NO_EDGE
            newEdgesMat[indB][indA] = DIRECTED
            neighbors.append(Solution(self.machines, self.operationArr, newEdgesMat, self.startingOperations))

        return neighbors


def TabuSearch(initialSolution : Solution, iterations : int, tabuSetSize : int):
    currentSolution = initialSolution
    bestSolution = currentSolution

    tabuSet = set()

    for _ in range(iterations):
        neighbors = currentSolution.GetNeighbors()
        bestNeighbor = None
        bestNeighborMakespan = INF

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


if __name__ == "__main__":
    file = open("tests/0.json", 'r')
    jobsData = json.loads(file.read())["jobs_data"]
    file.close()

    tabu = TabuSearch(Solution.from_list(jobsData), iterations = 10, tabuSetSize = 3)
    PrintGraph(tabu.edgesMat)
    print(tabu.GetMakespan())
