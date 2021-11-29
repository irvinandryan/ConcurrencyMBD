class Task:

    def __init__(self, tipe, data, txn, timestamp):
        self.type = tipe.lower()
        self.data = str(data).lower()
        self.txn = int(txn)
        self.timestamp = timestamp
        self.uniqueTimestamp = "-"

    def print_details(self):
        print("Type: "+ self.type)
        print("Data: " + self.data)
        print("Transaction: " + str(self.txn))
        print("Timestamp: "+str(self.timestamp))

    def setUniqueTimestamp(self, uniqueTimestamp):
        self.uniqueTimestamp = uniqueTimestamp

