import json
from math import pow

INF = 999999


class Job:
    def __init__(self, tasks : list[list[int]]) -> None:
        self.machinesMap = {}

        startTime = 0
        for task in tasks:
            machine_id = task[0]
            processingTime = task[1]
            self.machinesMap.update({machine_id : [startTime, startTime + processingTime]})
            startTime += processingTime

        self.duration = startTime
        return


    def __getitem__(self, machine_id : int) -> list[int]:
        return self.machinesMap[machine_id]


def SegmentsCollide(A, B, C, D) -> bool:
    '''
    Returns True if AB and CD intersect in an INTERNAL point
    '''

    # E = B-A = ( Bx-Ax, By-Ay )
    # F = D-C = ( Dx-Cx, Dy-Cy )
    # P = ( -Ey, Ex )
    # h = ( (A-C) * P ) / ( F * P )

    # чтобы написть это нормально нужно сделать класс для 2д векторов а мне лень простите
    E = [ B[0] - A[0], B[1] - A[1] ]
    F = [ D[0] - C[0], D[1] - C[1] ]

    top = (A[0] - C[0]) * -E[1] + (A[1] - C[1]) * E[0]
    bot = F[0] * -E[1] + F[1] * E[0]
    if bot == 0: return False

    h = top / bot
    return 0 < h and h < 1


class Block:
    def __init__(self, taskA : list[int], taskB : list[int]) -> None:
        self.top_left = [taskA[0], taskB[1]]
        self.top_right = [taskA[1], taskB[1]]
        self.bottom_left = [taskA[0], taskB[0]]
        self.bottom_right = [taskA[1], taskB[0]]
        return


    def CollidesWithSegment(self, pointA : list[int], pointB : list[int]) -> bool:
        if SegmentsCollide(pointA, pointB, self.top_left, self.top_right):
            return True

        if SegmentsCollide(pointA, pointB, self.top_right, self.bottom_right):
            return True

        if SegmentsCollide(pointA, pointB, self.bottom_right, self.bottom_left):
            return True

        if SegmentsCollide(pointA, pointB, self.bottom_left, self.top_left):
            return True

        return False


    def GetVertices(self) -> list[list[int]]:
        return [self.top_left, self.top_right, self.bottom_right, self.bottom_right]


def CalculateDistance(pointA : list[int], pointB : list[int]) -> int:
    # return int(pow(pointB[0] - pointA[0], 2) + pow(pointB[1] - pointA[1], 2))
    x = pointB[0] - pointA[0]
    y = pointB[1] - pointA[1]
    return x + y - min(x, y)


class Solver:
    def __init__(self, jobsData) -> None:
        self.numberOfMachines = len(jobsData[0])
        jobA = Job(jobsData[0])
        jobB = Job(jobsData[1])

        self.endpoint = [jobA.duration, jobB.duration]
        self.blocks = []
        self.vertices = [self.endpoint, [0, jobA.duration], [jobB.duration, 0]]
        for i in range(self.numberOfMachines):
            block = Block(jobA[i], jobB[i])
            self.blocks.append(block)
            self.vertices.extend(block.GetVertices())

        # сортировка по диагоналям
        self.vertices.sort(key = lambda vertex: vertex[0] + vertex[1])
        return


    def GetShortestPathFrom(self, pointA : list[int]) -> tuple[list[list[int]], int]:
        if pointA == self.endpoint:
            return [self.endpoint], 0

        shortestPathLen = INF
        shortestPath = []

        for pointB in self.vertices:
            # @TODO: bin search here
            if pointA[0] + pointA[1] >= pointB[0] + pointB[1]:
                continue

            collision = False
            for block in self.blocks:
                if block.CollidesWithSegment(pointA, pointB):
                    collision = True
                    break

            if collision: continue

            path, len = self.GetShortestPathFrom(pointB)
            candidatePath = [pointA]
            candidatePath.extend(path)
            candidatePathLen = len + CalculateDistance(pointA, pointB)

            if candidatePathLen < shortestPathLen:
                shortestPathLen = candidatePathLen
                shortestPath = candidatePath

        if shortestPathLen == INF:
            raise RuntimeError("Ill-formed JSSP")
        return shortestPath, shortestPathLen


    def Solve(self) -> tuple[list[list[int]], int]:
        return self.GetShortestPathFrom([0, 0])
