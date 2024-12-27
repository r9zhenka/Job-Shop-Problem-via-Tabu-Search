# tabu_search
# What is it
Two solution for classic Job Shop Problem
We used (Google_solver|https://github.com/google/or-tools)  as a benchmark ((guide|https://developers.google.com/optimization/scheduling/job_shop))
The used sources are listed in the files references.txt in each directory (tabuV2 and two_jobs)
Files "test.py" compilate main files and google solver.
Files "generate_tests" generate files with random values if they have not existed yet. Number of machines, jobs, range of times (weight) and number of operations in each job can be edited in these files.
##two_jobs
Accurate solution for 2MxN dimension.
Main code is located in "two_jobs.py" and, of course, it has not cool speed

##TabuV2
Main file is "tabu.py"
There are test files, some statistic and visual comparison with benchmark in subdirectories "statistic", "tests" and "tests for graphics"
"Visualisation.py" has function for output Gantt's charts and a graph that shows the improvement of the makespan, taking into account the increase in the number of iterations for a particular file, which can be edit for graphs which will be output editing makespan-benchmark for each file in tests set.
We use graph method based on (this article|https://www.researchgate.net/publication/226183797_Applying_Tabu_Search_to_the_Job-Shop_Scheduling_Problem). Also we didnt realised all methods and functions from this file, so "tabu.py" can be improved and output better makespan.
