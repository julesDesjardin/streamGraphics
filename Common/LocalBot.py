from Common import SQLiteQueue


class LocalBot:

    def __init__(self, receiver, callback):
        if receiver:
            self.queue = SQLiteQueue.SQLiteQueue("localData.db", callback)
        else:
            self.queue = SQLiteQueue.SQLiteQueue("localData.db")

    def polling(self):
        pass

    def send_message(self, id, message):
        self.queue.put(message)
