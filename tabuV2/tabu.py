import json
import random
import time
from copy import deepcopy
from collections import deque
from functools import cmp_to_key


INF = 999999999
NO_EDGE = 0
DIRECTED = 1
NOT_DIRECTED = 2


def PrintGraph(edges):
    for i in range(len(edges)): print(edges[i])
    return


def timeit(func):
    def measure_time(*args, **kw):
        start_time = time.time()
        result = func(*args, **kw)
        print("Processing time of %s(): %.2f seconds."
                % (func.__qualname__, time.time() - start_time))
        return result
    return measure_time


class Operation:
    def __init__(self, machine, weight, job, machines) -> None:
        if machines != 0:
            self.job = job
            self.machine = machine
            self.weight = weight
            self.index = job * machines + machine + 1
            self.nextIndex = 0
            self.prevIndex = 0
        else:
            self.job = -1
            self.machine = -1
            self.weight = 0
            self.index = 0
            self.nextIndex = 0
            self.prevIndex = 0
        return


class Solution:
    def __init__(self, machines, operationArr, edgesMat) -> None:
        self.machines = machines
        self.operations = len(operationArr) - 2

        # those share same indexes
        # we also add 2 nodes (start and end)
        self.operationArr = operationArr
        self.edgesMat = edgesMat

        self.criticalPath = None
        self.makespan = None


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

                if operationInd != len(jobsData[jobInd]) - 1:
                    nextMachine = jobsData[jobInd][operationInd + 1][0]
                    nextOperationIndex = jobInd * machines + nextMachine + 1
                    operation.nextIndex = nextOperationIndex

                if operationInd != 0:
                    prevMachine = jobsData[jobInd][operationInd - 1][0]
                    prevOperationIndex = jobInd * machines + prevMachine + 1
                    operation.prevIndex = prevOperationIndex

                operationArr[operation.index] = operation


        for i in range(operations + 2):
            if i != 0:
                edgesMat[0][i] = DIRECTED
            if i != operations + 1:
                edgesMat[i][operations + 1] = DIRECTED

        # construct A - precedence constraints and weights
        for i in range(1, operations + 1):
            operation = operationArr[i]
            if operation.nextIndex != 0:
                edgesMat[operation.index][operation.nextIndex] = DIRECTED

            for j in range(i+1, operations + 1):
                other = operationArr[j]

                if operation.machine != other.machine: continue

                edgesMat[operation.index][other.index] = NOT_DIRECTED
                edgesMat[other.index][operation.index] = NOT_DIRECTED

        instance = cls(machines, operationArr, edgesMat)
        instance.ListSchedule(startingOperations)
        return instance


    def GetOperationTimeLeft(self, operationInd) -> int:
        time = 0
        operation = self.operationArr[operationInd]
        while operation.nextIndex != 0:
            time += operation.weight
            operation = self.operationArr[operation.nextIndex]
        return time


    def ListSchedule(self, startingOperations):
        scheduled = [0]

        priority = startingOperations
        while priority:
            # TODO: priority queue
            i = max(priority, key=self.GetOperationTimeLeft)
            priority.remove(i)

            for j in scheduled:
                if self.edgesMat[i][j] != NOT_DIRECTED:
                    continue

                self.edgesMat[i][j] = NO_EDGE
                self.edgesMat[j][i] = DIRECTED

            scheduled.append(i)

            if self.operationArr[i].nextIndex != 0:
                priority.append(self.operationArr[i].nextIndex)
        return


    def CriticalPathHelp(self, start, finish):
        longestPath = []
        longestPathWeight = 0

        bestWeights = [0 for _ in range(self.operations + 2)]

        q = [ ([start], 0) ]
        while q:
            path, weight = q.pop()
            curr = path[-1]

            bestWeights[curr] = weight

            if curr == finish and weight > longestPathWeight:
                longestPath = path
                longestPathWeight = weight

            for child in range(self.operations + 2):
                if self.edgesMat[curr][child] != DIRECTED: continue
                if bestWeights[child] > weight + self.operationArr[child].weight: continue

                newPath = path.copy()
                newPath.append(child)
                q.append((newPath, weight + self.operationArr[child].weight))

        return longestPath


    def GetCriticalPath(self) -> list[int]:
        if self.criticalPath is not None: return self.criticalPath

        start, finish  = 0, self.operations + 1
        longestPath = self.CriticalPathHelp(start, finish)

        self.criticalPath = longestPath
        return longestPath


    def GetMakespan(self) -> int:
        if self.makespan is not None: return self.makespan
        start, finish = 0, self.operations + 1


        q = [ (start, 0) ]
        bestWeights = [0 for _ in range(self.operations + 2)]
        while q:
            curr, weight = q.pop()
            bestWeights[curr] = weight

            for child in range(self.operations + 2):
                if self.edgesMat[curr][child] != DIRECTED: continue
                if bestWeights[child] > weight + self.operationArr[child].weight: continue

                q.append( (child, weight + self.operationArr[child].weight) )

        return bestWeights[-1]


    def GetMakespanApproximation(self) -> int:
        # TODO:
        return self.GetMakespan()


    def GetBestNeighbor(self) -> "Solution | None":
        flippable = []
        criticalPath = self.GetCriticalPath()
        for i in range(len(criticalPath) - 1):
            operationA = self.operationArr[criticalPath[i]]
            operationB = self.operationArr[criticalPath[i+1]]

            if operationA.machine != operationB.machine:
                continue

            flippable.append( (operationA.index, operationB.index) )

        # print(len(flippable))

        bestNeighbor = None
        bestMakespanApproximation = INF

        for indA, indB in flippable:
            self.edgesMat[indA][indB] = NO_EDGE
            self.edgesMat[indB][indA] = DIRECTED

            neighbor = Solution(self.machines, self.operationArr, self.edgesMat)
            approximation = neighbor.GetMakespanApproximation()
            if approximation < bestMakespanApproximation:
                bestMakespanApproximation = approximation
                newEdgesMat = deepcopy(self.edgesMat)
                bestNeighbor = Solution(self.machines, self.operationArr, newEdgesMat)

            self.edgesMat[indA][indB] = DIRECTED
            self.edgesMat[indB][indA] = NO_EDGE

        return bestNeighbor


    def GetMachinesSchedule(self) -> list:
        schedule = [[] for _ in range(self.machines)]

        for operation in self.operationArr[1 : -1]:
            if operation.job == -1: continue
            start = sum(self.operationArr[i].weight for i in self.CriticalPathHelp(0, operation.index)) - operation.weight
            schedule[operation.machine].append( (start, start + operation.weight, operation.job) )

        # for machineInd in range(len(schedule)):
        #     schedule[machineInd].sort(key=cmp_to_key(lambda x, y: self.edgesMat[x][y] != DIRECTED))

        return schedule


def TabuSearch(initialSolution : Solution, iterations : int = 10, tabuSetSize : int = 3):
    currentSolution = initialSolution
    bestSolution = currentSolution

    tabuList = []
    history = []

    for _ in range(iterations):
        bestNeighbor = None
        bestNeighborMakespan = INF

        bestNeighbor = currentSolution.GetBestNeighbor()

        if bestNeighbor is None:
            break

        currentSolution = bestNeighbor
        tabuList.append(bestNeighbor)
        history.append(bestNeighbor.GetMakespan())

        if len(tabuList) > tabuSetSize:
            tabuList.pop(0)

        if bestNeighbor.GetMakespan() < bestSolution.GetMakespan():
            bestSolution = bestNeighbor

    print(history)
    return bestSolution


if __name__ == "__main__":
    file = open("tests/0.json", 'r')
    jobsData = json.loads(file.read())["jobs_data"]
    file.close()

    tabu = TabuSearch(Solution.from_list(jobsData), 0, 3)
    PrintGraph(tabu.edgesMat)
    print(tabu.GetMakespan())
    print(tabu.GetMachinesSchedule())
