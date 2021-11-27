from config import queue, lockedObj

def isLocked(obj): #check if object is locked somewhere
    return any(obj in x for x in lockedObj)

def isLockedHere(obj, transaction): #check if object is locked by this transaction
    return (obj in lockedObj[transaction-1])

def grantLock(obj, transaction): #grant lock to object in this transaction
    print("Grant lock(" + str(obj) + "," + "T" + str(transaction) + ")")
    lockedObj[transaction-1].append(obj)

def releaseLock(obj, transaction): #release lock from object in this transaction
    print("Release lock(" + str(obj) + "," + "T" + str(transaction) + ")")
    lockedObj[transaction-1].remove(obj)

n = 1
def read(obj, transaction):
    if isLocked(obj):
        if isLockedHere(obj, transaction):
            print("T" + str(transaction) + ": Read " + str(obj))
        else:
            global n
            if(len(queue[transaction-1]) == 0):
                queue[transaction-1].append(n)
                n += 1
            queue[transaction-1].append('read')
            queue[transaction-1].append(obj)

    else:
        grantLock(obj, transaction)
        print("T" + str(transaction) + ": Read " + str(obj))

def write(obj, transaction):
    if isLocked(obj):
        if isLockedHere(obj, transaction):
            print("T" + str(transaction) + ": Write " + str(obj))
        else:
            global n
            if(len(queue[transaction-1]) == 0):
                queue[transaction-1].append(n)
                n += 1
            queue[transaction-1].append('write')
            queue[transaction-1].append(obj)
            #abort(transaction)

    else:
        grantLock(obj, transaction)
        print("T" + str(transaction) + ": Write " + str(obj))

def commit(transaction):
    if len(queue[transaction-1]) != 0 and "commit" not in queue[transaction-1]:
        queue[transaction-1].append('commit')
        queue[transaction-1].append('')

    else:
        print("Commit " + "T" + str(transaction))
        for _ in range(len(lockedObj[transaction-1])):
            releaseLock(lockedObj[transaction-1][0], transaction)

def abort(transaction):
    for _ in range(len(lockedObj[transaction-1])):
        releaseLock(lockedObj[transaction-1][0], transaction)


def execute(queue):
    m = 1
    for i in range(0, len(queue)):
        if len(queue[i]) != 0:
            if queue[i][0] == m:
                if len(queue[i]) <= 5:
                    for j in range(1, len(queue[i]), 2):
                        command = queue[i][j]
                        obj = queue[i][j+1]
                        t = i + 1
                        if command == "read":
                            read(obj, t)
                        elif command == "write":
                            write(obj, t)
                        elif command == "commit":
                            commit(t)
                m += 1
                    