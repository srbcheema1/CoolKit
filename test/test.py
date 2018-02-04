from randy import *
from srbIo import *

n = rand(10)
print(n)
arr = rand_arr(n,10)
printf(arr)

q = rand(10)
print(q)
for i in range(1,q+1):
    print(rand(1,n),rand(1,10))
