#sequential time
import os
import subprocess
import matplotlib.pyplot as plt
import shlex
sizes = [100000]
threads = [1, 2, 4, 8, 16]
# sizes = [10000, 50000]
# threads = [1,2]


try:
    subprocess.call('rm ./time_seq.txt', shell=True)
except:
    print("exception")

for size in sizes:
    syntax = 'sh run_sequential.sh 10 datasets/dataset_' + str(size)+'_4.txt out_'+str(size)+'.txt cent_'+str(size)+'.txt'

    print("syntax:", syntax)
    subprocess.call(shlex.split(syntax))

try:
    subprocess.call('rm ./time_pthread.txt', shell=True)
except:
    print("exception")


try:
    subprocess.call('rm ./time_omp.txt', shell=True)
except:
    print("exception")

for size in sizes:
    for thread in threads:
        syntax = 'sh run_omp.sh 10 '+str(thread)+' datasets/dataset_' + str(size)+'_4.txt out_'+str(size)+'.txt cent_'+str(size)+'.txt'
        print("syntax:", syntax)
        subprocess.call(shlex.split(syntax))


file_seq ="time_seq.txt"
file_omp ="time_openmp.txt"

file_s_pthread = open("speedup_omp.txt", "a")
with open(file_seq) as f:
    sequential = f.readlines()
sequential=[x.strip() for x in sequential]
sequential = list(map(float, sequential))
print('sequential times:', sequential)


with open(file_omp) as f:
    omp = f.readlines()
omp=[x.strip() for x in omp]
omp = list(map(float, omp))
print('omp times:', omp)

i = 0
num_proc = len(threads)
for t_s in sequential:
    print("size:", sizes[i])
    currentlist_omp = omp[i*num_proc:(i+1)*num_proc]
    print("current:", currentlist_omp)
    speedup_omp = [t_s/x for x in currentlist_omp]
    plt.plot(threads, speedup_omp,label="OpenMP")
    print("speedup:", speedup_omp)
    i+=1

plt.legend()
plt.xlabel("Number of threads")
plt.ylabel("Mutiplier")
plt.savefig("TIME SPEEDUP")
