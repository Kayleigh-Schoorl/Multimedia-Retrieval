import time
from accuracy_test import evaluate
from accuracy_test_knn import evaluate_knn
import os
import statistics

os.chdir("..")

times = []
for i in range(20):
    start = time.time()
    print("Starting the normal querying...")
    evaluate()
    end = time.time()
    print("Time measured for querying using exact distance: " + str(end - start))
    times.append(end - start)
print("Average time for exact distance: " + str(statistics.mean(times)))
print("Standard deviation for exact distance: " + str(statistics.stdev(times)))

times_knn = []
for i in range(20):
    start_knn = time.time()
    print("Starting the k-nn querying...")
    evaluate_knn()
    end_knn = time.time()
    print("Time for querying using k-nn: " + str(end_knn - start_knn))
    times_knn.append(end_knn - start_knn)
print("Average time for k-nn: " + str(statistics.mean(times_knn)))
print("Standard deviation for k-nn: " + str(statistics.stdev(times_knn)))