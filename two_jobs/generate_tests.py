import os
import random


TEST_COUNT = 5
MACHINES = 25
MAX_TIME = 100

def GenerateJob() -> str:
    job = "["

    for machine in range(MACHINES):
        # if random.randint(0, 1) == 0: continue
        job += f"[{machine}, {random.randint(0, MAX_TIME)}]"

        if machine != MACHINES - 1:
            job += ','

    job += "]"
    return job


def GenerateTest() -> str:
    test = "{\"jobs_data\": ["
    test += GenerateJob()
    test += ","
    test += GenerateJob()

    test += "]}"
    return test


if __name__ == "__main__":
    existing_files = os.listdir("tests/")

    count = 0
    while count < TEST_COUNT:
        filename = f"{count}.json"
        if filename in existing_files: continue

        file = open("tests/" + filename, 'w')
        file.write(GenerateTest())
        file.close()

        count += 1
