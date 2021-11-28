from lock import *

read("A", 1)
read("B", 1)
write("A", 2)
read("A", 2)
commit(1)
commit(2)
execute()