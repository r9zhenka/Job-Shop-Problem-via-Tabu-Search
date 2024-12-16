import json
from collections import defaultdict


INF = 9999999


class Job:
    def __init__(self, operations : list[list[int]]) -> None:
        self.machinesMap = {}

        startTime = 0
        for operation in operations:
            machine_id = operation[0]
            processingTime = operation[1]
            self.machinesMap.update({machine_id : [startTime, startTime + processingTime]})
            startTime += processingTime

        self.duration = startTime
        return


    def UsesMachine(self, machine_id : int) -> bool:
        return machine_id in self.machinesMap.keys()


    def __getitem__(self, machine_id : int) -> list[int]:
        return self.machinesMap[machine_id]


def SegmentsCollideAt(A, B, C, D) -> float:
    E = [ B[0] - A[0], B[1] - A[1] ]
    F = [ D[0] - C[0], D[1] - C[1] ]

    top = (A[0] - C[0]) * -E[1] + (A[1] - C[1]) * E[0]
    bot = F[0] * -E[1] + F[1] * E[0]
    if bot == 0: return False

    h = top / bot
    return h


class Block:
    def __init__(self, operationA : list[int], operationB : list[int], index) -> None:
        self.top_left = (operationA[0], operationB[1])
        self.top_right = (operationA[1], operationB[1])
        self.bottom_left = (operationA[0], operationB[0])
        self.bottom_right = (operationA[1], operationB[0])
        self.index = index
        return


    def CollidesWithLineAt(self, pointA : tuple[int, int], pointB : tuple[int, int]) -> float:
        a = SegmentsCollideAt(pointA, pointB, self.bottom_left, self.bottom_right)
        if 0 < a < 1 and pointA[1] < self.bottom_right[1]:
            return SegmentsCollideAt(self.bottom_left, self.bottom_right, pointA, pointB)

        b = SegmentsCollideAt(pointA, pointB, self.bottom_left, self.top_left)
        if 0 < b < 1 and pointA[0] < self.bottom_left[0]:
            return SegmentsCollideAt(self.bottom_left, self.top_left, pointA, pointB)

        # CHECK 4 DIAGONAL EDGECASE
        if self.bottom_left[0] - pointA[0] == self.bottom_left[1] - pointA[1] and pointA[0] < self.bottom_left[0]:
            return SegmentsCollideAt(self.top_left, self.bottom_right, pointA, pointB)

        return 0


def CalculateDistance(pointA : tuple[int, int], pointB : tuple[int, int]) -> int:
    x = pointB[0] - pointA[0]
    y = pointB[1] - pointA[1]
    return x + y - min(x, y)


def GetFirstBlockCollision(blocks : list[Block], point : tuple[int, int], endpoint : tuple[int, int]) -> Block | None:
    pointB = (point[0] + max(endpoint), point[1] + max(endpoint))
    first = None
    minH = INF
    for block in blocks:
        if point == block.bottom_left: return block

        h = block.CollidesWithLineAt(point, pointB)
        if h == 0: continue
        if h < minH:
            minH = h
            first = block

    return first


class Solver:
    def __init__(self, jobsData) -> None:
        self.machines = max( max(operation[0] for operation in job) for job in jobsData ) + 1

        jobA = Job(jobsData[0])
        jobB = Job(jobsData[1])

        self.vertices = [ (0, 0) ]

        blocks = []
        for i in range(self.machines):
            if not (jobA.UsesMachine(i) and jobB.UsesMachine(i)):
                continue

            block = Block(jobA[i], jobB[i], len(self.vertices))
            blocks.append(block)

            if block.top_left == block.bottom_right:
                continue

            self.vertices.append(block.top_left)
            self.vertices.append(block.bottom_right)

        self.endpoint = (jobA.duration, jobB.duration)
        self.vertices.append(self.endpoint)

        self.edges = [ [0 for i in range(len(self.vertices))] for _ in range(len(self.vertices)) ]

        blocks.sort(key=lambda block: block.top_left[0] + block.top_left[1])
        for ind in range(len(self.vertices)):
            firstBlock = GetFirstBlockCollision(blocks, self.vertices[ind], self.endpoint)
            if firstBlock is None:
                self.edges[ind][-1] = CalculateDistance(self.vertices[ind], self.vertices[-1])
            else:
                self.edges[ind][firstBlock.index] = CalculateDistance(self.vertices[ind], firstBlock.top_left)
                self.edges[ind][firstBlock.index + 1] = CalculateDistance(self.vertices[ind], firstBlock.bottom_right)

        return


    def Solve(self) -> tuple[list[list[int]], int]:
        path = []
        start, finish = 0, len(self.vertices) - 1
        q = [ (start, 0) ]
        minDistances = [INF for _ in range(len(self.vertices))]
        while(q):
            curr, distance = q.pop()

            minDistances[curr] = distance

            for child in range(len(self.edges)):
                if self.edges[curr][child] == 0:
                    continue

                if minDistances[child] < distance + self.edges[curr][child]:
                    continue

                q.append( (child, distance + self.edges[curr][child]) )

        return path, minDistances[-1]
