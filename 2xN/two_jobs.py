import json
from math import pow

INF = 999999


class Job:
    def __init__(self, tasks : list[list[int]]) -> None:
        self.machinesMap = {}

        start_time = 0
        for task in tasks:
            machine_id = task[0]
            processing_time = task[1]
            self.machinesMap.update({machine_id : [start_time, start_time + processing_time]})
            start_time += processing_time

        self.duration = start_time
        return


    def __getitem__(self, machine_id : int) -> list[int]:
        return self.machinesMap[machine_id]


class Block:
    def __init__(self, taskA : list[int], taskB : list[int]) -> None:
        self.top_left = [taskA[0], taskB[1]]
        self.top_right = [taskA[1], taskB[1]]
        self.bottom_left = [taskA[0], taskB[0]]
        self.bottom_right = [taskA[1], taskB[0]]
        return


    def Collides(self, pointA : list[int], pointB : list[int]) -> bool:
        return False


    def GetVertices(self) -> list[list[int]]:
        return [self.top_left, self.top_right, self.bottom_right, self.bottom_right]


    def Print(self) -> None:
        print(self.bottom_left, self.top_right)
        return


def CalculateDistance(pointA : list[int], pointB : list[int]) -> int:
    return int(pow(pointB[0] - pointA[0], 2) + pow(pointB[1] - pointA[1], 2))


class Solver:
    def __init__(self, jobsData) -> None:
        self.number_of_machines = len(jobsData[0])
        jobA = Job(jobsData[0])
        jobB = Job(jobsData[1])

        self.endpoint = [jobA.duration, jobB.duration]
        self.blocks = []
        self.vertices = [self.endpoint]
        for i in range(self.number_of_machines):
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
            if pointA[0] + pointA[1] >= pointB[0] + pointB[1]:
                continue

            for block in self.blocks:
                if block.Collides(pointA, pointB):
                    continue

            path, len = self.GetShortestPathFrom(pointB)
            candidatePath = [pointA]
            candidatePath.extend(path)
            candidatePathLen = len + CalculateDistance(pointA, pointB)

            if candidatePathLen < shortestPathLen:
                shortestPathLen = candidatePathLen
                shortestPath = candidatePath

        if shortestPathLen == INF: raise RuntimeError
        return shortestPath, shortestPathLen



    def Solve(self) -> tuple[list[list[int]], int]:
        return self.GetShortestPathFrom([0, 0])


if __name__ == "__main__":
    with open("2xN/two_jobs.json", 'r') as file:
        jobsData = json.loads(file.read())["jobs_data"]

    solver = Solver(jobsData)
    ans = solver.Solve()
    print(ans[0])
    print(ans[1])
