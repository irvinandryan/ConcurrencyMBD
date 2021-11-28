from lock import *

read("A", 1)
read("A", 2)
write("A", 3)
commit(1)
commit(2)
commit(3)
execute()