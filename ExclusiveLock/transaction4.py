from lock import *

read("B", 1)
write("B", 1)
read("A", 2)
read("B", 2)
commit(2)
read("A", 1)
write("A", 1)
commit(1)
execute()