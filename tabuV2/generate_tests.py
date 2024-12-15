import os
import random





def GenerateJob(NUM_MACHINES = 10, MAX_TIME = 100) -> str:
    job = []

    for machine in range(NUM_MACHINES):
        if machine != 1 and random.randint(0, 1) == 0: continue
        job.append([machine, random.randint(1, MAX_TIME)])

    return job


def GenerateTest(JOBS = 10, MACHINES = 10, MAX_TIME = 100) -> str:

    test = []
    for _ in range(JOBS):
        test.append(GenerateJob(MACHINES, MAX_TIME = MAX_TIME))

    return '{\"jobs_data\": ' + str(test) + '}'


def main(TEST_COUNT = 1, MACHINES = 10, MAX_TIME = 100, JOBS = 10, directory = "tests/", filenm = ""):
    # TEST_COUNT = 1
    # MACHINES = 60
    # MAX_TIME = 100
    # JOBS = 10
    existing_files = os.listdir(directory)

    count = 0
    current = 0
    while count < TEST_COUNT:
        filename = filenm + str(current) + ".json"
        current += 1

        if filename in existing_files: continue

        file = open("tests/test_on_dims/" + filename, 'w')
        file.write(GenerateTest(JOBS, MACHINES, MAX_TIME))
        file.close()

        count += 1
main(TEST_COUNT=5, MACHINES=2, JOBS=6, directory="tests/test_on_dims/")