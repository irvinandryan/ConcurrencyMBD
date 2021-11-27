from lock import *

'''
#simple example
read("A", 1)
read("A", 2)
write("A", 3)
commit(1)
commit(2)
commit(3)
execute()
'''

#deadlock
read("B", 1)
write("B", 1)
read("A", 2)
read("B", 2)
write("A", 1)
commit(1)
commit(2)
execute()
