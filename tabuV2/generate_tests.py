import os
import random

TEST_COUNT = 20
MACHINES = 10
MAX_TIME = 10
JOBS = 10


def GenerateJob(NUM_MACHINES) -> str:
    job = []

    for machine in range(NUM_MACHINES):
        if machine!=1 and random.randint(0, 1) == 0: continue
        job.append([machine, random.randint(1, MAX_TIME)])
    return job


def GenerateTest(i) -> str:
    test = []
    for _ in range(JOBS):
        test.append(GenerateJob(i))

    return '{\"jobs_data\": ' + str(test) + '}'


if __name__ == "__main__":
    existing_files = os.listdir("tests_for_graphics/")

    count = 0
    current = 0
    JOBS = 20
    while count < TEST_COUNT:
        for i in range(3, MACHINES+1):
            filename = f"{current}.json"
            current += 1
            count += 1

            if filename in existing_files: continue

            file = open("tests_for_graphics/" + filename, 'w')
            file.write(GenerateTest(i))
            file.close()


