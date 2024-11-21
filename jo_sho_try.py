import random as rd

number = 100
end_n = 10
dick = {} #dicl = {job{i} =
# dick['jobs'] = [[] for i in range(number)]  # number = 100 jobs we consider
for i in range(number):
    n_x = rd.randint(1, 3)  # generate 1 to 3 jobs in task
    t_x = [rd.randint(1, end_n) for _ in range(n_x)]  # time for x job
    dick[f'task{i+1}'] = t_x
with open('data1.txt', 'w') as f:
    f.write(str(dick))
    f.close()
