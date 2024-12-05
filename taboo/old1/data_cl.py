import json
import random
data = {
    f'task{i+1}': [random.randint(1, 10) for _ in range(random.randint(1, 3))]
    for i in range(100)
}
with open('data.json', 'w') as f:
    json.dump(data, f)
    f.close()
